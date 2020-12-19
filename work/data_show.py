import matplotlib.pyplot as plt
import time
import os
import pymysql
import math
class Data:
    def __init__(self):
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
        self.mysqlNum = 0  # 插入数据库的数量
        self.cursor = self.connect.cursor()
    def get_data(self):
        sql = "select type,count(*) as num,origin from all_keyword where origin like '%transports-speciaux.ch%' GROUP BY type"
        # sql = "select words ,count(*) as num ,id from all_keyword where origin='transports-speciaux.ch' group by words"
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        return res
        pass
    def bar_show(self):
        x=[]
        y=[]
        data=self.get_data()
        for i in data:
            x.append(i[0])
            y.append(i[1])
        plt.xlim(0,max(x))
        print(max(x))
        p1 = plt.bar(x,height=y,width=0.5)
        plt.title('words')
        plt.show()
        pass
    def plot_show(self):
        pass
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
        labels = 'transports-speciaux.ch'  # 设置标签
        plt.title(labels)
        sizes = x  # 占比，和为100
        # explode = (0,0.1,0,0)  # 展开第二个扇形，即Hogs，间距为0.1
        plt.pie(sizes,labels=y,autopct='%1.1f%%',shadow=True,
                startangle=90)  # startangle控制饼状图的旋转方向
        plt.axis('equal')  # 保证饼状图是正圆，否则会有一点角度偏斜
        plt.show()
if __name__ == '__main__':
    data = Data()
    data.pie_show()
    print('结束执行')