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

        $uuid         = uniqid();
        $insertResult = Db::name('machine_list')->insertGetId([
            'uuid'          => $uuid,
            'lid'           => $linkID,
            'clientIP'      => $clientIp,
            'mac'           => $mac,
            'machineInfo'   => $machineInfo,
            'machineStatus' => 0,
            'remoteStatus'  => 1,
            'updateTime'    => getDateTime()
        ]);

        return json([
            'status' => 1,
            'msg'    => 'login success,welcome use DorpScan v' . env('APP_VERSION') . ' programs',
            'lid'    => $insertResult,
            'ip'     => $clientIp,
            'uuid'   => $uuid
        ]);
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

        if (empty($lid))
            return json(['status' => 0, 'msg' => 'lid is empty']);
        if (strlen($mac) != 17)
            return json(['status' => 0, 'msg' => 'mac fail']);
        if (strlen($uuid) != 13)
            return json(['status' => 0, 'msg' => 'uuid fail']);

        $selectResult = Db::name('machine_list')->where('id', $lid)->limit(1)->field('mac,uuid,taskInfo,remoteStatus')->select();
        if (empty($selectResult))
            return json(['status' => 0, 'msg' => 'lid or mac or uuid fail']);
        if ($selectResult[0]['mac'] != $mac)
            return json(['status' => 0, 'msg' => 'lid or mac or uuid fail']);
        if ($selectResult[0]['uuid'] != $uuid)
            return json(['status' => 0, 'msg' => 'lid or mac or uuid fail']);
        Db::name('machine_list')->where('id', $lid)->limit(1)->update([
            'machineStatus' => $status,
            'updateTime'    => getDateTime()
        ]);
        return json(['status' => 1, 'taskInfo' => $selectResult[0]['taskInfo'], 'remoteStatus' => $selectResult[0]['remoteStatus']]);
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
        if ($selectTaskData[0]['status'])
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
}
