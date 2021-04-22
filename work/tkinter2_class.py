import tkinter as tk
from redis_scrapy import RedisQueue
from scrapy_class import Scrapy
from redis_queue_thread import Threadop
import re
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sitemap = tk.StringVar()
        self.master = master
        self.master.geometry('500x500')
        self.create_widgets()


    def create_widgets(self):

        # self.hi_there = tk.Button(text="Hello World (click me)",command=self.say_hi)
        # self.hi_there.grid(row=0,column=0)
        #站点地图输入框
        tk.Label(text='输入框').grid(row=1,column=0)
        E1 = tk.Entry(bd=5,textvariable=self.sitemap)
        E1.grid(row=1,column=1)
        self.submit = tk.Button(text='自动化获取',command=self.run_scapy)
        self.submit.grid(row=1,column=2)

        #输入框按钮
        self.show = tk.Button(text="展示",fg="red",command=self.setlabel)
        self.show.grid(row=1,column=3,padx=5, pady=5)

        #展示区
        # self.label_text = tk.StringVar()
        # self.label_text.set("----")
        # self.lable = tk.Label(
        #                       textvariable=self.label_text,
        #                       font=('Arial',11),width=15,height=2)
        # self.lable.grid(row=3,column=0)

        #redis框按钮
        self.redis_read = tk.Button(text="读取redis数量",fg="red",command=self.read_redis)
        self.redis_read.grid(row=2,column=1,padx=5,pady=5)
        self.redis_del = tk.Button(text="清空redis数量",fg="red",command=self.del_redis)
        self.redis_del.grid(row=2,column=2,padx=5,pady=5)
        #展示区
        self.show=tk.Text()
        self.show.grid(row=4, rowspan=5,columnspan=5)
        self.show_text()
        # #结束按钮
        # self.quit = tk.Button(text="QUIT",fg="red",
        #                       command=self.master.destroy)
        # self.quit.grid(row=10,column=0)

    # 读取redis数量
    def read_redis(self):
        redis_object=RedisQueue('keyword_url')
        size=redis_object.qsize()
        print(size)
        self.show_text('redis数据库总数量:{}'.format(size))
    # 清空redis数量
    def del_redis(self):
        redis_object=RedisQueue('keyword_url')
        redis_object.delete('keyword_url')
        self.read_redis()
    # 开始运行程序 过程  sitemap的解析--》存入txt--》读取txt存redis--》运行爬虫程序
    def url_para(self,sitemap=''):

        pattern = re.compile(r'http[s]?://(.*)/(.*\.xml)',re.I)
        res2 = pattern.findall(sitemap)
        if res2:
            return str(res2[0][0])
        else:
            return ''
    def run_scapy(self):
        redis_object = RedisQueue('keyword_url')
        sitemap=self.sitemap.get()
        sitename=self.url_para(sitemap)
        self.show_text(sitemap)
        scrapy = Scrapy()
        print(scrapy)
        flag=scrapy.run_sitemap(sitemap)
        if flag:
            self.show_text('站点地图获取完成')
            self.del_redis()
            redis_object.read_text_redis()
            self.read_redis()
            thread_object=Threadop()
            thread_object.start_thread(sitename)


    def setlabel(self):
        print(self.sitemap)
        self.content=self.sitemap
        flag=self.label_text.set(self.content)
        if flag:
            self.show_text('结束')
            self.read_redis()

    def show_text(self,content=''):
        self.show.insert(tk.INSERT,str(content)+'\n')


root = tk.Tk()
app = Application(master=root)
app.mainloop()