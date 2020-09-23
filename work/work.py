import os
import time
import re
import random
import math
# from datetime import date,datetime
# print(time.strftime("%Y-%m-%d", time.localtime()))
def make_file(path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'):
    # path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'
    if os.path.exists('../data/keyword.txt'):
        # with open('../data/keyword.txt', mode='r', encoding='utf-8') as ff:
        # print("文件存在！")
        pass
    else:
        with open("../data/keyword.txt", mode='w', encoding='utf-8') as ff:
            print("文件创建成功！")
def improve():
    # pattern=r'(.*)([^test]).txt'
    # pattern=r'(.*)(^-)(.*).txt'
    pattern=re.compile(r'(.*)((?!test)\.)txt')
    file_dir=r'E:\红星办公文件\关键词\抓取工具\2.0spider'
    dir=time.strftime("%Y-%m-%d", time.localtime())
    for root, dirs, files in os.walk(file_dir):
        for filename in files:
            print(filename)
            # flag=re.match(pattern,filename)
            flag=pattern.search(filename)
            print(flag)
        # print(files)
    pass
def write_txt(keyword,filename):
    make_file(filename)
    with open(filename, "a", encoding='utf-8') as f:
        f.write(keyword)
    pass
def read_txt_make():
    make_num=20000
    data=[]
    prop_num=[]
    filename_all=[]
    dir=r'E:\pycharmdata\pydata\data\组装txt'
    write_filename=dir+'/../'+'组装结果/'+'add.txt'
    for root, dirs, files in os.walk(dir):
        for filename in files:
            # print(filename)
            file_handle=open(dir+'\\'+filename, mode='r',encoding='utf-8')
            file_all=len(file_handle.readlines())
            filename_all.append(file_all)
    all_rows=sum(filename_all)
    prop_num=[math.ceil(i/all_rows*make_num) for i in filename_all]
    print(prop_num)
    i=0
    for root, dirs, files in os.walk(dir):
        for filename in files:
            print(prop_num[i])
            with open(dir+'\\'+filename, 'r', encoding='utf-8') as f:
                a=random.sample(f.readlines(),prop_num[i])
                for word in a:
                    write_txt(word,write_filename)
            i=i+1

read_txt_make()