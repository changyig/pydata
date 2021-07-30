# -*- coding: utf-8 -*-

import requests
import random
import json
from hashlib import md5

class BaiduApi(object):
    def __init__(self):
        self.appid='20210511000822216'
        self.appkey='np72c9X6g4dFaflFPU3I'
        self.from_lang = 'en'
        self.to_lang =  'ara'#ara zh  ru
    def start(self,content=''):
        try:
            return_list=[]
            url='http://api.fanyi.baidu.com/api/trans/vip/translate'
            salt = random.randint(32768,65536)
            # content = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
            md5_str = (self.appid + content + str(salt) + self.appkey)
            sign=md5(md5_str.encode('utf-8')).hexdigest()
            # Build request
            headers = {'Content-Type':'application/x-www-form-urlencoded'}
            payload = {'appid':self.appid,'q':content,'from':self.from_lang,'to':self.to_lang,'salt':salt,'sign':sign}

            # Send request
            r = requests.post(url,params=payload,headers=headers)
            result = r.json()
            python_data=json.loads(json.dumps(result,indent=4,ensure_ascii=False))
            print(python_data['trans_result'])
            for onelist in python_data['trans_result']:
                # print(onelist['dst'])
                return_list.append(onelist['dst'])
            return return_list
        except Exception as e:
            print(e)
            return []

if __name__=='__main__':

    TextObject=BaiduApi()
    TextObject.start()