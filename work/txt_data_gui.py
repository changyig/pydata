import tkinter as tk
import threading
import time
import sys
import re
from test3 import TextData
from tkinter import filedialog
import copy
import matplotlib.pyplot as plt
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
def show_data_bar(data_x,data_y,title='bar_show'):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    p1 = plt.bar(data_x,data_y)
    plt.show()

class GUI():
    def __init__(self,root):
        self.sitemap = tk.StringVar()
        self.txt_path = r''
        self.initGUI(root)
        self.text_data='' #[数量, ['product':{},'material':{},'country':{}], {0:数量,1:数量,2:数量,3:数量,4:数量,5:数量,6:数量,7:数量}]
                                        # {0:'啥也没有',1:'地区',2:'物料',3:'物料+地区',4:'产品',5:'产品+地区',6:'产品+物料',7:'产品+物料+地区'}
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
        # self.txt_split = tk.Button(root,text='处理txt文件',command=self.handel_txt)
        # self.txt_split.grid(row=1,column=4)
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

        #图形化展示
        # self.mat=plt.figure(figsize=(5,4),dpi=100)
        # self.mat_show=FigureCanvasTkAgg(self.mat,root)
        # self.mat_show.get_tk_widget().grid(row=8, rowspan=2,columnspan=5)


        #功能按钮区
        # self.CheckVar1 = tk.IntVar()
        # self.CheckVar2 = tk.IntVar()
        # self.CheckVar3 = tk.IntVar()
        # self.CheckVar4 = tk.IntVar()
        # self.ch1 = tk.Checkbutton(root,text='文本转换',         variable=self.CheckVar1,onvalue=1,offvalue=0,command=self.check_button)
        # self.ch2 = tk.Checkbutton(root,text='过滤特殊字符',      variable=self.CheckVar2,onvalue=1,offvalue=0,command=self.check_button)
        # self.ch3 = tk.Checkbutton(root,text='去除重复度高的',    variable=self.CheckVar3,onvalue=1,offvalue=0,command=self.check_button)
        # self.ch4 = tk.Checkbutton(root,text='分割',            variable=self.CheckVar4,onvalue=1,offvalue=0,command=self.check_button)
        # self.like_num = tk.StringVar()
        # self.like_num.set(0.82)
        # self.like_num_box = tk.Entry(root,textvariable=self.like_num)
        # self.split_num=tk.StringVar()
        # self.split_num.set(2)
        # self.split_num_box = tk.Entry(root, textvariable=self.split_num)
        # self.ch1.grid(row=10,column=1)
        # self.ch2.grid(row=11,column=1)
        # self.ch3.grid(row=12,column=1)
        # self.like_num_box.grid(row=12,column=2)
        # self.ch4.grid(row=13,column=1)
        # self.split_num_box.grid(row=13,column=2)

        #功能按钮区
        self.start = tk.Button(root,text='数据解析',command=self.start)
        self.start.grid(row=14,column=6)
        self.start = tk.Button(root,text='总体条形图',command=self.__bar_data)
        self.start.grid(row=15,column=6)
        self.start = tk.Button(root,text='总体饼状图',command=self.__pie_data)
        self.start.grid(row=15,column=7)
        self.start = tk.Button(root,text='国家柱状图',command=self.__country_bar)
        self.start.grid(row=16,column=6)
        self.start = tk.Button(root,text='国家饼状图',command=self.__country_pie)
        self.start.grid(row=16,column=7)
        self.start = tk.Button(root,text='物料柱状图',command=self.__material_bar)
        self.start.grid(row=17,column=6)
        self.start = tk.Button(root,text='物料饼状图',command=self.__material_pie)
        self.start.grid(row=17,column=7)
        self.start = tk.Button(root,text='产品分布图',command=self.__product_bar)
        self.start.grid(row=18,column=6)
        self.start = tk.Button(root,text='词长分布图',command=self.__words_len)
        self.start.grid(row=18,column=7)
        root.mainloop()
    def time_run(self):
        timestr = time.strftime("%H:%M:%S") # 获取当前的时间并转化为字符串
        self.time_box.configure(text=timestr)   # 重新设置标签文本
        root.after(1000,self.time_run) # 每隔1s调用函数 gettime 自身获取时间
    # def check_button(self):
    #     list_data=[self.CheckVar1,self.CheckVar2,self.CheckVar3,self.CheckVar4]
    #     dicts_data = {0:'文本转换',1:'过滤特殊字符',2:'去除重复度高的',3:'分割'}
    #     for index,list in enumerate(list_data):
    #         list_data[index]=list.get()
    #     message_info='选中的功能区为：'
    #     for index ,d in dicts_data.items():
    #         if list_data[index]==1:
    #             message_info=message_info+','+d
    #     print(message_info)
    #     return list_data

    # def __handel_txt(self):
    #     text_object=TextData(self.txt_path)
    #     data = text_object.read_txt()
    #     print(data)
    # def handel_txt(self):
    #     T = threading.Thread(target=self.__handel_txt,args=())
    #     T.start()
    def make_autopct(self,values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            # 同时显示数值和占比的饼图
            return '{p:.2f}%({v:d})'.format(p=pct,v=val)
        return my_autopct
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

    '''
        说明：通过bar将数据可视化
    '''
    def __bar_data(self):
        bar_data_x = ['产品','物料','国家']
        product_num=copy.deepcopy(self.text_data[1]['product']['num'])
        material_num=copy.deepcopy(self.text_data[1]['material']['num'])
        country_num=copy.deepcopy(self.text_data[1]['country']['num'])
        bar_data_y = [product_num,material_num,country_num]
        plt.figure("总体柱状分布图",figsize=(8, 8), dpi=100)
        plt.title('总体柱状分布图,总数量:{}'.format(self.text_data[0]))
        for a,b in zip(bar_data_x,bar_data_y):
            plt.text(a,b + 0.05,'%.0f' % b,ha='center',va='bottom',fontsize=11)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        p1 = plt.bar(bar_data_x,bar_data_y)
        plt.show()

    def __pie_data(self):
        dict_name = {0:'啥也没有',1:'地区',2:'物料',3:'物料+地区',4:'产品',5:'产品+地区',6:'产品+物料',7:'产品+物料+地区'}
        dict_x = []
        dict_y = []
        for xy in self.text_data[2].items():
            dict_x.append(xy[1]),dict_y.append(dict_name[xy[0]])
        plt.figure("词的分类分析",figsize=(8, 8), dpi=100)
        plt.title('词的分类分析')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        exp = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
        # plt.pie(dict_x,labels=dict_y,autopct='%1.1f%%',shadow=False,startangle=90,explode=exp)  # startangle控制饼状图的旋转方向
        plt.pie(dict_x,labels=dict_y,autopct=self.make_autopct(dict_x),shadow=False,startangle=90,explode=exp)  # startangle控制饼状图的旋转方向
        plt.axis('equal')  # 保证饼状图是正圆，否则会有一点角度偏斜
        plt.legend()
        plt.show()
    '''
           说明：通过bar将数据可视化
       '''

    def __product_bar(self):
        #产品条形图
        bar_data_x = []
        bar_data_y = []
        data=copy.deepcopy(self.text_data[1]['product'])
        num=data.pop('num')
        d_order = sorted(data.items(),key=lambda x:x[1],reverse=True)
        for nm in d_order:
            if nm[1] >= 10:
                bar_data_x.append(nm[0])
                bar_data_y.append(nm[1])
        plt.figure("产品柱状图分布",figsize=(8, 8), dpi=100)
        plt.title('产品柱状图分,布总数量:{}'.format(num))
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        p1 = plt.bar(bar_data_x,bar_data_y,bottom=0.217)
        for a,b in zip(bar_data_x,bar_data_y):
            plt.text(a,b + 0.05,'%.0f' % b,ha='center',va='bottom',fontsize=11)
        plt.xticks(bar_data_x,rotation=-60)
        plt.show()

    '''
               说明：通过bar将数据可视化
           '''

    def __words_len(self):
        #产品条形图
        bar_data_x = []
        bar_data_y = []
        data = copy.deepcopy(self.text_data[3])
        print(data)
        d_order = sorted(data.items(),key=lambda x:x[1],reverse=True)
        for nm in d_order:
            if nm[1] >= 10:
                bar_data_x.append(nm[0])
                bar_data_y.append(nm[1])
        plt.figure("产品柱状图分布",figsize=(8,8),dpi=100)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        p1 = plt.bar(bar_data_x,bar_data_y,bottom=0.217)
        for a,b in zip(bar_data_x,bar_data_y):
            plt.text(a,b + 0.05,'%.0f' % b,ha='center',va='bottom',fontsize=11)
        plt.xticks(bar_data_x,rotation=-60)
        plt.show()

    '''
               说明：通过bar将数据可视化
           '''

    def __country_pie(self):
        data_x = []
        data_y = []
        data = copy.deepcopy(self.text_data[1]['country'])
        num=data.pop('num')
        d_order = sorted(data.items(),key=lambda x:x[1],reverse=True)
        for xy in data.items():
            if xy[1] >= 10:
                data_x.append(xy[1]),data_y.append(xy[0])
        plt.figure("国家饼状图分布",figsize=(8, 8), dpi=100)
        plt.title('国家饼状图分,布总数量:{}'.format(num))
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        exp = [0.1 for x in data_x]
        # plt.pie(data_x,labels=data_y,autopct='%1.1f%%',shadow=False,startangle=90,explode=exp)  # startangle控制饼状图的旋转方向
        plt.pie(data_x,labels=data_y,autopct=self.make_autopct(data_x),shadow=False,startangle=90,explode=exp)  # startangle控制饼状图的旋转方向
        plt.axis('equal')  # 保证饼状图是正圆，否则会有一点角度偏斜
        plt.legend()
        plt.show()

    '''
                  说明：通过bar将数据可视化
            '''

    def __country_bar(self):
        bar_data_x = []
        bar_data_y = []
        data = copy.deepcopy(self.text_data[1]['country'])
        num=data.pop('num')
        d_order = sorted(data.items(),key=lambda x:x[1],reverse=True)
        for nm in d_order:
            if nm[1] >= 10:
                bar_data_x.append(nm[0])
                bar_data_y.append(nm[1])
        plt.figure("国家柱状图分布",figsize=(8, 8), dpi=100)
        plt.title('国家柱状图分布,总数量:{}'.format(num))
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        p1 = plt.bar(bar_data_x,bar_data_y,bottom=0.217)
        for a,b in zip(bar_data_x,bar_data_y):
            plt.text(a,b + 0.05,'%.0f' % b,ha='center',va='bottom',fontsize=11)
        plt.xticks(bar_data_x,rotation=-60)
        plt.show()

    '''
                  说明：通过bar将数据可视化
              '''

    def __material_pie(self):
        data_x = []
        data_y = []
        data = copy.deepcopy(self.text_data[1]['material'])
        num = data.pop('num')
        d_order = sorted(data.items(),key=lambda x:x[1],reverse=True)
        for xy in data.items():
            if xy[1] >= 10:
                data_x.append(xy[1]),data_y.append(xy[0])
        plt.figure("物料饼状图分布",figsize=(8, 8), dpi=100)
        plt.title('物料饼状图分,布总数量:{}'.format(num))
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        exp = [0.1 for x in data_x]
        # plt.pie(data_x,labels=data_y,autopct='%1.1f%%',shadow=False,startangle=90,explode=exp)  # startangle控制饼状图的旋转方向
        plt.pie(data_x,labels=data_y,autopct=self.make_autopct(data_x),shadow=False,startangle=90,explode=exp)  # startangle控制饼状图的旋转方向
        plt.axis('equal')  # 保证饼状图是正圆，否则会有一点角度偏斜
        plt.legend()
        plt.show()

    '''
                  说明：通过bar将数据可视化
            '''

    def __material_bar(self):
        bar_data_x = []
        bar_data_y = []
        data = copy.deepcopy(self.text_data[1]['material'])
        num = data.pop('num')
        d_order = sorted(data.items(),key=lambda x:x[1],reverse=True)
        for nm in d_order:
            if nm[1] >= 10:
                bar_data_x.append(nm[0])
                bar_data_y.append(nm[1])
        plt.figure("物料柱状图分布",figsize=(8, 8), dpi=100)
        plt.title('物料柱状图分布,总数量:{}'.format(num))
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        p1 = plt.bar(bar_data_x,bar_data_y,bottom=0.217)
        for a,b in zip(bar_data_x,bar_data_y):
            plt.text(a,b + 0.05,'%.0f' % b,ha='center',va='bottom',fontsize=11)
        plt.xticks(bar_data_x,rotation=-60)
        plt.show()
    def bar_data(self):
        T = threading.Thread(target=self.__bar_data,args=())
        T.start()


    def pie_data(self):
        T = threading.Thread(target=self.__pie_data,args=())
        T.start()
    def __start(self):
        print('开始处理文本')
        # list_data = self.check_button()
        text_object=TextData(self.txt_path)
        self.text_data=text_object.read_txt()
        print('总数:{}'.format(self.text_data[0]))
        print('产品总数:{},所占百分比:{:.2%}'.format(self.text_data[1]['product']['num'],self.text_data[1]['product']['num'] /self.text_data[0]))
        for i in self.text_data[1]['product'].items():
            print("{}数量:{},所占百分比:{:.2%}".format(i[0],i[1],i[1] / self.text_data[0]))
        print('物料总数:{},所占百分比:{:.2%}'.format(self.text_data[1]['material']['num'],
                                            self.text_data[1]['material']['num'] / self.text_data[0]))
        for i in self.text_data[1]['material'].items():
            print("{}数量:{},所占百分比:{:.2%}".format(i[0],i[1],i[1] / self.text_data[0]))
        print('地区总数:{},所占百分比:{:.2%}'.format(self.text_data[1]['country']['num'],
                                            self.text_data[1]['country']['num'] / self.text_data[0]))
        for i in self.text_data[1]['country'].items():
            print("{}数量:{},所占百分比:{:.2%}".format(i[0],i[1],i[1] / self.text_data[0]))
        print('数据分析结束')
        #图形化数据

    def start(self):
        T = threading.Thread(target=self.__start,args=())
        T.start()


if __name__ == "__main__":

    root = tk.Tk()
    myGUI = GUI(root)
