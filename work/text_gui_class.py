import tkinter as tk
import threading
import time
import sys
import re
from text_class import TextObject
from tkinter import filedialog

def fmtTime(timeStamp):
    timeArray = time.localtime(timeStamp)
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
    return dateTime

class re_Text():
    def __init__(self,widget):
        self.widget = widget
    def write(self,content):
        # self.widget.delete('1.0', tk.END)
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
        self.time_box = tk.Label(root,text='时间')
        self.time_box.grid(row=1,column=1)
        self.txt_open = tk.Button(root,text='打开txt文件',command=self.import_txt)
        self.time_run()
        self.txt_open.grid(row=1,column=2)
        self.txt_split = tk.Button(root,text='处理txt文件',command=self.handel_txt)
        self.txt_split.grid(row=1,column=4)
        # 第二排

        # 文本展示框
        # self.text_show =  tk.Text(root,yscrollcommand=self.scrollBar.set)
        # self.text_show =  tk.Text(root,bg='black',fg='white')
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
        self.split_num=tk.StringVar()
        self.split_num.set(2)
        self.split_num_box = tk.Entry(root, textvariable=self.split_num)
        self.ch1.grid(row=10,column=1)
        self.ch2.grid(row=11,column=1)
        self.ch3.grid(row=12,column=1)
        self.ch4.grid(row=13,column=1)
        self.split_num_box.grid(row=13,column=2)

        #功能按钮区
        self.start = tk.Button(root,text='开始执行',command=self.start)
        self.start.grid(row=14,column=6)
        root.mainloop()
    def time_run(self):
        timestr = time.strftime("%H:%M:%S") # 获取当前的时间并转化为字符串
        self.time_box.configure(text=timestr)   # 重新设置标签文本
        root.after(1000,self.time_run) # 每隔1s调用函数 gettime 自身获取时间
    def check_button(self):
        list_data=[self.CheckVar1,self.CheckVar2,self.CheckVar3,self.CheckVar4]
        dicts_data = {0:'文本转换',1:'过滤特殊字符',2:'去除重复度高的',3:'分割'}
        for index,list in enumerate(list_data):
            list_data[index]=list.get()
        message_info='选中的功能区为：'
        for index ,d in dicts_data.items():
            if list_data[index]==1:
                message_info=message_info+','+d
        print(message_info)
        return list_data

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
    def __import_txt(self):
        # s2fname = filedialog.askopenfilename(title='打开S2文件',filetypes=[('S2out','*.out'),('All Files','*')])
        s2fname = filedialog.askopenfilename(title='打开S2文件',filetypes=[('txt','*.txt')])
        self.txt_path=s2fname
        print('文件地址为:{}'.format(self.txt_path))
    '''
    说明：多线程开启站点地图抓取
    '''
    def import_txt(self):
        T = threading.Thread(target=self.__import_txt,args=())
        T.start()
    def __start(self):
        print('开始处理文本')
        list_data = self.check_button()
        text_object=TextObject(self.txt_path)
        txt_content=text_object.read_text()
        txt_content=text_object.sort_text(txt_content)
        for index,value in enumerate(list_data):
            print(index,value)
            if value==1:
                if index==0 :
                    print('dd')
                elif index==1 :#过滤掉特殊的字符
                    txt_content=text_object.filter_txt(txt_content)
                    print(txt_content)
                elif index==2:#去除重复度高的
                    print('sss')
                    # txt_content=text_object.list_in_line(txt_content)
                    # TextObject.list_write_text(txt_content,res[0],res[1],result_path,like_path)
                else:#分割文本内容
                    txt_content=text_object.split_list(txt_content,2,1)
                    for index,content in enumerate(txt_content):
                        write_path=r"C:\Users\Administrator\Desktop\python\key_split_{}.txt".format(index)
                        # for line in content:
                        text_object.write_text(write_path,content,'a')
                    print(txt_content)
        print(txt_content)
    def start(self):
        T = threading.Thread(target=self.__start,args=())
        T.start()


if __name__ == "__main__":

    root = tk.Tk()
    myGUI = GUI(root)
