import requests
import threading
import queue
import time
# from lxml import etree
import json

# 采集线程列表
crawl_thread_list = []
# 解析线程列表
parse_thread_list = []


class CrawlThread(threading.Thread):
    def __init__(self, name, page_queue, data_queue):
        super().__init__()
        self.name = name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
            }

    def run(self):
        print('%s开始采集数据....' % self.name)
        # 这里需要加循环让线程继续下去，不然执行一次之后就会停止
        while True:
            # 获取页码队列中的数据，拼接url
            url = 'http://www.ifanjian.net/jianwen-{}'
            # 判断队列是否为空
            if not self.page_queue.empty():
                url = url.format(self.page_queue.get())
                # print(url)
            else:
                # print('数据已取完')
                break
            # 发送请求
            r = requests.get(url, headers=self.headers)
            # print('请求url----------------------------------------', r.url)
            # self.fp1.write(r.text)
            # 将数据添加到数据队列
            self.data_queue.put(r.text)
            # print(self.data_queue.qsize())
            # print(self.data_queue.get())
        print('%s结束采集数据....' % self.name)


class ParseThread(threading.Thread):
    def __init__(self, name, data_queue, lock, fp):
        super().__init__()
        self.name = name
        self.data_queue = data_queue
        self.lock = lock
        self.fp = fp

    def run(self):

        items = []
        print('{}开始解析数据...'.format(self.name))
        while self.data_queue.qsize() != 0:
            # 从队列中获取数据
            content = self.data_queue.get()
            print(content)
            # 解析数据
            # tree = etree.HTML(content)
            time.sleep(1)
            # 获取标题
        print('{}结束解析数据...'.format(self.name))


def creat_crawl_thread(page_queue, data_queue):
    crawl_name_list = ['采集线程1', '采集线程2', '采集线程3']
    for name in crawl_name_list:
        crawl_thread = CrawlThread(name, page_queue, data_queue)
        crawl_thread_list.append(crawl_thread)


def creat_parse_thread(data_queue, lock, fp):
    parse_name_list = ['解析线程1', '解析线程2', '解析线程3']
    for name in parse_name_list:
        parse_thread = ParseThread(name, data_queue, lock, fp)
        parse_thread_list.append(parse_thread)


def main():
    # 创建页码队列
    page_queue = queue.Queue()
    # 给队列添加页码
    for page in range(1, 51):
        page_queue.put(page)
    # 创建数据队列
    data_queue = queue.Queue()
    # 创建锁
    lock = threading.Lock()
    # 创建文件
    # fp = open('Reptile/fanjian.json', 'a', encoding='utf8')
    fp = open('fanjian.txt', 'a', encoding='utf8')
    # 创建采集数据线程
    creat_crawl_thread(page_queue, data_queue)
    # 创建解析数据线程
    creat_parse_thread(data_queue, lock, fp)

    # 启动采集数据线程
    for cthread in crawl_thread_list:
        cthread.start()

    time.sleep(3)
    # 启动解析数据线程
    for pthread in parse_thread_list:
        pthread.start()

    # 主线程等待子线程结束
    cthread.join()
    pthread.join()

    print('主线程结束....')
    # 关闭文件
    # fp.close()


if __name__ == "__main__":
    main()