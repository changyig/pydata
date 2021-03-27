import requests
import threading
import queue
import time
import json
from bs4 import BeautifulSoup
from redis_scrapy import RedisQueue

# 采集线程列表
crawl_thread_list = []
for i in range(20):
    crawl_thread_list.append(i)
# crawl_thread_list = ['采集线程1','采集线程2','采集线程3','采集线程4','采集线程5','采集线程6','采集线程7','采集线程8','采集线程9','采集线程10','采集线程11','采集线程12']
# 解析线程列表
parse_thread_list = []


class CrawlThread(threading.Thread):
    def __init__(self,name,redisqueue,queue_all,start_time):
        super().__init__()
        self.name = name
        self.redis_object = redisqueue
        self.queue_all = queue_all
        self.start_time = start_time
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
            'Connection':'close'
        }

    def run(self):
        print('%s开始采集数据....' % self.name)
        pre_url = None
        # 这里需要加循环让线程继续下去，不然执行一次之后就会停止
        while True:
            try:
                if pre_url:
                    url = pre_url
                else:
                    size = self.redis_object.qsize()
                    url = self.get_url_info_from_queue()
                    if size > 0:
                        pass
                    else:
                        print('当前采集器:{},数据已取完'.format(self.name))
                        break
                keyword_html = requests.get(url,timeout=10)
                if keyword_html.status_code == 200:
                    pre_url = None
                    keyword = BeautifulSoup(keyword_html.text,"html.parser")
                    title = keyword.title.string
                    progress = (self.queue_all - size) / self.queue_all
                    left_time = ((time.time() - self.start_time) / progress - (time.time() - self.start_time)) / 60
                    print('队列总个数：{}，剩余个数：{},当前进度：{}%,预计剩余时间：{}分钟'.format(self.queue_all,size,
                                                                         format(progress * 100,'.2f'),
                                                                         format(left_time,'.2f')))
                    print('当前采集器:{},当前title:{},当前url:{}'.format(self.name,title,url))
                    with open('./scrapy_data/www.vat69.cz.txt','a',encoding='utf8') as f:
                        f.write(title + '\n')
                else:
                    pre_url = url
                    print('当前采集器:{},休息10秒,当前url:{}'.format(self.name,pre_url))
                    time.sleep(10)
            except Exception as e:
                if self.redis_object.qsize() == 0:
                    print('当前采集器:{},无法获取数据'.format(self.name))
                    break
                else:
                    pre_url = url
                    print(e)
                    print('出现错误休眠10秒,当前url:{}'.format(pre_url))
                    time.sleep(10)

        print('%s结束采集数据....' % self.name)
    # 从队列中获取一个待下载的URL
    def get_url_info_from_queue(self):
        while True:
            url_info = self.redis_object.get_wait(10)
            if url_info is not None and len(url_info) >= 2:
                url_info = url_info[1]
                if url_info is not None:
                    return url_info
            return url_info

# 用该类操作多线程类
class Threadop:
    def start_thread(self):
        # 创建页码队列
        redisqueue = RedisQueue('keyword_url')
        qsize = redisqueue.qsize()
        for i in crawl_thread_list:
            download_thread = CrawlThread(i,redisqueue,qsize,time.time())
            download_thread.start()
        print(qsize)
        time.sleep(20)
        print('采集结束')
        pass
def main():
    # 创建页码队列
    redisqueue = RedisQueue('keyword_url')
    qsize = redisqueue.qsize()
    for i in crawl_thread_list:
        download_thread = CrawlThread(i,redisqueue,qsize,time.time())
        download_thread.start()
    print(qsize)
    time.sleep(20)
    print('采集结束')
    pass


if __name__ == "__main__":
    main()
