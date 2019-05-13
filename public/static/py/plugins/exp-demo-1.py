#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: range
# ref: 案例地址
import time


def assign(service_name):
    if service_name == 'xinzuobiao':
        return True
    return False


def audit(target_data, user_agent, cookie):
    # print(public.cookie)
    send_scan_result('这个是标题', '这个是信息', 2)
    print(target_data)
    print(tootls.curl('http://127.0.0.1/a.txt', {}, {}))
    # print('demo plugins 1 run ' + arg['domain'])


if __name__ == '__main__':
    audit(assign('xinzuobiao', 'http://www.azxx.net/')[1])
