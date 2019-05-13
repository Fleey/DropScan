#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: range
# ref: 案例地址
import time


def assign(service, arg):
    if service == 'xinzuobiao':
        return [True, arg]
    return [False, arg]


def audit(arg):
    time.sleep(2)
    print('demo plugins 2 run ' + arg['domain'])


if __name__ == '__main__':
    audit(assign('xinzuobiao', 'http://www.azxx.net/')[1])
