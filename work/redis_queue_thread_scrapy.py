import requests
import threading
import queue
import time
import json
from bs4 import BeautifulSoup
from redis_scrapy import RedisQueue
from lxml import etree
from mysql_class import Mysql
import re
# 采集线程列表
crawl_thread_list = []
for i in range(1):
    crawl_thread_list.append(i)
# crawl_thread_list = ['采集线程1','采集线程2','采集线程3','采集线程4','采集线程5','采集线程6','采集线程7','采集线程8','采集线程9','采集线程10','采集线程11','采集线程12']
# 解析线程列表
parse_thread_list = []

'''
 说明：根据redis里面的链接地址 抓取中文网站 并存入相应的数据当中
 流程：读取redis地址-->线程爬虫-->页面解析-->存入数据库
'''
class CrawlThread(threading.Thread):
    def __init__(self,name,redisqueue,queue_all,start_time,mysql=None):
        super().__init__()
        self.name = name
        self.redis_object = redisqueue
        self.queue_all = queue_all
        self.start_time = start_time

        self.mysql = mysql
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
                    data=self.get_content_page(keyword_html)
                    # print(data)
                    if data:
                        self.insert_mysql(data,url)
                    else:
                        print('当前采集器:{},休息10秒,当前url:{}'.format(self.name,pre_url))
                        time.sleep(10)
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
    def get_content_page(self,html=''):
        try:
            html = html.content.decode('utf8')
            tree = etree.HTML(html)
            title = tree.xpath("//h1/text()")
            content_list = tree.xpath(
                "//div[@class='news-left']/*[not(contains(@class,'news-art1')) and not(contains(@class,'show-msg')) and not(contains(@class,'xg-news'))]//text()")
            content = ''.join(content_list)
            title = ''.join(title)
            if title and content:
                return [title,content]
        except Exception as e:
            print(e)
            return None
    def insert_mysql(self,data,url):
        try:
            print(self.mysql,data,url)
            page=0
            pattern = re.compile(r'\d+',re.I)
            digital = pattern.findall(url)
            if digital:
                page=int(digital[0])
            data=[{'page':page},{'title':data[0]},{'answer':data[1]},{'url':url}]
            print(data)
            res=self.mysql.table('sitemap_scrapy_zh').insert(data)
            print(res)
            print('数据插入成功')
        except Exception as e:
            print(e)
    # 从队列中获取一个待下载的URL
    def get_url_info_from_queue(self):
        while True:
            url_info = self.redis_object.get_wait(10)
            if url_info is not None and len(url_info) >= 2:
                url_info = url_info[1]
                if url_info is not None:
                    return url_info
            return url_info


def main():
    # 创建页码队列
    redisqueue = RedisQueue('keyword_url')
    qsize = redisqueue.qsize()
    mysql=Mysql()
    for i in crawl_thread_list:
        download_thread = CrawlThread(i,redisqueue,qsize,time.time(),mysql)
        download_thread.start()
    print(qsize)
    time.sleep(20)
    print('采集结束')
    pass


if __name__ == "__main__":
    main()
