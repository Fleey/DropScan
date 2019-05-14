import json
import threading

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
        login_result['lid']) + ', MAC => ' + mac)

    return {
        'lid': login_result['lid'],
        'mac': mac
    }


def get_target_service(target, user_agent='', cookie=''):
    print('[+] load service fingerprint dict ...')
    service_fingerprint_dict = json.loads(tootls.curl('http://scan.cn/static/py/resources/Feature.json', {}, {}))
    print('[+] load service fingerprint ok !')

    print('[+] start service fingerprint target => ' + target)

    scan_service = scanService.scanService(target, service_fingerprint_dict, user_agent=user_agent, cookie=cookie)
    result = scan_service.scan_domain()
    print('[+] end service fingerprint target => ' + target)
    return result


def heart_beat_request(server_address, lid, status):
    data = tootls.curl(server_address + '/api/v1/Heartbeat', {
        'lid': lid,
        'status': status,
        'mac': tootls.get_mac_address()
    }, {}, 'POST')
    if len(data) == 0:
        print('[-][HeartBeat] request network error')
        exit(500)
    data = json.loads(data)
    if data['status'] != 1:
        print('[-][HeartBeat] request error info => ' + data['msg'])
    return data


class heart_beat_threading(threading.Thread):
    __lid = None
    __mac = None
    __server_gateway = None
    __service_fingerprint_dict = []

    def __init__(self, server_address, lid):
        threading.Thread.__init__(self)
        self.__lid = lid
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

        threader = scan_main_threading(
            self.__server_gateway,
            target,
            1,
            {
                'token': 'hk585KIHvEwFtvRkvMN8uDsYgKeJIdev',
                'tid': 2
            }, get_target_service(target),
            ua, cookie)
        threader.start()

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
    __run_done_plugins_id = []
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
    def __init__(self, server_gateway, target_url, thread_num, scan_data, service_list=[], user_agent='',
                 cookie='test'):
        threading.Thread.__init__(self)

        self.is_suspend = False
        self.is_stop = False
        # 这两个参数控制暂停与停止

        self.user_agent = user_agent
        self.__cookie = cookie
        self.__targets_data.append({
            'service_list': service_list,
            'target_url': target_url
        })
        self.__server_gateway = server_gateway
        self.__scan_data = scan_data

        self.__run_done_plugins_id = []
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
        if level <= 0 or level > 3:
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

    def run(self):
        isEnd = False
        print('[+] Start Scan Target !')
        while isEnd is False:
            [self.__pool.putRequest(req) for req in self.__requests]
            try:
                self.__pool.wait()
            except Exception as err:
                print('[-] ' + str(err))
            self.__targets_data.pop(0)
            if len(self.__targets_data) == 0:
                isEnd = True
        print('[+] Scan Target Done !')
