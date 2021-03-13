import requests
import json
import re
import time
'''
    字符串类的操作
'''
class HandleStr(object):
    #对超出的字符串长度的内容按照指定的分割符合进行截取，并返回list结果
    def split_string(self,string='',maxlen=5000):
        pattern = ','
        result_list = []
        length = len(string)
        if length > maxlen:
            str_list = string.split(pattern)
            list_num = len(str_list)
            flag = True
            i = 0
            temp = ''
            while flag:
                temp_two = temp
                temp_two = temp_two + str_list[i]
                if len(temp_two) > maxlen:
                    if i == list_num - 1:
                        result_list.append(temp)
                        result_list.append(str_list[i])
                    else:
                        result_list.append(temp)
                        temp = str_list[i]
                else:
                    if i == list_num - 1:
                        result_list.append(temp_two)
                    else:
                        if temp != '':
                            temp = temp + pattern + str_list[i]
                        else:
                            temp = temp + str_list[i]
                i = i + 1
                if i >= (list_num):
                    flag = False
            return result_list
        else:
            result_list.append(string)
            return result_list
    #通过正则对字符串进行过滤替换
    def filter_str(self,text=''):
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^（^）^(^)^:^,^.^。^，^-^%^!^?^\n]")  # 匹配不是中文、大小写、数字的其他字符
        text = cop.sub('',text)
        text = text.replace("\n",'<br/>').replace("-",'').replace('，',',').replace('。','.')
        return text

    #通过正则判断字符串是否符合指定的格式
    def search_str(self,text=''):
        pattern=re.compile(r'https://www.hnhxpsj.com/([^pros]).*\.htm', re.I)
        res=pattern.search(text)
        print(res)
        if res:
            pattern = re.compile(r'\d+',re.I)
            digital = pattern.findall(text)
            print(digital)
            print(digital[0])
            return True
        else:
            return False

    #通过一定的规则 获取指定的字符串并返回
    def get_str(self,str=''):
        res=str.split('/')[-2].split('_')[-1].replace('-',' ')
        return res
        # print(res)
if __name__=='__main__':
    Strclass=HandleStr()
    # Strclass.search_str(str)
    Strclass.get_str()