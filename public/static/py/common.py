import json
import threading
import time
from urllib import request

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


def login_server(server_gateway, uid, hash):
    banner()

    mac = tootls.get_mac_address()

    code, _, body, _, _ = tootls.curl2(server_gateway + '/api/v1/Login', {
        'mac': mac,
        'machineInfo': tootls.get_system_info(),
        'uid': uid,
        'hash': hash
    }, {}, 'post')

    if code != 200:
        print('[-] request server error')
        exit(500)

    login_result = json.loads(body)
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


def quit_server(server_gateway, lid, mac, uuid):
    code, _, body, _, _ = tootls.curl2(server_gateway + '/api/v1/Logout', {
        'mac': mac,
        'lid': lid,
        'uuid': uuid
    }, {}, 'post')

    if code != 200:
        print('[-] request server error, but logout success')
        exit(500)

    print('[-] logout success lid => ' + str(lid) + ' uuid => ' + uuid)


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

    __run_task_list = []
    __run_task_id_list = []

    def __init__(self, server_address, lid, uuid):
        threading.Thread.__init__(self)
        self.__lid = lid
        self.__uuid = uuid
        self.__mac = tootls.get_mac_address()
        self.__server_gateway = server_address

    # 设置任务状态 0 运行待运行 1 运行中 2 运行完成 3 终止运行
    def __set_task_status(self, task_id, status):
        if status == 2 or status == 1:
            request_url = self.__server_gateway + '/api/v1/TaskStatus'
            code, _, body, _, _ = tootls.curl2(request_url, {
                'lid': self.__lid,
                'mac': self.__mac,
                'uuid': self.__uuid,
                'taskID': task_id,
                'taskStatus': status
            }, None, 'post')
            if code != 200:
                print('[-] set task status error')
        if status == 2 or status == 3:
            temp_list = []
            for temp_data in self.__run_task_id_list:
                if task_id == temp_data:
                    continue
                temp_list.append(task_id)
            self.__run_task_id_list = temp_list
            # 删除任务id列表
            for temp_data in self.__run_task_list:
                if temp_data['id'] == task_id:
                    continue
                temp_list.append(temp_data)
            self.__run_task_list = temp_list
            # 删除任务列表数据

    # 获取任务信息
    def __get_task_info(self, task_id):
        request_url = self.__server_gateway + '/api/v1/TaskInfo'
        code, header, body, _, _ = tootls.curl2(request_url, {
            'lid': self.__lid,
            'mac': self.__mac,
            'uuid': self.__uuid,
            'taskID': task_id
        })
        if code != 200:
            print('[-] get task info error')
            exit(500)
        try:
            body = json.loads(body)
        except:
            print('[-] task info info error ,pls reload program')
            exit(500)
        if body['status'] != 1:
            print('[-] task info get error,' + body['msg'])
            exit(500)
        return body['data']

    def run(self):
        while True:
            if len(self.__run_task_id_list) == 0:
                machine_status = 1
            else:
                machine_status = 2
            # 如果执行中的任务列表为空
            heart_beat_result = heart_beat_request(self.__server_gateway, self.__lid, self.__uuid, machine_status)
            if heart_beat_result['status'] != 1:
                time.sleep(5)
                continue
            # 当心跳数据异常
            if len(heart_beat_result['taskList']) != 0:
                for task_info in heart_beat_result['taskList']:
                    if task_info['status'] == 0:
                        if task_info['id'] in self.__run_task_id_list:
                            pass
                        # 如果线程在运行则不运行
                        else:
                            threader = scan_main_threading(self.__server_gateway, self.__get_task_info(task_info['id']))
                            threader.set_task_status = self.__set_task_status
                            threader.setDaemon(True)
                            threader.start()
                            self.__run_task_list.append({
                                'id': task_info['id'],
                                'thread': threader
                            })
                            self.__run_task_id_list.append(task_info['id'])
                            # 设置任务运行状态
                        # 不在运行列表就运行
                    # 需要运行线程
                    if task_info['status'] == 3:
                        if task_info['id'] in self.__run_task_id_list:
                            for task_data in self.__run_task_list:
                                if task_data['id'] == task_info['id']:
                                    task_data['thread'].is_stop = True
                        else:
                            pass
                    # 停止线程
            time.sleep(2)


