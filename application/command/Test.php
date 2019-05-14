<?php

namespace app\command;

use think\console\Command;
use think\console\Input;
use think\console\Output;
use think\Db;

class Test extends Command
{
    protected function configure()
    {
        // 指令配置
        $this->setName('test')->setDescription('user test');
        // 设置参数
    }

    protected function execute(Input $input, Output $output)
    {
        $this->buildFingerprintService();
        // 指令输出
    }

    private function buildFingerprintService()
    {
        $filePath     = __DIR__ . '/../../public/static/py/resources/Feature.json';
        $selectResult = Db::query('SELECT * FROM `scan`.`scan_fingerprint_service` WHERE `name` LIKE \'%ord%\' ORDER BY `name`  LIMIT 0,1000');
//        $selectResult = Db::name('fingerprint_service')->field('name,type,url,content')->where('status', 1)->select();
        file_put_contents($filePath, json_encode($selectResult));
    }

}
