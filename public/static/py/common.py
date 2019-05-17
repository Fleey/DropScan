import json
import threading
import time

import threadpool


def banner():
    print("""
     _____                       _____                    
    |  __ \                     / ____|                   
    | |  | |  ___   _ __  _ __ | (___    ___  __ _  _ __  
    | |  | | / _ \ | '__|| '_ \ \___ \  / __|/ _` || '_ \ 
    | |__| || (_) || |   | |_) |____) || (__| (_| || | | |
    |_____/  \___/ |_|   | .__/|_____/  \___|\__,_||_| |_|
                         | |                              
                         |_|                              
    Coded By Fleey (V1.0 RELEASE) email:fleey2013@live.cn
        """)


# print(load_module)

def login_server(server_address, uid, hash):
    banner()

    mac = tootls.get_mac_address()

    login_result = tootls.curl(server_address + '/api/v1/Login', {
        'mac': mac,
        'machineInfo': tootls.get_system_info(),
        'uid': uid,
        'hash': hash
    }, {}, 'POST')

    login_result = json.loads(login_result)
    if login_result['status'] is 0:
        print('[+] ' + login_result['msg'])
        exit(500)

    print('[+] ' + login_result['msg'])
    print('[+] IP => ' + login_result['ip'] + ', LID => ' + str(
        login_result['lid']) + ', MAC => ' + mac + ', UUID => ' + login_result['uuid'])

    return {
        'lid': login_result['lid'],
        'mac': mac,
        'uuid': login_result['uuid']
    }


def get_target_service(target, user_agent='', cookie=''):
    print('[+] load service fingerprint dict ...')
    service_fingerprint_dict = json.loads(tootls.curl('http://scan.cn/static/py/resources/Feature.json', {}, {}))
    print('[+] load service fingerprint ok !')

    print('[+] start service fingerprint target => ' + target)
    scanService.tootls = tootls
    scan_service = scanService.scanService(target, service_fingerprint_dict, user_agent=user_agent, cookie=cookie)
    result = scan_service.scan_domain()
    print('[+] end service fingerprint target => ' + target)
    return result


def get_namp_scan_result(target, args='-T4 -F'):
    target_host = tootls.get_url_host(target)
    print('[+] start use nmap scan target => ' + target_host + ' ...')
    nm = nmap.PortScanner()
    nm.scan(hosts=target_host, arguments=args)
    temp_result = []
    for host in nm.all_hosts():
        for port in nm[host]['tcp']:
            port_info = nm[host]['tcp'][port]
            if port_info['state'] != 'closed':
                temp_result.append({
                    'ip': target_host,
                    'port': str(port),
                    'name': port_info['name']
                })
    print('[+] end use nmap scan target => ' + target_host + ' ...')
    if len(temp_result) == 0:
        return []
    return temp_result


def heart_beat_request(server_address, lid, uuid, status):
    data = tootls.curl(server_address + '/api/v1/Heartbeat', {
        'lid': lid,
        'uuid': uuid,
        'status': status,
        'mac': tootls.get_mac_address()
    }, {}, 'POST')
    if len(data) == 0:
        print('[-][HeartBeat] request network error')
        exit(500)
    try:
        data = json.loads(data)
    except:
        print('[-][HeartBeat] The connection to the server failed')
        exit(500)
    if data['status'] != 1:
        print('[-][HeartBeat] request error info => ' + data['msg'])
    return data


class heart_beat_threading(threading.Thread):
    __lid = None
    __mac = None
    __uuid = None
    __server_gateway = None
    __service_fingerprint_dict = []

    def __init__(self, server_address, lid, uuid):
        threading.Thread.__init__(self)
        self.__lid = lid
        self.__uuid = uuid
        self.__mac = tootls.get_mac_address()
        self.__server_gateway = server_address

    def run(self):
        task_list = {}
        machine_data = {
            'runThread': 0,
        }
        # while True:
        target = 'http://43.248.187.89:8000'
        ua = 'DropScan v1.0.0'
        cookie = 'none'

        # threader = scan_main_threading(
        #     self.__server_gateway,
        #     target,
        #     1,
        #     {
        #         'token': 'hk585KIHvEwFtvRkvMN8uDsYgKeJIdev',
        #         'tid': 2,
        #         'nmap_scan_args': '-T4 -F'
        #     },
        #     ua, cookie)
        # threader.start()
        machine_status = 0
        while True:
            heart_beat_result = heart_beat_request(self.__server_gateway, self.__lid, self.__uuid, machine_status)
            if heart_beat_result['status'] != 1:
                time.sleep(5)
                continue
            # 当心跳数据异常
            if heart_beat_result['remoteStatus'] == 1:
                
            print(heart_beat_result)
            time.sleep(2)
        # machine_status = 0
        # while True:
        #     heart_beat_result = heart_beat_request(self.__server_gateway, self.__lid, self.__uuid, machine_status)

        # threader.run()
        # thread_id = generate_random_str(8)
        # # create random id
        # task_list[thread_id] = {
        #     'target': 'http://127.0.0.1',
        #     'proxy': '127.0.0.1:1080',
        #     'isScanC': False,
        #     'dnsList': '223.5.5.5,223.6.6.6',
        #     'status': 0
        # }
        # pool = ThreadPool(poolsize)
        # heart_beat_result = heart_beat_request(self.server_address, self.lid, machine_status)
        # if heart_beat_result['status'] != 1:
        #     time.sleep(5)
        #     continue
        # if heart_beat_result['remoteStatus'] == 1 and machine_status == 1:
        #     task_info = json.loads(heart_beat_result['taskInfo'])
        #     machine_status = 2
        # if machine_status == 2 and work_threading.is_alive() is False:
        #     machine_status = 1
        #     print('[+] Waiting for the assignment......')
        # 2 sec heart beat


