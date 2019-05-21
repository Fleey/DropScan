<?php

namespace app\api\controller;

use think\Db;

class ApiV1
{
    public function getRun(string $hash = '', int $uid = 1)
    {
        if (empty($hash) || empty($uid))
            return 'print("[-] UID or HASH is fail")';
        $runTemplate = file_get_contents(env('ROOT_PATH') . 'public/static/py/run.py');
        $runTemplate = str_replace('{$USER_UID}', $uid, $runTemplate);
        $runTemplate = str_replace('{$USER_HASH}', $hash, $runTemplate);
        return $runTemplate;
    }

    /**
     * @return \think\response\Json
     * @throws \think\Exception
     * @throws \think\db\exception\DataNotFoundException
     * @throws \think\db\exception\ModelNotFoundException
     * @throws \think\exception\DbException
     * @throws \think\exception\PDOException
     */
    public function postLogin()
    {
        $hash = input('post.hash/s');
        $uid  = input('post.uid/d');

        if (strlen($hash) != 64 || $uid == 0)
            return json(['status' => 0, 'msg' => 'login fail,pls contact web admin.']);

        $mac         = input('post.mac/s');
        $machineInfo = input('post.machineInfo/s');
        if (empty($mac) || empty($machineInfo))
            return json(['status' => 0, 'msg' => 'login fail,login request data fail.']);

        $selectResult = Db::name('machine_link')->where([
            'uid' => $uid
        ])->limit(1)->field('id,hash')->select();

        if (empty($selectResult))
            return json(['status' => 0, 'msg' => 'login fail,uid or hash fail.']);

        if ($selectResult[0]['hash'] != $hash)
            return json(['status' => 0, 'msg' => 'login fail,uid or hash fail.']);
        //判断uid 与 hash 是否正确

        $linkID = $selectResult[0]['id'];
        //获取lid
        $selectResult = Db::name('machine_list')->where([
            'mac' => $mac,
            'lid' => $linkID
        ])->limit(5)->field('id')->select();

        $clientIp = getClientIP();
        //get client ip
        if (count($selectResult) >= 5)
            return json(['status' => 0, 'msg' => 'Just a moment, please,You have reached the maximum limit.']);

        $uuid = uniqid();
        Db::name('machine_list')->insertGetId([
            'uuid'          => $uuid,
            'lid'           => $linkID,
            'clientIP'      => $clientIp,
            'mac'           => $mac,
            'machineInfo'   => $machineInfo,
            'machineStatus' => 0,
            'updateTime'    => getDateTime()
        ]);

        return json([
            'status' => 1,
            'msg'    => 'login success,welcome use DorpScan v' . env('APP_VERSION') . ' programs',
            'lid'    => $linkID,
            'ip'     => $clientIp,
            'uuid'   => $uuid
        ]);
    }

    public function postLogout()
    {
        $lid  = input('post.lid/d');
        $mac  = input('post.mac/s');
        $uuid = input('post.uuid/s');

        if (!$this->verifyMachineData($lid, $mac, $uuid))
            return json(['status' => 0, 'msg' => 'lid or mac or uuid fail']);

        Db::name('machine_list')->where([
            'lid'  => $lid,
            'uuid' => ':uuid'
        ])->bind([
            'uuid' => $uuid
        ])->limit(1)->delete();
        return json(['status' => 1, 'msg' => 'exit login success']);
    }

