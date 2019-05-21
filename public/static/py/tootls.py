import hashlib
import json
import os
import platform
import random
import re
import string
import uuid
import socket
from urllib import parse, request, error

from urllib.parse import urlparse


# 获取随机字符串
def generate_random_str(random_length=16):
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(random_length)]
    random_str = ''.join(str_list)
    return random_str


# curl 东西
def curl(url, data, headers, type='GET'):
    params = "?"
    for key in data:
        params = params + str(key) + "=" + str(data[key]) + "&"
    data = parse.urlencode(data).encode('utf-8')
    if type != 'GET':
        headers = dict({'Content-Type': 'application/x-www-form-urlencoded'}.items() | headers.items())
        req = request.Request(url, headers=headers, data=data)
    else:
        req = request.Request(url + params)

    try:
        result = request.urlopen(req).read().decode('utf-8')
    except error.URLError as e:
        result = '[' + str(e.code) + '] ' + e.reason
    return result


def curl2(url=None, request_data=None, headers=None, request_type=None, proxy=None, timeout=3):
    if url is None:
        return [500, [], '', 500, 'url is empty']
    if request_type is None:
        request_type = 'get'
    else:
        request_type = request_type.lower()

    if (request_type == 'get' or request_type == 'post') and type(request_data) == dict:
        request_data = parse.urlencode(request_data, encoding='utf-8')
        if request_type == 'get':
            url += '?' + request_data
    if headers is None:
        headers = {}
    if request_type != 'get':
        if request_type == 'json':
            headers['Content-Type'] = 'application/json; charset=utf-8'
            if request_data is None:
                request_data = '{}'
            if type(request_data) == dict or type(request_data) == list:
                request_data = json.dumps(request_data)
        if request_type is 'xml':
            headers['Content-Type'] = 'text/xml; charset=utf-8'
        headers['Content-Length'] = len(request_data)
    # 组合参数
    proxy_handler = request.ProxyHandler({})
    if proxy is not None:
        proxy_handler = proxy
    # 设置代理头
    opener = request.build_opener(proxy_handler)
    if request_type != 'get':
        response = request.Request(url, headers=headers, data=request_data.encode('utf-8'))
    else:
        response = request.Request(url, headers=headers)
    temp_data = []
    try:
        response = opener.open(response, timeout=timeout)
        temp_data.append(response.code)
        temp_data.append(response.getheaders())
        response = response.read().decode('utf-8')
        temp_data.append(response)
        temp_data.append(0)
        temp_data.append('ok')
        return temp_data
    except error.HTTPError as e:
        return [500, [], '', e.code, e.msg]
    except error.URLError as e:
        return [500, [], '', 500, str(e)]
    except WindowsError as e:
        return [500, [], '', 500, str(e)]
    except:
        return [500, [], '', 500, '反正就是异常了']


# 获取本机MAC
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


# 获取本机的系统信息
def get_system_info():
    return platform.platform() + " " + platform.machine()


# 获取字符串的MD5
def get_md5_value(str):
    my_md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
    my_md5.update(str)  # 得到MD5消息摘要
    my_md5_Digest = my_md5.hexdigest()  # 以16进制返回消息摘要，32位
    return my_md5_Digest


# 获取域名的IP地址
def get_url_host(url):  # 域名转IP
    try:
        domain = urlparse(url).hostname
        result = socket.gethostbyname(domain)
        return result
    except:
        return 'unknown ip'


# 获取 url 的根域名地址
def get_domain_root(url):
    return urlparse(url).hostname


# 获取 URL 中请求的文件的后缀名（不适用于重写 URL 规则的 URL）
def get_url_ext(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    return filename


# 判断字符是否为ipv4
def is_ip_v4(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False
