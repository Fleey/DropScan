import imp
import sys
import urllib.request

# def preload_module(chunk, modulename):
#     m = imp.new_module(modulename)
#     exec(chunk, m.__dict__)
#     sys.modules[modulename] = m
#     globals()[modulename] = m
#     return m
#
#
# data = open('./test.py', mode='rb').read()
# data = compile(data, 'tootls', 'exec')
# data = marshal.dumps(data)
# data = zlib.compress(data, 9)
# f = open('./test.py', 'wb')
# f.write(data)
# f.flush()
# f.close()
# preload_module(marshal.loads(zlib.decompress(data)), 'test')
# print(test.generate_random_str(6))
# print(data)

# from lxml import etree
#
# text='''
# <div>
#     <ul>
#          <li class="item-0"><a href="link1.html">第一个</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-0"><a href="link5.html">a属性</a>
#      </ul>
#  </div>
# '''
# html=etree.HTML(text) #初始化生成一个XPath解析对象
# result=etree.tostring(html,encoding='utf-8')   #解析对象输出代码
# print(type(html))
# print(type(result))
# print(result.decode('utf-8'))

if sys.version_info < (3, 6):
    print('[+] must use python < 3.6')
    exit(500)


def load_module(model_name, url):
    u = urllib.request.urlopen(url)
    source = u.read().decode('utf-8')
    mod = sys.modules.setdefault(url, imp.new_module(url))
    code = compile(source, url, 'exec')
    mod.__file__ = url
    mod.__package__ = ''
    exec(code, mod.__dict__)
    sys.modules[model_name] = mod
    globals()[model_name] = mod
    return mod


API_GATEWAY = 'http://scan.cn'
USER_UID = 1
USER_HASH = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'

load_module('common', 'http://scan.cn/static/py/common.py')
load_module('HackRequests', 'http://scan.cn/static/py/lib/HackRequest.py')
load_module('nmap', 'http://scan.cn/static/py/lib/nmap.py')
load_module('scanService', 'http://scan.cn/static/py/lib/scanService.py')
load_module('tootls', 'http://scan.cn/static/py/tootls.py')

common.load_module = load_module
common.HackRequests = HackRequests
common.nmap = nmap
common.scanService = scanService
common.tootls = tootls

login_result = common.login_server(API_GATEWAY, USER_UID, USER_HASH)
print('[+] Waiting for the assignment......')

USER_LID = login_result['lid']
UUID = login_result['uuid']

heart_beat_thread = common.heart_beat_threading(API_GATEWAY, USER_LID, UUID)
heart_beat_thread.start()

# from lib import nmap
#
# nm = nmap.PortScanner()
# nm.scan(hosts='43.248.187.89', arguments="-T4 -F")
#
# for host in nm.all_hosts():
#     print('存在下列域名：')
#     for domain in nm[host]['hostnames']:
#         print("domain:" + domain['name'] + ' type:' + domain['type'])
#
#     print('域名开放下列端口：')
#     for port in nm[host]['tcp']:
#         port_info = nm[host]['tcp'][port]
#         if port_info['state'] != 'closed':
#             print('port:' + str(port) + ' name:' + port_info['name'] + '  ' + port_info['product'] + ' ' +
#                   port_info['version'])

# print(common.get_mac_address())
# print(233)
