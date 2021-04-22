import tkinter as tk
import threading
import time
import sys
import re
from text_class import TextObject
from tkinter import filedialog
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
        self.txt_path = r''
        self.initGUI(root)
    def initGUI(self,root):
        root.title("gui")
        root.geometry("800x800")
        root.resizable = True
        # 第一排 选择按钮
        self.txt_open = tk.Button(root,text='打开txt文件',command=self.start)
        self.txt_open.grid(row=1,column=2)
        self.txt_split = tk.Button(root,text='处理txt文件',command=self.handel_txt)
        self.txt_split.grid(row=1,column=4)
        # 第二排

        # 文本展示框
        # self.text_show =  tk.Text(root,yscrollcommand=self.scrollBar.set)
        self.text_show =  tk.Text(root)
        self.text_show.grid(row=4, rowspan=5,columnspan=5)
        self.scrollBar = tk.Scrollbar(root,orient='vertical',command=self.text_show.yview)
        # self.scrollBar.grid(row=4,rowspan=20,column=7)
        self.scrollBar.grid(row=4,column=6,rowspan=5,sticky=tk.S + tk.W + tk.E + tk.N)
        self.text_show.config(yscrollcommand=self.scrollBar.set)
        sys.stdout = re_Text(self.text_show)

        #功能按钮区
        self.CheckVar1 = tk.IntVar()
        self.CheckVar2 = tk.IntVar()
        self.CheckVar3 = tk.IntVar()
        self.CheckVar4 = tk.IntVar()
        self.ch1 = tk.Checkbutton(root,text='文本转换',            variable=self.CheckVar1,onvalue=1,offvalue=0,command=self.check_button)
        self.ch2 = tk.Checkbutton(root,text='过滤特殊字符',      variable=self.CheckVar2,onvalue=1,offvalue=0,command=self.check_button)
        self.ch3 = tk.Checkbutton(root,text='去除重复度高的',    variable=self.CheckVar3,onvalue=1,offvalue=0,command=self.check_button)
        self.ch4 = tk.Checkbutton(root,text='分割',            variable=self.CheckVar4,onvalue=1,offvalue=0,command=self.check_button)
        self.ch1.grid(row=10,column=1)
        self.ch2.grid(row=11,column=1)
        self.ch3.grid(row=12,column=1)
        self.ch4.grid(row=13,column=1)

        #功能按钮区
        self.start = tk.Button(root,text='开始执行',command=self.start)
        self.start.grid(row=14,column=6)
        root.mainloop()
    def check_button(self):
        list_data=[self.CheckVar1,self.CheckVar2,self.CheckVar3,self.CheckVar4]
        dicts_data = {0:'文本转换',1:'过滤特殊字符',2:'去除重复度高的',3:'分割'}
        for index,list in enumerate(list_data):
            # print(list)
            list_data[index]=list.get()
        # print(list_data)
        message_info='选中的功能区为：'
        for index ,d in dicts_data.items():
            # [ list_data[i]==1  for i ,d in dicts_data.items()]
            if list_data[index]==1:
                message_info=message_info+','+d
        print(message_info)
    # 开始运行程序 过程  sitemap的解析--》存入txt--》读取txt存redis--》运行爬虫程序
    def url_para(self,sitemap=''):

        pattern = re.compile(r'http[s]?://(.*)/(.*\.xml)',re.I)
        res2 = pattern.findall(sitemap)
        if res2:
            return str(res2[0][0])
        else:
            return ''
    def __handel_txt(self):
        txtObject=TextObject()
    def handel_txt(self):
        T = threading.Thread(target=self.__handel_txt,args=())
        T.start()


    def __run_sitemap(self):
        # s2fname = filedialog.askopenfilename(title='打开S2文件',filetypes=[('S2out','*.out'),('All Files','*')])
        s2fname = filedialog.askopenfilename(title='打开S2文件',filetypes=[('txt','*.txt')])
        self.txt_path=s2fname
        print('文件地址为:{}'.format(self.txt_path))
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
