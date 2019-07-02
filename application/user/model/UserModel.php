<?php

namespace app\user\model;

use think\Db;
use think\Exception;

class UserModel
{
    /**
     * @param int $uid
     * @param string $token
     * @return int // 0 token无效 1 token有效 -1 token超时
     */
    public static function checkLoginToken(int $uid, string $token)
    {
        if (empty($token))
            return 0;
        $data = self::getAttr($uid, 'loginToken');
        if (empty($data))
            return 0;
        $data = unserialize($data);
        if ($data['token'] != $token)
            return 0;
        if ($data['expire'] < time())
            return -1;
        return 1;
    }

    /**
     * @param $uid
     * @param string $key
     * @return string
     */
    public static function getAttr(int $uid, string $key)
    {
        try {
            $result = Db::name('user_attr')->field('attrValue')->limit(1)
                ->where('uid=:uid and attrKey=:key')->bind([
                    'uid' => $uid,
                    'key' => $key
                ])->select();
            if (empty($result))
                $result = '';
            else
                $result = $result[0]['attrValue'];
        } catch (Exception $exception) {
            $result = '';
        }
        return $result;
    }

    /**
     * @param int $uid
     * @param string $key
     * @param string $value
     * @return int|string
     * @throws Exception
     * @throws \think\exception\PDOException
     */
    public static function setAttr(int $uid, string $key, string $value)
    {
        if (self::getAttr($uid, $key) != '') {
            return Db::name('user_attr')->where('uid=:uid and attrKey=:key')->bind([
                'uid' => $uid,
                'key' => $key
            ])->limit(1)->update([
                'attrValue'  => $value,
                'createTime' => getDateTime()
            ]);
        } else {
            return Db::name('user_attr')->insertGetId([
                'uid'        => $uid,
                'attrKey'    => $key,
                'attrValue'  => $value,
                'createTime' => getDateTime()
            ]);
        }
    }
}