class scan_main_threading(threading.Thread):
    __pool = None
    __request = None

    __plugins_temp = []
    # __run_done_plugins_id = []
    __targets_data = []
    __server_gateway = ''
    __scan_data = {}

    __task_id = 0

    def __init__(self, server_gateway, task_info):
        threading.Thread.__init__(self)

        # self.is_suspend = False
        self.is_stop = False
        # 这两个参数控制暂停与停止
        self.__server_gateway = server_gateway

        self.__targets_data.append({
            'target_url': task_info['target_url']
        })
        self.__scan_data = task_info
        self.__task_id = task_info['taskID']

        # self.__run_done_plugins_id = []
        # 这个参数用来存储已经完成的插件ID 用于暂停后恢复线程 并且不会假死
        self.__load_plugins()
        # 加载插件列表
        self.__pool = threadpool.ThreadPool(task_info['plugins_thread_num'])
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
        # if self.is_suspend == 1:
        #     raise Exception('Scan Suspend ... Await Restart Scan')
        if self.is_stop == 1:
            raise Exception('Scan Exit')

    def send_scan_result(self, title, message, level):
        if level < 0 or level > 3:
            return [False, 'message level error']
        request_path = self.__server_gateway + '/api/v1/TaskMessage'
        # build request path
        request_result = tootls.curl(request_path, {
            'taskID': self.__scan_data['taskID'],
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

    def curl(self, url=None, request_data=None, headers=None, request_type=None, proxy=None, timeout=3):
        if headers is None:
            headers = {
                'user-agent': self.__scan_data['userAgent'],
                'cookie': self.__scan_data['cookie']
            }
        if proxy is None and self.__scan_data['proxy'] is not None:
            if self.__scan_data['proxy']['type'] == 'http':
                proxy = request.ProxyHandler(
                    {'http': self.__scan_data['proxy']['ip'] + ':' + str(self.__scan_data['proxy']['port'])})
        return tootls.curl2(url, request_data, headers, request_type, proxy, timeout)

    def __run_plugins(self, data):
        data['code'].plugin_id = data['id']
        data['code'].send_scan_result = self.send_scan_result
        data['code'].task_push = self.task_push
        data['code'].tootls = tootls
        data['code'].curl = self.curl

        if data['code'].assign(self.__targets_data[0]['service_list']):
            data['code'].audit(
                self.__targets_data[0]['target_url'],
                self.__scan_data['userAgent'],
                self.__scan_data['cookie']
            )
        # try:
        #     if data['code'].assign(self.__targets_data[0]['service_list']):
        #         data['code'].audit(
        #             self.__targets_data[0]['target_url'],
        #             self.__scan_data['userAgent'],
        #             self.__scan_data['cookie']
        #         )
        # except:
        #     pass
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
        self.set_task_status(self.__task_id, 1)
        print('[+] Start Scan Target !')
        while isEnd is False:
            self.__targets_data[0]['service_list'] = get_target_service(self.__targets_data[0]['target_url'],
                                                                        self.__scan_data['userAgent'],
                                                                        self.__scan_data['cookie'])
            # scan target service
            self.__nmap_scan_target()
            # nmap scan
            self.__push_target_service()
            # save Fingerprint Scan Result
            [self.__pool.putRequest(req) for req in self.__requests]
            try:
                self.__pool.wait()
            except Exception as err:
                self.set_task_status(self.__task_id, 3)
                print('[-] ' + str(err))
            self.__targets_data.pop(0)
            if len(self.__targets_data) == 0:
                isEnd = True
        print('[+] Scan Target Done !')
        self.set_task_status(self.__task_id, 2)
