import time
import os
import pymysql
class Mysql:
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
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
    def read_txt_mysql(self):#（0 未知 1是地区词 2 不是地区词）
        origin='uwojciakow.pl'
        filename= r"./scrapy_data/uwojciakow.pl.txt"
        country=0
        remark='排名比较好的网站'
        with open(filename, 'r',encoding='utf-8') as infile:
            for line in infile:
                try:
                    sql = "INSERT INTO all_keyword(keyword,origin,createtime,country,remark) VALUES(%s,%s,%s,%s,%s)"
                    self.cursor.execute(sql, (self.filter_space(line), origin, int(time.time()),country,remark))
                    self.cursor.connection.commit()
                    self.mysqlNum = self.mysqlNum + 1
                    print('成功插入数据库的数量:{}'.format(self.mysqlNum))
                except BaseException as e:
                    print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
                    # print('重新连接数据库')
                    # self.connect = pymysql.connect(
                    #     host="127.0.0.1",
                    #     db="scrapy",
                    #     user="root",
                    #     passwd="root",
                    #     charset='utf8',
                    #     use_unicode=True
                    # )
                    # self.cursor = self.connect.cursor()
            print('文件导入完成')
    '''
    过滤文本中连续的空格
    '''
    def filter_space(self,str=''):
        str = ' '.join(str.split())
        return str
if __name__ == '__main__':
    mysql = Mysql()
    mysql.read_txt_mysql()
    print('结束执行')