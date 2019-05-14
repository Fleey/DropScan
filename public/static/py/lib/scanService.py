import re
from urllib import request

class scanService:
    __temp_dict = {}
    __service_fingerprint_dict = []
    __success_record = {}
    __target = ''
    __head = {}
    __timeout = 2

    def __init__(self, target, service_fingerprint_dict, user_agent='DorpScan v1.0.0', cookie='', timeout=3):
        self.__target = target
        self.__service_fingerprint_dict = service_fingerprint_dict
        self.__head = {
            'User-Agent': user_agent,
            'cookie': cookie
        }
        self.__timeout = timeout

    def scan_domain(self):
        self.__scan_domain()
        return self.__get_scan_data()

    def __scan_domain(self):
        for data in self.__service_fingerprint_dict:
            result = self.__get_web_file_md5(self.__target + data['url'])
            if result[0] is False:
                continue
            data['name'] = data['name'].lower()
            if data['type'] == 1:
                data['content'] = data['content'].lower()
                if data['content'] != result[0]:
                    continue
            else:
                str_content = ''
                for header in result[2]:
                    str_content += header[0] + ': ' + header[1] + '\n'

                if result[3] is not False:
                    str_content += result[3]

                if data['type'] == 2:
                    if str_content.find(data['content']) == -1:
                        continue
                # 普通搜索字符串模式
                if data['type'] == 3:
                    pattern = data['content']
                    try:
                        match = re.search(pattern, str_content, re.IGNORECASE)
                        if match is None:
                            continue
                    except:
                        continue

            if data['name'] in self.__success_record:
                self.__success_record[data['name']]['count'] += 1
            else:
                self.__success_record[data['name']] = {
                    'count': 1,
                    'name': data['name']
                }

    def __get_web_file_md5(self, url):
        if url in self.__temp_dict:
            if self.__temp_dict[url]['is_exist']:
                return [self.__temp_dict[url]['hash'], True, self.__temp_dict[url]['headers'],
                        self.__temp_dict[url]['content']]
            else:
                return [False, False, False, False]
        try:
            temp_response = request.Request(url, headers=self.__head)

            response = request.urlopen(temp_response, timeout=self.__timeout)
            headers = response.getheaders()
            data = response.read()
            file_hash = tootls.get_md5_value(data)

            try:
                data = data.decode('utf-8')
            except:
                data = False

            self.__temp_dict[url] = {
                'is_exist': True,
                'hash': file_hash,
                'headers': headers,
                'content': data
            }
            return [file_hash, True, headers, data]
        except:
            self.__temp_dict[url] = {
                'is_exist': False
            }
            return [False, False, False, False]

    # 获取一坨可能的系统指纹
    def __get_scan_data(self):
        temp_data = []
        for str1 in self.__success_record:
            value = self.__success_record[str1]
            temp_data.append(value['name'])
        return temp_data

    # 获取最可能的那个系统 容错率比较低
    def __get_filter_data(self):
        temp_data = {
            "name": "未知系统",
            "count": 0
        }
        for str1 in self.__success_record:
            value = self.__success_record[str1]
            if temp_data["name"] == value["name"]:
                continue
            if temp_data["count"] < value["count"]:
                temp_data = value

        return temp_data["name"]
