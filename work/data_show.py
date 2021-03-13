# coding:utf-8
import matplotlib.pyplot as plt
import time
import os
import pymysql
import math
from mysql_class import Mysql
class Data:
    def __init__(self,mysql=None):
        self.mysql = mysql
        self.connect = False
        self.connect = pymysql.connect(
            host="127.0.0.1",
            db="industro",
            user="root",
            passwd="root",
            charset='utf8',
            use_unicode=True
        )
        self.flag = True
        self.start_time = time.time()
        self.currentLine = 0
        self.num = 0  # 插入数据库的数量
        self.website = 'polskapaczkarnia.pl'  # 网站域名
        self.cursor = self.connect.cursor()
        self.bie_or_bar = 3 #1:bie->product 2:bie->materials 3:bar->words length
    #获取指定表格的总得数量
    def get_num(self):
        # sql = "select type,count(*) as num,origin from all_keyword_data where origin like '%transports-speciaux.ch%' GROUP BY type"
        origin_value ="'%"+self.website+"%'"
        sql = "select count(*) as num  from all_keyword_data where origin like {} ".format(origin_value)
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        return res
    #从数据库中调用相应的数据
    def get_data(self):
        origin_value = "'%" + self.website + "%'"
        if self.bie_or_bar==1:
            sql = "select type,count(*) as num,origin from all_keyword_data where origin like {} GROUP BY type".format(origin_value)
        else:
            sql = "select words ,count(*) as num ,id from all_keyword_data where origin like {} group by words".format(
                origin_value)
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        return res
        pass

    #条柱状数据显示
    def bar_show(self):
        x=[]
        y=[]
        data=self.get_data()
        num_tupple=self.get_num()
        for i in num_tupple:
            self.num=i[0]
        for i in data:
            x.append(i[0])
            y.append(i[1])
        plt.xlim(0,max(x))
        p1 = plt.bar(x,height=y,width=0.5)
        plt.title("{}:words".format(self.num))
        plt.show()
        pass
    def plot_show(self):
        pass

    #扇形数据显示
    # //1 => 'jaw crusher', 2 => 'impact crusher', 3 => 'cone crusher', 4 => 'stone crusher', 5 => 'mobile crusher',
    # 6 => 'crusher', 8 => 'hammer mill', 9 => 'ball mill', 10 => 'grinding mill', 13 => 'sand making machine', 14 => 'drying machine'
    def pie_show(self):
        type = {0:'other',1:'jaw crusher',2:'impact crusher',3:'cone crusher',4:'stone crusher',5:'mobile crusher',6:'crusher',8:'hammer mill',9:'ball mill',10:'grinding mill',13:'sand making machine',14:'drying machine'}
        x = []
        y = []
        data = self.get_data()
        for i in data:
            x.append(i[1])
            y.append(type[i[0]])
        print(x,y)
        explode=[]
        for i in x:
            explode.append(0.5)
        plt.title(self.website)
        sizes = x  # 占比，和为100
        # explode = (0,0.1,0,0)  # 展开第二个扇形，即Hogs，间距为0.1
        plt.pie(sizes,labels=y,autopct='%1.1f%%',shadow=True,
                startangle=90)  # startangle控制饼状图的旋转方向
        plt.axis('equal')  # 保证饼状图是正圆，否则会有一点角度偏斜
        plt.show()
    #物料词和非物料词扇形图
    def pie_show2(self):
        #物料+产品  物料+非产品 非物料+产品 非物料+非产品
        num=[]
        num1=self.mysql.table('all_keyword_data').where([{'origin':['like',self.website]},{'material_score':['!=',0]},{'type':['!=',0]}]).count()
        num2=self.mysql.table('all_keyword_data').where([{'origin':['like',self.website]},{'material_score':['!=',0]},{'type':['=',0]}]).count()
        num3=self.mysql.table('all_keyword_data').where([{'origin':['like',self.website]},{'material_score':['=',0]},{'type':['!=',0]}]).count()
        num4=self.mysql.table('all_keyword_data').where([{'origin':['like',self.website]},{'material_score':['=',0]},{'type':['=',0]}]).count()
        num.extend([num1,num2,num3,num4])
        print(num)
        x = []
        y = ['物料+产品','物料+非产品','非物料+产品','非物料+非产品']
        for i in num:
            x.append(i[0])
        plt.title(self.website+'词的分类分析')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(x,labels=y,autopct='%1.1f%%',shadow=True,
                startangle=90)  # startangle控制饼状图的旋转方向
        plt.axis('equal')  # 保证饼状图是正圆，否则会有一点角度偏斜
        # plt.figure("bie")
        plt.show()
    # 返回元祖数据格式 （数量+id+物料名字）
    def get_material_bie(self):
        material=[]
        sql="select count(*) as num,material_id,name from all_keyword_data a left join materials b on a.material_id=b.id where a.origin='"+self.website+"'  group by a.material_id"
        material_sql="select id,name from materials "
        res=self.mysql.query(sql)
        return res
 #物料词和非物料词扇形图
    def bar3(self):
        #（数量+id+物料名字）
        temp_x = []
        y = []
        num_tupple = self.get_material_bie()
        for i in num_tupple:
            temp_x.append(i[2])
            y.append(i[0])
        x=tuple(temp_x)
        print(x,y)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        x = range(len(temp_x))
        p1 = plt.bar(x,y)
        plt.xticks(x,temp_x)
        plt.show()
        pass
if __name__ == '__main__':
    mysql = Mysql(dbname='industro')
    data = Data(mysql)
    # data.bar3()
    # data.pie_show()
    if data.bie_or_bar==1:
        data.pie_show()
    elif data.bie_or_bar==2:
        data.pie_show2()
    else:
        data.bar_show()
    print('结束执行')