    /**
     * @return \think\response\Json
     * @throws \think\Exception
     * @throws \think\db\exception\DataNotFoundException
     * @throws \think\db\exception\ModelNotFoundException
     * @throws \think\exception\DbException
     * @throws \think\exception\PDOException
     */
    public function postHeartbeat()
    {
        $lid    = input('post.lid/d');
        $mac    = input('post.mac/s');
        $uuid   = input('post.uuid/s');
        $status = input('post.status/d', 0);

        if (!$this->verifyMachineData($lid, $mac, $uuid))
            return json(['status' => 0, 'msg' => 'lid or mac or uuid fail']);

        $selectResult = Db::name('machine_list')->where([
            'lid'  => $lid,
            'uuid' => ':uuid'
        ])->bind([
            'uuid' => $uuid
        ])->limit(1)->field('mac,uuid,taskList')->select();

        Db::name('machine_list')->where([
            'lid'  => $lid,
            'uuid' => ':uuid'
        ])->bind([
            'uuid' => $uuid
        ])->limit(1)->update([
            'machineStatus' => $status,
            'updateTime'    => getDateTime()
        ]);

        $taskList = unserialize($selectResult[0]['taskList']);

        return json(['status' => 1, 'taskList' => empty($taskList) ? [] : $taskList]);
    }

    /**
     * 提交任务信息
     * @return \think\response\Json
     * @throws \think\db\exception\DataNotFoundException
     * @throws \think\db\exception\ModelNotFoundException
     * @throws \think\exception\DbException
     */
    public function postTaskMessage()
    {
        $taskID = input('post.taskID/d');
        $token  = input('post.token/s');

        $target = input('post.target/s');
        //目标url 或者
        $title   = input('post.title/s');
        $message = input('post.message/s');
        $level   = input('post.level/d');

        if (empty($taskID) || empty($token) || empty($target) || empty($title) || empty($message))
            return json(['status' => 0, 'msg' => 'param fail']);
        //check param
        if (strlen($token) != 32)
            return json(['status' => 0, 'msg' => 'token fail']);
        //check token
        if ($level < 0 || $level > 3)
            return json(['status' => 0, 'msg' => 'message level fail']);
        //check level
        if (strlen($title) > 255)
            return json(['status' => 0, 'msg' => 'title length too long']);
        if (strlen($target) > 255)
            return json(['status' => 0, 'msg' => 'target length too long']);
        $selectTaskData = Db::name('task_list')->where('id', $taskID)->field('token,status')->limit(1)->select();
        if (empty($selectTaskData))
            return json(['status' => 0, 'msg' => 'task id fail or token fail']);
        if ($selectTaskData[0]['status'] == 2)
            return json(['status' => 0, 'msg' => 'task is done']);
        if ($selectTaskData[0]['token'] != $token)
            return json(['status' => 0, 'msg' => 'task id fail or token fail']);

        $insertResult = Db::name('result_temp')->insertGetId([
            'taskID'     => $taskID,
            'target'     => $target,
            'title'      => $title,
            'message'    => $message,
            'level'      => $level,
            'createTime' => getDateTime()
        ]);
        if (!$insertResult)
            return json(['status' => -1, 'msg' => 'insert data fail pls again']);

        return json(['status' => 1]);
    }

    /**
     * @return \think\response\Json
     * @throws \think\db\exception\DataNotFoundException
     * @throws \think\db\exception\ModelNotFoundException
     * @throws \think\exception\DbException
     */
    public function getTaskInfo()
    {
        $lid  = input('get.lid/d');
        $mac  = input('get.mac/s');
        $uuid = input('get.uuid/s');

        $taskID = input('get.taskID/d');

        if (empty($taskID))
            return json(['status' => 0, 'msg' => 'task id fail']);
        if (!$this->verifyMachineData($lid, $mac, $uuid))
            return json(['status' => 0, 'msg' => 'lid or mac or uuid fail']);

        $selectResult = Db::name('task_list')->where([
            'lid' => $lid,
            'id'  => $taskID
        ])->limit(1)->field('scanData,token')->select();

        $token = $selectResult[0]['token'];

        $selectResult           = json_decode($selectResult[0]['scanData'], true);
        $selectResult['taskID'] = $taskID;
        $selectResult['token']  = $token;

        return json(['status' => 1, 'data' => $selectResult]);
    }

