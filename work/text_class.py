import requests
import json
import re
import time
import math
import difflib
from string_class import HandleStr
'''
    字符串类的操作
'''
class TextObject(object):
    def __init__(self,file_path=r'C:\Users\CYG\Desktop\key.txt'):
        self.file_path=file_path
        self.string_object=HandleStr()

    '''
        说明：获取指定文件路径的文件名字 和后缀  
        返回结果：['key2.txt', 'key2', 'txt']
    '''
    def get_text_name(self,filename):
        filename=filename.replace('\\','/')
        name=filename.split('/')[-1]
        ext=name.split('.')
        return [name,ext[0],ext[-1]]
    def read_text(self):
        with open(self.file_path,mode='r',encoding='utf-8') as ff:
            return ff.readlines()
    '''
    说明：向指定文件中存入内容
    '''
    def write_text(self,write_file='',content='',mode='w'):
        if write_file=='':
            write_file=self.file_path
        write_handel = open(write_file, mode=mode,encoding='utf-8')

        if isinstance(content,str):
            write_handel.write(content)
        elif isinstance(content,list):
            for line in content:
                write_handel.write(line)
        else:
            print('未知处理方式')

    '''
        说明：将list列表按照一定的数量均分成n个list列表
        并返回相应的list列表
    '''
    def split_list(self,content=[],num=30):
        n =math.ceil(len(content)/num)
        k,m = divmod(len(content),n)
        return [content[i * k + min(i,m):(i + 1) * k + min(i + 1,m)] for i in list(range(n))]
    '''
        说明：将内容进行默认的排序
    '''
    def sort_text(self,content):
        res=content.sort()
        return content

    '''
        说明：去除判断列表中相似重复度比较高的元素
    '''
    def list_in_line(self,content=[]):
        list_data=[]
        content2=content[:]
        list_index=0
        for index,line in enumerate(content):
            content.pop(0)
            index=index+1
            print(index,line)
            # content2.pop(0)
            # for index2,line2 in enumerate(content2):
            #    print(index,line,index2,line2)
            #    digital=self.string_object.compare_string(line,line2)#相似性长尾词进行判断 可以设置一个阀值进行去重
            #    print(digital)
            #    if digital >0.85:
            #         print('相似')
            #         content2.pop(index2)


        #     list_data.append(line)
        # print(list_data)
if __name__=='__main__':
    file_path=r'C:\Users\CYG\Desktop\key3.txt'
    TextObject=TextObject(file_path)
    content=TextObject.read_text()
    # name=TextObject.get_text_name(file_path)
    # print(name)
    # print(TextObject.read_text())
    # content=TextObject.sort_text(content)
    # TextObject.write_text(r'C:\Users\CYG\Desktop\key3.txt',content)
    # content=TextObject.split_list(content)

    content=TextObject.list_in_line(content)
    print(content)
    # TextObject.write_text(r'C:\Users\CYG\Desktop\key2.txt',content,'w')