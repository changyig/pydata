import os.path

import requests
import json
import re
import time
import math
import difflib
from string_class import HandleStr
import random
from baidu_api import BaiduApi
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
        if os.path.isfile(write_file):
            pass
        else:
            open(write_file, mode='w',encoding='utf-8')
        write_handel = open(write_file, mode=mode,encoding='utf-8')
        if isinstance(content,str):
            write_handel.write(content.strip()+'\n')
        elif isinstance(content,list):
            for line in content:
                write_handel.write(line.strip()+'\n')
        else:
            print('未知处理方式')


    '''
    type: 0(数量等分) 1(等额份数)
        说明：将list列表按照一定的数量均分成n个list列表
        或者按照等分的数量进行
        并返回相应的list列表
    '''
    def split_list(self,content=[],num=50,tpye=0):
        if tpye==1:
            n = num
        else:
            n = math.ceil(len(content) / num)
        k,m = divmod(len(content),n)
        # print(k,m,n)
        return [content[i * k + min(i,m):(i + 1) * k + min(i + 1,m)] for i in list(range(n))]
    '''
        说明：将内容进行默认的排序
    '''
    def sort_text(self,content):
        res=content.sort()
        return content

    '''
        说明：去除判断列表中相似重复度比较高的元素
        返回数据：[返回列表中相似度极高的下标，以及重复的键值]
    '''
    def list_in_line(self,content=[],threshold=0.85):
        list_data=[]
        list_index=[]#遍历行号
        list_like=[]#相似的行号
        content2=content[:]
        dict_like={}
        for index,line in enumerate(content):
            if index in list_like:
                list_index.append(index)
            else:
                list_index.append(index)
                # content2.pop(0)
                for index2,line2 in enumerate(content2):
                    if (index2 in list_index) or (index2 in list_like):
                        pass
                    else:
                        # print(index,line,index2,line2)
                        digital=self.string_object.compare_string(line,line2)#相似性长尾词进行判断 可以设置一个阀值进行去重
                        if digital >threshold:
                            print('相似编号:{0}-{1},相似内容:{2},对比:{3}'.format(index,index2,line,line2))
                            if index in dict_like:
                                dict_like[index].append(index2)
                            else:
                                dict_like[index]=[index2]
                            list_like.append(index2)
        return [list_like,dict_like]

    '''
        说明：list_in_line 方法之后 进一步处理的方法
            根据传入的参数 把内容进行分类存入不同的文件
            content:txt内容列表
            list_index:重复的内容列表下标 需要剔除
            dict_list:字典形式的内容列表 可供查看中间的过程
            result_path:提出后需要保存的txt文件
            like_path:相似长尾词的存入的文件
        返回数据：
    '''
    def list_write_text(self,content,list_index,dict_list,result_path='',like_path=''):
        for index,line in enumerate(content):
            # print(index,line,list_index)
            if index not in list_index:
                self.write_text(result_path,line,'a')
        for i in dict_list:
            temp='相似关键词:{}'.format(content[i])
            for ii in dict_list[i]:
                temp=temp+'-->'+str(content[ii])
            self.write_text(like_path,temp,'a')

    '''
        说明：将list列表转换成指定的数据并返回list
    '''
    def str_list_text(self,content):
        file_path = r'C:\Users\CYG\Desktop\result.txt'
        strObject=HandleStr()
        for line in content:
            line=line.strip().lower()+'\n'
            if strObject.str_len(line,3):
                print(line)
                self.write_text(file_path,line,'a')

    '''
        说明：将list列表转换成指定的数据并返回list
    '''

    def str_list_text2(self,content):
        strObject = HandleStr()
        return_list=[]
        for line in content:
            line = line.strip().lower() + '\n'
            if strObject.str_len(line,3):
                return_list.append(line)
        return return_list
    '''
    说明：过滤掉txt文本中含有的特殊符号的 只保留  字母、数字、空格
    '''
    def filter_txt(self,content):
        list_data=[]
        for i in content:
            list_data.append(self.string_object.retain_digital_letter(i))
        return list_data

    '''
        说明：过滤掉txt文本中含有的特殊符号的 只保留  字母、数字、空格
        '''
    def baidu_translate(self,content):
        write_path=r'C:\Users\CYG\Desktop\pydata\translate4.txt'
        open(write_path,'w').close()
        BaiduApiObj=BaiduApi()
        num=200
        n = math.ceil(len(content) / num)
        k,m = divmod(len(content),n)
        # print(k,m,n)
        temp_list=[content[i * k + min(i,m):(i + 1) * k + min(i + 1,m)] for i in list(range(n))]
        for onelist in temp_list:
            translate_str=''.join(onelist)
            # print(translate_str)
            return_data=BaiduApiObj.start(translate_str)
            print(return_data)
            self.write_text(write_path,return_data,'a')
            time.sleep(1.5)

    '''
    说明：给予指定的list表 过滤掉重复的内容 并返回不重复的内容
    '''
    def delete_like_list(self,content=[],threshold=0.85):
        contents=self.split_list(content)
        return_list=[]
        for content in contents:
            res=self.list_in_line(content,threshold)
            for index,line in enumerate(content):
                if index not in res[0]:
                    return_list.append(content[index])
        # print(return_list)
        return return_list
if __name__=='__main__':
    file_path=r'C:\Users\CYG\Desktop\key_result2.txt'

    TextObject=TextObject(file_path)
    content=TextObject.read_text()
    # TextObject.delete_like_list(content)
    # TextObject.baidu_translate(content)
    # content=TextObject.filter_txt(content)
    #
    # TextObject.str_list_text(content)
    # name=TextObject.get_text_name(file_path)

    # TextObject.write_text(r'C:\Users\CYG\Desktop\key3.txt',content)

    # result_path = r'C:\Users\CYG\Desktop\key_result.txt'
    # like_path = r'C:\Users\CYG\Desktop\key_like.txt'
    # content = TextObject.sort_text(content)
    # random.shuffle(content)
    # random.shuffle(content)
    # random.shuffle(content)
    # random.shuffle(content)
    # contents = TextObject.split_list(content,3,1)
    # for index,content in enumerate(contents):
    #     write_path=r"C:\Users\CYG\Desktop\pydata\key_split_{}.txt".format(index)
    #     open(write_path,'w').close()
    #     for line in content:
    #         TextObject.write_text(write_path,line,'a')

    # 根据txt文本中的相似性，将文本进行区分存储
    result_path = r'C:\Users\CYG\Desktop\key_result2.txt'
    like_path = r'C:\Users\CYG\Desktop\key_like.txt'
    content = TextObject.sort_text(content)
    contents=TextObject.split_list(content)
    for content in contents:
        res=TextObject.list_in_line(content)
        TextObject.list_write_text(content,res[0],res[1],result_path,like_path)
