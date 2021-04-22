import tkinter as tk
import threading
import time
import sys
import re
from redis_queue_thread import Threadop
from redis_scrapy import RedisQueue
from scrapy_class import Scrapy
# 读取redis数量
def read_redis():
    redis_object = RedisQueue('keyword_url')
    size = redis_object.qsize()
    print(size)
def fmtTime(timeStamp):
    timeArray = time.localtime(timeStamp)
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
    return dateTime

class re_Text():
    def __init__(self,widget):
        self.widget = widget
    def write(self,content):
        self.widget.insert(tk.INSERT,content)
        self.widget.see(tk.END)


class GUI():
    def __init__(self,root):
        self.sitemap = tk.StringVar()
        self.initGUI(root)
    def initGUI(self,root):
        root.title("gui")
        root.geometry("800x800")
        root.resizable = True
        # 第一排
        tk.Label(text='输入框').grid(row=1,column=0)
        E1 = tk.Entry(bd=5,textvariable=self.sitemap)
        E1.grid(row=1,columnspan=5)
        self.start = tk.Button(root,text='自动化获取',command=self.start)
        self.start.grid(row=1,column=6)
        # 第二排
        self.button_test = tk.Button(root,text='测试',command=self.show)
        self.button_test.grid(row=2,column=7)
        self.read_redis = tk.Button(root,text='读取redis',command=self.read_redis)
        self.read_redis.grid(row=2,column=0)
        self.clear_redis = tk.Button(root,text='清空redis',command=self.del_redis)
        self.clear_redis.grid(row=2,column=2)

        # 文本展示框
        # self.text_show =  tk.Text(root,yscrollcommand=self.scrollBar.set)
        self.text_show =  tk.Text(root)
        self.text_show.grid(row=4, rowspan=5,columnspan=5)
        self.scrollBar = tk.Scrollbar(root,orient='vertical',command=self.text_show.yview)
        # self.scrollBar.grid(row=4,rowspan=20,column=7)
        self.scrollBar.grid(row=4,column=6,rowspan=5,sticky=tk.S + tk.W + tk.E + tk.N)
        self.text_show.config(yscrollcommand=self.scrollBar.set)
        sys.stdout = re_Text(self.text_show)
        root.mainloop()

    # 开始运行程序 过程  sitemap的解析--》存入txt--》读取txt存redis--》运行爬虫程序
    def url_para(self,sitemap=''):

        pattern = re.compile(r'http[s]?://(.*)/(.*\.xml)',re.I)
        res2 = pattern.findall(sitemap)
        if res2:
            return str(res2[0][0])
        else:
            return ''
    def __show(self):
        i = 0
        while i<3:
            print(fmtTime(time.time()))
            time.sleep(1)
            i += 1
    def show(self):
        T = threading.Thread(target=self.__show,args=())
        T.start()

    # 清空redis数量
    def del_redis(self):
        redis_object = RedisQueue('keyword_url')
        redis_object.delete('keyword_url')
        read_redis()

    # 读取redis数量
    def read_redis(self):
        read_redis()
    def __run_sitemap(self):
        redis_object = RedisQueue('keyword_url')
        sitemap = self.sitemap.get()
        sitename = self.url_para(sitemap)
        print(sitename)
        scrapy = Scrapy()
        flag = scrapy.run_sitemap(sitemap)
        if flag:
            print('站点地图获取完成')
            self.del_redis()
            redis_object.read_text_redis()
            self.read_redis()
            thread_object = Threadop()
            thread_object.start_thread(sitename)
    '''
    说明：多线程开启站点地图抓取
    '''
    def start(self):
        T = threading.Thread(target=self.__run_sitemap,args=())
        T.start()

        # flag = scrapy.run_sitemap(sitemap)

if __name__ == "__main__":

    root = tk.Tk()
    myGUI = GUI(root)
