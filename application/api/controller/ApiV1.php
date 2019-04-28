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
        ])->limit(1)->field('id')->select();

        $clientIp = getClientIP();
        //get client ip
        if (!empty($selectResult)) {
            Db::name('machine_list')->where([
                'id' => $selectResult[0]['id']
            ])->limit(1)->update([
                'clientIP'      => $clientIp,
                'updateTime'    => getDateTime(),
                'machineStatus' => 1,
                'machineInfo'   => $machineInfo
            ]);
            return json(['status' => 1, 'msg' => 'login success,welcome use DorpScan v' . env('APP_VERSION') . ' programs', 'lid' => $selectResult[0]['id'], 'ip' => $clientIp]);
            //机器记录已经存在则更新信息
        }

        $insertResult = Db::name('machine_list')->insertGetId([
            'lid'         => $linkID,
            'clientIP'    => $clientIp,
            'mac'         => $mac,
            'machineInfo' => $machineInfo,
            'status'      => 1,
            'updateTime'  => getDateTime()
        ]);

        return json(['status' => 1, 'msg' => 'login success,welcome use DorpScan v' . env('APP_VERSION') . ' programs', 'lid' => $insertResult, 'ip' => $clientIp]);
    }

    public function postHeartbeat()
    {
        $lid    = input('post.lid/d');
        $mac    = input('post.mac/s');
        $status = input('post.status/d', 0);

        if (empty($lid))
            return json(['status' => 0, 'msg' => 'lid is empty']);
        if (strlen($mac) != 17)
            return json(['status' => 0, 'msg' => 'mac fail']);

        $selectResult = Db::name('machine_list')->where('id', $lid)->limit(1)->field('mac,taskInfo,remoteStatus')->select();
        if (empty($selectResult))
            return json(['status' => 0, 'msg' => 'lid or mac fail']);
        if ($selectResult[0]['mac'] != $mac)
            return json(['status' => 0, 'msg' => 'lid or mac fail']);
        Db::name('machine_list')->where('id', $lid)->limit(1)->update([
            'machineStatus' => $status,
            'updateTime'    => getDateTime()
        ]);
        return json(['status' => 1, 'taskInfo' => $selectResult[0]['taskInfo'], 'remoteStatus' => $selectResult[0]['remoteStatus']]);
    }

}
