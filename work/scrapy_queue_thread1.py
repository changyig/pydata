import requests
import threading
import queue
import time
# from lxml import etree
import json
from bs4 import BeautifulSoup

# 采集线程列表
crawl_thread_list = []
# 解析线程列表
parse_thread_list = []
class CrawlThread(threading.Thread):
    def __init__(self, name, page_queue, data_queue,queue_all,start_time):
        super().__init__()
        self.name = name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.queue_all = queue_all
        self.start_time = start_time
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
            }

    def run(self):
        print('%s开始采集数据....' % self.name)
        # 这里需要加循环让线程继续下去，不然执行一次之后就会停止
        while True:
            if not self.page_queue.empty():
                # url = url.format(self.page_queue.get())
                url = self.page_queue.get()
                print(self.name)
            else:
                # print('数据已取完')
                break
            keyword_html = requests.get(url)
            keyword = BeautifulSoup(keyword_html.text, "html.parser")
            title = keyword.title.string
            progress=(self.queue_all-self.page_queue.qsize())/self.queue_all
            left_time=((time.time()-self.start_time)/progress-(time.time()-self.start_time))/60
            print('队列总个数：{}，剩余个数：{},当前进度：{}%,预计剩余时间：{}分钟'.format(self.queue_all,self.page_queue.qsize(),format(progress*100,'.2f'),format(left_time,'.2f')))
            print('当前title:{}'.format(title))
            with open('test.txt', 'a', encoding='utf8') as f:
                f.write(title+'\n')
        print('%s结束采集数据....' % self.name)
def creat_crawl_thread(page_queue, data_queue,queue_all,start_time):
    crawl_name_list = ['采集线程1', '采集线程2', '采集线程3', '采集线程4', '采集线程5', '采集线程6', '采集线程7', '采集线程8']
    for name in crawl_name_list:
        crawl_thread = CrawlThread(name, page_queue, data_queue,queue_all,start_time)
        crawl_thread_list.append(crawl_thread)

def main():
    # 创建页码队列
    page_queue = queue.Queue()
    # 给队列添加页码
    filename = '../data/url/url1.txt'
    file_handle = open(filename, mode='r', encoding='utf-8')
    for line in file_handle.readlines():
        page_queue.put(line.strip())
    queue_all=page_queue.qsize()
    # 创建锁
    # lock = threading.Lock()
    # 创建采集数据线程
    data_queue = queue.Queue()
    start_time=time.time()
    creat_crawl_thread(page_queue, data_queue,queue_all,start_time)
    for cthread in crawl_thread_list:
        cthread.start()

    time.sleep(3)
    # 主线程等待子线程结束
    # cthread.join()
    print('主线程结束....')
    # 关闭文件
    # fp.close()
if __name__ == "__main__":
    main()
    # read_text()