    /**
     * @return \think\response\Json
     * @throws \think\Exception
     * @throws \think\db\exception\DataNotFoundException
     * @throws \think\db\exception\ModelNotFoundException
     * @throws \think\exception\DbException
     * @throws \think\exception\PDOException
     */
    public function postTaskStatus()
    {
        $lid  = input('post.lid/d');
        $mac  = input('post.mac/s');
        $uuid = input('post.uuid/s');

        $taskID     = input('post.taskID/s');
        $taskStatus = input('post.taskStatus/d');

        $whiteList = [1, 2];

        if (empty($taskID) || empty($taskStatus))
            return json(['status' => 0, 'msg' => 'task id fail or task status fail']);
        if (!in_array($taskStatus, $whiteList))
            return json(['status' => 0, 'msg' => 'task status fail']);
        if (!$this->verifyMachineData($lid, $mac, $uuid))
            return json(['status' => 0, 'msg' => 'lid or mac or uuid fail']);

        $selectResult = Db::name('task_list')->where([
            'lid' => $lid,
            'id'  => $taskID
        ])->limit(1)->field('status')->select();

        if (empty($selectResult))
            return json(['status' => 0, 'msg' => 'server api exception']);

        if ($selectResult[0]['status'] == 2 || $selectResult[0]['status'] == 3)
            return json(['status' => 0, 'msg' => 'task done change status fail']);
        //任务已经完成 或 终止 不能完成修改
        if ($selectResult[0]['status'] == 1 && $taskStatus == 1)
            return json(['status' => 0, 'msg' => 'task status change fail']);
        $updateTaskListData = [
            'status' => $taskStatus
        ];
        if ($taskStatus == 2)
            $updateTaskListData['endTime'] = getDateTime();
        Db::name('task_list')->where([
            'lid' => $lid,
            'id'  => $taskID
        ])->limit(1)->update($updateTaskListData);
        //更新任务状态
        if ($taskStatus == 2) {
            $selectResult = Db::name('machine_list')->where([
                'uuid' => ':uuid',
                'lid'  => $lid
            ])->bind([
                'uuid' => $uuid
            ])->limit(1)->field('taskList')->select();
            if (!empty($selectResult)) {
                $tempTaskList = unserialize($selectResult[0]['taskList']);
                if (!empty($tempTaskList)) {
                    $tempListData = [];
                    foreach ($tempTaskList as $key => $value) {
                        if ($value['id'] == $taskID)
                            continue;
                        $tempListData[] = $value;
                    }
                    $tempTaskList = serialize($tempListData);
                    Db::name('machine_list')->where([
                        'uuid' => ':uuid',
                        'lid'  => $lid
                    ])->bind([
                        'uuid' => $uuid
                    ])->limit(1)->update([
                        'taskList' => $tempTaskList
                    ]);
                }
            }
        }
        //删除已经完成的任务
        return json(['status' => 1, 'msg' => 'task status change success']);
    }


    /**
     * @param int $lid
     * @param string $mac
     * @param string $uuid
     * @return bool
     * @throws \think\db\exception\DataNotFoundException
     * @throws \think\db\exception\ModelNotFoundException
     * @throws \think\exception\DbException
     */
    private function verifyMachineData(int $lid, string $mac, string $uuid)
    {
        if (empty($mac) || empty($lid) || empty($uuid))
            return false;
        $selectResult = Db::name('machine_list')->where([
            'lid'  => $lid,
            'uuid' => ':uuid'
        ])->bind([
            'uuid' => $uuid
        ])->limit(1)->field('mac')->select();
        if (empty($selectResult))
            return false;
        if ($selectResult[0]['mac'] != $mac)
            return false;
        return true;
    }

    /**
     * @param int $taskID
     * @param string $token
     * @return bool
     * @throws \think\db\exception\DataNotFoundException
     * @throws \think\db\exception\ModelNotFoundException
     * @throws \think\exception\DbException
     */
    private function verifyTaskData(int $taskID, string $token)
    {
        if (empty($taskID) || empty($token))
            return false;
        if (strlen($token) != 64)
            return false;
        $selectTaskData = Db::name('task_list')->where('id', $taskID)->field('token')->limit(1)->select();
        if (empty($selectTaskData))
            return false;
        if ($selectTaskData[0]['token'] != $token)
            return false;
        return true;
    }
}