class scan_main_threading(threading.Thread):
    __pool = None
    __request = None

    __plugins_temp = []
    # __run_done_plugins_id = []
    __user_agent = ''
    __cookie = ''
    __targets_data = []
    __server_gateway = ''
    __scan_data = {}

    # threader = scan_main_threading(self.__server_gateway, 'http://www.laruence.com/', 1, {
    #     'lid': self.__lid,
    #     'token': self.__mac,
    #     'tid': 1
    # }, 'none', 'DropScan v1.0.0')
    def __init__(self, server_gateway, target_url, thread_num, scan_data, user_agent='',
                 cookie='test'):
        threading.Thread.__init__(self)

        self.is_suspend = False
        self.is_stop = False
        # 这两个参数控制暂停与停止

        self.user_agent = user_agent
        self.__cookie = cookie
        self.__targets_data.append({
            'target_url': target_url
        })
        self.__server_gateway = server_gateway
        self.__scan_data = scan_data

        # self.__run_done_plugins_id = []
        # 这个参数用来存储已经完成的插件ID 用于暂停后恢复线程 并且不会假死
        self.__load_plugins()
        # 加载插件列表
        self.__pool = threadpool.ThreadPool(thread_num)
        self.__requests = threadpool.makeRequests(callable_=self.__run_plugins, args_list=self.__plugins_temp,
                                                  callback=self.__check_status)
        # 这两行用来初始化线程池

    def __load_plugins(self):
        plugins = [
            {
                'id': 1,
                'hash': 'exp-demo-1'
            },
            # {
            #     'id': 2,
            #     'hash': 'exp-demo-2'
            # },
            # {
            #     'id': 3,
            #     'hash': 'exp-demo-3'
            # }
        ]
        for data in plugins:
            self.__plugins_temp.append({
                'code': load_module('plugin' + str(data['id']),
                                    'http://scan.cn/static/py/plugins/' + data['hash'] + '.py'),
                'id': str(data['id'])
            })

    def __check_status(self, b, c):
        if self.is_suspend == 1:
            raise Exception('Scan Suspend ... Await Restart Scan')
        if self.is_stop == 1:
            raise Exception('Scan Exit')

    def send_scan_result(self, title, message, level):
        if level < 0 or level > 3:
            return [False, 'message level error']
        request_path = self.__server_gateway + '/api/v1/TaskMessage'
        # build request path
        request_result = tootls.curl(request_path, {
            'taskID': self.__scan_data['tid'],
            'token': self.__scan_data['token'],
            'target': self.__targets_data[0]['target_url'],
            'title': title,
            'message': message,
            'level': level
        }, {}, 'POST')
        try:
            json_data_temp = json.loads(request_result)
        except:
            return
        if json_data_temp['status'] == 1:
            return [True, '']
        else:
            return [False, json_data_temp['msg']]

    # 推送任务
    def task_push(self, service_list, target_url):
        self.__targets_data.append({
            'service_list': service_list,
            'target_url': target_url
        })

    def __run_plugins(self, data):
        data['code'].plugin_id = data['id']
        data['code'].send_scan_result = self.send_scan_result
        data['code'].task_push = self.task_push
        data['code'].tootls = tootls
        try:
            if data['code'].assign(self.__targets_data[0]['service_list']):
                data['code'].audit(
                    self.__targets_data[0]['target_url'],
                    self.__user_agent,
                    self.__cookie
                )
        except:
            print('error')
            pass
        # 这里写入服务名 进行判断是否需要下一步操作 避免不必要的扫描过程

        # 砍掉了暂停功能只留停止功能
        # self.__run_done_plugins_id.append(data['id'])
        # if data['id'] in self.__run_done_plugins_id:
        #     return
        # else:
        #     data['code'].audit(tootls, {
        #         self.__targets_data,
        #         self.__user_agent,
        #         self.__cookie
        #     }, self.send_scan_result)
        #     self.__run_done_plugins_id.append(data['id'])

    def __nmap_scan_target(self):
        nmap_scan_result = get_namp_scan_result(self.__targets_data[0]['target_url'],
                                                self.__scan_data['nmap_scan_args'])
        if len(nmap_scan_result) == 0:
            return
        for temp_data in nmap_scan_result:
            self.send_scan_result('Nmap scan result',
                                  temp_data['ip'] + ':' + temp_data['port'] + '   ' + temp_data['name'], 0)
            self.__targets_data[0]['service_list'].append(temp_data['name'].lower())
            # add service list

    def __push_target_service(self):
        if len(self.__targets_data[0]['service_list']) == 0:
            return
        for name in self.__targets_data[0]['service_list']:
            self.send_scan_result('Service Fingerprint Scan Result', name, 0)

    def run(self):
        isEnd = False
        print('[+] Start Scan Target !')
        while isEnd is False:
            self.__targets_data[0]['service_list'] = get_target_service(self.__targets_data[0]['target_url'],
                                                                        self.__user_agent, self.__cookie)
            # scan target service
            self.__nmap_scan_target()
            # nmap scan
            self.__push_target_service()
            # save Fingerprint Scan Result
            [self.__pool.putRequest(req) for req in self.__requests]
            try:
                self.__pool.wait()
            except Exception as err:
                print('[-] ' + str(err))
            self.__targets_data.pop(0)
            if len(self.__targets_data) == 0:
                isEnd = True
        print('[+] Scan Target Done !')
