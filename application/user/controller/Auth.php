<?php

namespace app\user\controller;

use app\user\model\UserModel;
use think\Db;
use tools\Geetest;

class Auth
{
    public function getGeetestInfo()
    {
        $geetestID = env('GEETEST_ID');
        $geetestKey = env('GEETEST_KEY');
        $isGeetest = !empty($geetestID) && !empty($geetestKey);
        if (!$isGeetest)
            return json(['status' => 0, 'msg' => '极验证接口尚未开启']);
        $gtSDK  = new Geetest($geetestID, $geetestKey);
        $request = request();
        $data   = [
            'client_type' => $request->isMobile() ? 'h5' : 'web',
            'ip_address'  => $request->ip()
        ];
        $status = $gtSDK->pre_process($data, 1);
        session('gtServerStatus', $status);
        return json($gtSDK->get_response());
    }

    /**
     * @return \think\response\Json
     * @throws \think\db\exception\DataNotFoundException
     * @throws \think\db\exception\ModelNotFoundException
     * @throws \think\exception\DbException
     */
    public function postRegister()
    {
        $email    = input('post.email/s');
        $username = input('post.username/s');
        $password = input('post.password/s');
        if (empty($email))
            return json(['status' => 0, 'msg' => '邮箱账户不能为空']);
        if (empty($username))
            return json(['status' => 0, 'msg' => '用户名不能为空']);
        if (empty($password))
            return json(['status' => 0, 'msg' => '密码不能为空']);
        if (mb_strlen($username, 'utf-8') > 128)
            return json(['status' => 0, 'msg' => '用户名不能超过128个字符']);
        if (mb_strlen($email, 'utf-8') > 128)
            return json(['status' => 0, 'msg' => '邮箱账户长度不能超过128个字符']);
        if (!filter_var($email, FILTER_VALIDATE_EMAIL))
            return json(['status' => 0, 'msg' => '邮箱账户格式不正确']);

        $selectResult = Db::name('user')->whereRaw('username=:username or email=:email', [
            'username' => $username,
            'email'    => $email
        ])->field('username,email')->limit(1)->select();
        if (!empty($selectResult)) {
            if (strcasecmp($username, $selectResult[0]['username']) == 0)
                return json(['status' => 0, 'msg' => '该用户名已被使用']);
            if (strcasecmp($email, $selectResult[0]['email']))
                return json(['status' => 0, 'msg' => '该邮箱账户已被使用']);
        }
        //check data
        $salt         = getRandChar(6);
        $password     = hash('sha256', hash('sha256', $password) . $salt);
        $insertResult = Db::name('user')->insertGetId([
            'username'   => $username,
            'password'   => $password,
            'salt'       => $salt,
            'email'      => $email,
            'createTime' => getDateTime()
        ]);
        if (!$insertResult)
            return json(['status' => 0, 'msg' => '服务器异常,注册账户失败,请联系站长处理。']);
        return json(['status' => 1, 'msg' => '注册账户成功']);
    }

    public function postLogin()
    {
        $loginName = input('post.loginName/s');
        $password  = input('post.password/s');

        if (empty($loginName) || empty($password))
            return json(['status' => 0, 'msg' => '登录账户或密码不能为空']);
        if (mb_strlen($loginName, 'utf-8') > 128)
            return json(['status' => 0, 'msg' => '登录账户或者密码不正确']);
        $isEmail      = !filter_var($loginName, FILTER_VALIDATE_EMAIL);
        $selectResult = Db::name('user');
        if ($isEmail)
            $selectResult = $selectResult->where('username=:loginName');
        else
            $selectResult = $selectResult->where('email=:loginName');
        $selectResult = $selectResult->bind(['loginName' => $loginName])->field('id,username,password,salt')->limit(1)->select();
        if (empty($selectResult))
            return json(['status' => 0, 'msg' => '[1]登录账户或密码不正确']);
        $verifyPassword = hash('sha256', hash('sha256', $password) . $selectResult[0]['salt']);
        if ($verifyPassword != $selectResult[0]['password'])
            return json(['status' => 0, 'msg' => '[2]登录账户或密码不正确']);
        $token = hash('sha256', time() . uniqid()) . '-' . $selectResult[0]['id'];
        //build token
        $expireTime   = strtotime('+2 hours');
        $insertResult = UserModel::setAttr($selectResult[0]['id'], 'loginToken', serialize(['token' => $token, 'expire' => $expireTime]));
        //save token add expire time
        if (!$insertResult)
            return json(['status' => 0, 'msg' => '系统异常,登录账号失败,请重试']);
        return json([
            'status'     => 1,
            'msg'        => '登录账号成功',
            'token'      => $token,
            'expireTime' => $expireTime,
            'uid'        => $selectResult[0]['id'],
            'username'   => $selectResult[0]['username']
        ]);
    }
}