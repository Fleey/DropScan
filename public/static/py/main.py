import imp
import sys
import urllib.request

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

heart_beat_thread = common.heart_beat_threading(API_GATEWAY, USER_LID)
heart_beat_thread.start()

# nm = nmap.PortScanner()
# nm.scan(hosts='127.0.0.1', arguments="-T4 -F")
#
# for host in nm.all_hosts():
#     print('存在下列域名：')
#     for domain in nm[host]['hostnames']:
#         print("domain:" + domain['name'] + ' type:' + domain['type'])
#
#     print('域名开放下列端口：')
#     for port in nm[host]['tcp']:
#         port_info = nm[host]['tcp'][port]
#         print('port:' + str(port) + ' name:' + port_info['name'] + '  ' + port_info['product'] + ' ' +
#               port_info['version'])


# print(common.get_mac_address())
# print(233)
