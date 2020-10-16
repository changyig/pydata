import os
import time
import re
import math
import random
# from datetime import date,datetime
# print(time.strftime("%Y-%m-%d", time.localtime()))
#对文件的操作 包括打乱顺序 查询指定txt文件 组装txt
class handleTxt:
    '''
    #说明：①需要遍历组装的文件夹目录（self.readdir）
    #说明：②将新组装txt文件放入的目录（self.writedir）
    #说明：③将新组装txt文件写入的文件名字（self.write_filename）
    #说明：④读取文件的名字（self.read_filename）
    '''
    def __init__(self):
        self.read_filename=''
        self.write_filename='result7.txt'
        self.readdir=r'D:\pydata\data\组装txt'
        self.writedir=r'D:\pydata\data\组装结果txt'
        self.make_num=30000
        self.open_filename=False
    #判断文件是否存在 不存在就创建文件
    def make_file(self,path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'):
        # path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'
        if os.path.exists(path):
            self.open_filename=open(path, mode='w', encoding='utf-8')
            print('第一种刚开启文件:{}'.format(path))
        else:
            if self.open_filename :
                pass
            else:
                self.open_filename=open(path, mode='w', encoding='utf-8')
                print('第二种刚开启文件:{}'.format(path))
    #测试方法
    def improve(self):
        str='error-test.txt'
        # pattern = re.compile(r'(.*)(?!test(.*))(\.)txt')
        # pattern = re.compile(r'((?!test).)*(\.)txt')
        pattern = re.compile(r'(((?!test\.txt).)*)')
        # flag = pattern.search(str)
        flag = pattern.match(str)
        print(flag)

    # 测试方法
    def test(self):
        # pattern=r'(.*)([^test]).txt'
        # pattern=r'(.*)(^-)(.*).txt'
        pattern=re.compile(r'(.*)(?!test)(.*)(\.)txt')
        file_dir=r'E:\红星办公文件\关键词\抓取工具\spider1.7'
        dir=time.strftime("%Y-%m-%d", time.localtime())
        for root, dirs, files in os.walk(file_dir):
            for filename in files:
                print(filename)
                # flag=re.match(pattern,filename)
                # flag=pattern.match(filename)
                flag=pattern.search(filename)
                print(flag)
            # print(files)
        pass
    #向打开的文件中写入数据
    def write_txt(self,keyword,filename):
        if self.open_filename :
            self.open_filename.write(keyword)
        else:
            self.make_file(filename)
    #遍历根据指定文件夹中的文件 并且根据每个文件中的行数按照比例随机抽取行数 并合成新的txt文件
    def read_txt_make(self):
        make_num=self.make_num
        data=[]
        file_rows=[]
        for root, dirs, files in os.walk(self.readdir):
            for filename in files:
                with open(self.readdir+'\\'+filename, mode='r',encoding='utf-8') as f:
                    file_rows.append(len(f.readlines()))
        all = sum(file_rows)
        prop_num=[ math.ceil(i*make_num/all) for i in file_rows]
        i=0
        for root, dirs, files in os.walk(self.readdir):
            for filename in files:
                with open(self.readdir + '\\' + filename, mode='r', encoding='utf-8') as ff:
                    get_rows=random.sample(ff.readlines(),prop_num[i])
                    i = i + 1
                    for keyword in get_rows :
                        self.write_txt(keyword, self.writedir+'/'+self.write_filename)
                    # print(get_rows)
    #打乱txt文件中的顺序
    def txt_shuffle(self):
        out = open(r"E:\红星办公文件\关键词\抓取工具\spider1.7\temp.txt", 'w',encoding='utf-8')
        lines = []
        with open(r"E:\红星办公文件\关键词\抓取工具\spider1.7\result7.txt", 'r',encoding='utf-8') as infile:
            for line in infile:
                lines.append(line)
        random.shuffle(lines)
        random.shuffle(lines)
        random.shuffle(lines)
        random.shuffle(lines)
        random.shuffle(lines)
        for line in lines:
            out.write(line)

    # 去除txt文档中 每行左边的空格 以及空行
    def filter_keyword(self):
        filename = r'C:\Users\CYG\Desktop\linshi.txt'
        file2 = open(r'C:\Users\CYG\Desktop\linshi2.txt', 'a', encoding='utf-8')
        with open(filename, mode='r', encoding='utf-8') as ff:
            for i in ff.readlines():
                str = i.lstrip()
                str=' '.join(str.split())
                if str == '\n':
                    print(str)
                    str = str.strip('\n')
                file2.write(str)
    def filter_digital_txt(self):
        file2 = open(r'C:\Users\CYG\Desktop\linshi.txt', 'a', encoding='utf-8')
        with open(r"D:\github\spider\test\keyword.txt", 'r',encoding='utf-8') as infile:
            for line in infile:
                write_line=re.sub('\d+','',line)
                file2.write(write_line)
    def filter_space_txt(self):
        filename = r'C:\Users\CYG\Desktop\linshi.txt'
        file2 = open(r'C:\Users\CYG\Desktop\linshi2.txt', 'a', encoding='utf-8')
        with open(filename, mode='r', encoding='utf-8') as ff:
            for i in ff.readlines():
                str = i.lstrip()
                str=' '.join(str.split())
                file2.write(str+'\n')
if __name__=='__main__':
    hd=handleTxt()
    hd.filter_space_txt()
    print(33)
    # str=' a s  svadaf12 ad    adsfa '
    # str = str.lstrip()
    # str = ' '.join(str.split())
    # print(str)