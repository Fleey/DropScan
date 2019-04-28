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
    Route::controller('v1', 'api/ApiV1');
});