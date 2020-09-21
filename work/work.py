import os
import time
import re
# from datetime import date,datetime
print(time.strftime("%Y-%m-%d", time.localtime()))
def make_file(path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'):
    # path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'
    print(path)
    if os.path.exists('../data/keyword.txt'):
        with open('../data/keyword.txt', mode='r', encoding='utf-8') as ff:
            print(ff.readlines())
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
improve()