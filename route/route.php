<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006~2018 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: liu21st <liu21st@gmail.com>
// +----------------------------------------------------------------------
Route::get('run/:id/:hash', 'api/ApiV1/getRun')->pattern([
    'id'   => '[0-9]{1,6}',
    'hash' => '[a-zA-Z0-9]{64}']);

Route::group('api', function () {
    Route::controller('v1', 'api/ScanApiV1');
});

Route::rule('test', function () {
    dump(serialize([2]));
//    \think\Db::name('task_list')->insertGetId([
//        'uid'        => 1,
//        'token'      => getRandChar(32),
//        'target'     => 'http://www.laruence.com/',
//        'scanData'   => json_encode([
//            'cookie'    => 'none cookie',
//            'userAgent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
//            'isScanC'   => false
//        ]),
//        'status'     => 0,
//        'createTime' => getDateTime()
//    ]);
});