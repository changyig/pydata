import threading
from queue import Queue
CRAWL_EXIT = False
class ThreadCrawl(threading.Thread):
    def __init__(self, thread_name, page_queue, data_queue):
        # threading.Thread.__init__(self)
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        self.threadName = thread_name
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        print(self.threadName + ' 启动************')
        while not CRAWL_EXIT:
            try:
                header={
                    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
                }
                # 队列为空 产生异常
                page = self.page_queue.get(block=False)
                print(page)
            except:
                print(self.threadName)
                break

def main():
    # 声明一个队列，使用循环在里面存入100个页码
    page_queue  = Queue(100)
    for i in range(1,101):
        page_queue.put(i)

    # 采集结果(等待下载的图片地址)
    data_queue = Queue()

    # 记录线程的列表
    thread_crawl = []
    # 每次开启4个线程
    craw_list = ['采集线程1号','采集线程2号','采集线程3号','采集线程4号']
    for thread_name in craw_list:
        c_thread = ThreadCrawl(thread_name, page_queue, data_queue)
        c_thread.start()
        thread_crawl.append(c_thread)

    # 等待page_queue队列为空，也就是等待之前的操作执行完毕
    while not page_queue.empty():
        global CRAWL_EXIT
        CRAWL_EXIT = True
        pass

if __name__ == '__main__':
    main()
