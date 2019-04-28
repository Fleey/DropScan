<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006-2016 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: 流年 <liu21st@gmail.com>
// +----------------------------------------------------------------------

// 应用公共文件

/**
 * 获取随机字符串
 * @param int $length
 * @return null|string
 */
function getRandChar($length = 8)
{
    $str    = null;
    $strPol = "ABCDEFGHIJKMNPQRSTUVWXYZ23456789abcdefghjkmnpqrstuvwxyz";
    $max    = strlen($strPol) - 1;
    for ($i = 0; $i < $length; $i++) {
        $str .= $strPol[rand(0, $max)];
    }
    return $str;
}

/**
 * 返回当前时间格式 存储数据库专用
 * @return false|string
 */
function getDateTime()
{
    return date('Y-m-d H:i:s', time());
}

function is_mobile($text)
{
    $search = '/^1[34578]{1}\d{9}$/';
    if (preg_match($search, $text)) {
        return true;
    } else {
        return false;
    }
}

function is_email($text)
{
    return filter_var($text, FILTER_VALIDATE_EMAIL) === false ? false : true;
}

function getClientIp()
{
    $ip = $_SERVER['REMOTE_ADDR'];
    if (isset($_SERVER['HTTP_X_FORWARDED_FOR']) && preg_match_all('#\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}#s', $_SERVER['HTTP_X_FORWARDED_FOR'], $matches)) {
        foreach ($matches[0] AS $xip) {
            if (!preg_match('#^(10|172\.16|192\.168)\.#', $xip)) {
                $ip = $xip;
                break;
            }
        }
    } elseif (isset($_SERVER['HTTP_CLIENT_IP']) && preg_match('/^([0-9]{1,3}\.){3}[0-9]{1,3}$/', $_SERVER['HTTP_CLIENT_IP'])) {
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (isset($_SERVER['HTTP_CF_CONNECTING_IP']) && preg_match('/^([0-9]{1,3}\.){3}[0-9]{1,3}$/', $_SERVER['HTTP_CF_CONNECTING_IP'])) {
        $ip = $_SERVER['HTTP_CF_CONNECTING_IP'];
    } elseif (isset($_SERVER['HTTP_X_REAL_IP']) && preg_match('/^([0-9]{1,3}\.){3}[0-9]{1,3}$/', $_SERVER['HTTP_X_REAL_IP'])) {
        $ip = $_SERVER['HTTP_X_REAL_IP'];
    }
    return $ip;
}

function curl($url = '', $addHeaders = [], $requestType = 'get', $requestData = '', $postType = '', $urlencode = true, $isProxy = false)
{
    if (empty($url))
        return '';
    //容错处理
    $headers  = [
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    ];
    $postType = strtolower($postType);
    if ($requestType == 'get' && is_array($requestData)) {
        $tempBuff = '';
        foreach ($requestData as $key => $value) {
            $tempBuff .= $key . '=' . $value . '&';
        }
        $tempBuff = trim($tempBuff, '&');
        $url      .= '?' . $tempBuff;
    }
    //手动build get请求参数

    if (!empty($addHeaders))
        $headers = array_merge($headers, $addHeaders);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);

    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    //设置允许302转跳

    if ($isProxy) {
        curl_setopt($ch, CURLOPT_PROXYAUTH, CURLAUTH_BASIC);
        curl_setopt($ch, CURLOPT_PROXY, '127.0.0.1'); //代理服务器地址
        curl_setopt($ch, CURLOPT_PROXYPORT, 8123); //代理服务器端口
        //set proxy
    }
    curl_setopt($ch, CURLOPT_ENCODING, 'gzip');
    //gzip

    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    //add ssl
    if ($requestType == 'get') {
        curl_setopt($ch, CURLOPT_HEADER, false);
    } else if ($requestType == 'post') {
        curl_setopt($ch, CURLOPT_POST, 1);
    } else {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($requestType));
    }
    //处理类型
    if ($requestType != 'get') {
        if (is_array($requestData) && !empty($requestData)) {
            $temp = '';
            foreach ($requestData as $key => $value) {
                if ($urlencode) {
                    $temp .= rawurlencode(rawurlencode($key)) . '=' . rawurlencode(rawurlencode($value)) . '&';
                } else {
                    $temp .= $key . '=' . $value . '&';
                }
            }
            $requestData = substr($temp, 0, strlen($temp) - 1);
        }
        curl_setopt($ch, CURLOPT_POSTFIELDS, $requestData);
    }
    //只要不是get姿势都塞东西给他post
    if ($requestType != 'get') {
        if ($postType == 'json') {
            $headers[]   = 'Content-Type: application/json; charset=utf-8';
            $requestData = is_array($requestData) ? json_encode($requestData) : $requestData;
        } else if ($postType == 'xml') {
            $headers[] = 'Content-Type:text/xml; charset=utf-8';
        }
        $headers[] = 'Content-Length: ' . strlen($requestData);
    }
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    $result = curl_exec($ch);

    curl_close($ch);
    return $result;
}