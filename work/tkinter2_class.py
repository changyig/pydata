import tkinter as tk
from redis_scrapy import RedisQueue
from scrapy_class import Scrapy
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
        self.show = tk.Button(text="展示",fg="red",
                              command=self.setlabel)
        self.show.grid(row=1,column=3,padx=5, pady=5)

        #展示区
        # self.label_text = tk.StringVar()
        # self.label_text.set("----")
        # self.lable = tk.Label(
        #                       textvariable=self.label_text,
        #                       font=('Arial',11),width=15,height=2)
        # self.lable.grid(row=3,column=0)

        #展示区
        self.show=tk.Text()
        self.show.grid(row=4, rowspan=5,columnspan=5)
        self.show_text()
        # #结束按钮
        # self.quit = tk.Button(text="QUIT",fg="red",
        #                       command=self.master.destroy)
        # self.quit.grid(row=10,column=0)

    def say_hi(self):
        redis_object=RedisQueue('keyword_url')
        size=redis_object.qsize()
        print(size)

    def run_scapy(self):
        sitemap=self.sitemap.get()
        self.show_text(sitemap)
        scrapy = Scrapy()
        print(scrapy)
        flag=scrapy.run_sitemap(sitemap)
        if flag:
            self.show_text('站点地图获取完成')


    def setlabel(self):
        print(self.sitemap)
        self.content=self.sitemap
        flag=self.label_text.set(self.content)
        if flag:
            self.show_text('结束')

    def show_text(self,content=''):
        self.show.insert(tk.INSERT,str(content)+'\n')


root = tk.Tk()
app = Application(master=root)
app.mainloop()