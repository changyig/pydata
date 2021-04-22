import requests
import json
import re
import time
import difflib
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
    #通过正则对特殊符号和中文字符串进行过滤替换
    def filter_str(self,text=''):
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^（^）^(^)^:^,^.^。^，^-^%^!^?^\n]")  # 匹配不是中文、大小写、数字的其他字符
        text = cop.sub('',text)
        text = text.replace("\n",'<br/>').replace("-",'').replace('，',',').replace('。','.')
        return text
    #通过正则对字符串只保留字母和数字
    def retain_digital_letter(self,text=''):
        pattern=re.compile("[^a-zA-Z0-9]")
        text = pattern.sub('',text)
        print(text)
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

    #过滤掉中文和一些指定的特殊字符
    def filter_ch(self,str=''):
        cop = re.compile("[\u4e00-\u9fa5.*^()@/,]")  # 匹配不是中文、大小写、数字的其他字符
        text = cop.sub('',str)

        return text

    #过滤掉中文和一些指定的特殊字符
    def filter_ch2(self,str=''):
        cop = re.compile("[\s()]")  # 匹配不是中文、大小写、数字的其他字符
        text = cop.sub('',str)
        print(text)
        return text
    def str_page(self):
        str='https://www.google.com/search?q=site:ag-susa.cz&ei=pw5TYO3VMYOC-Qa0_52QCw&start=10&sa=N&ved=2ahUKEwitxYDTtbnvAhUDQd4KHbR_B7IQ8tMDegQIARA6&cshid=1616056076188366'
        # res=str.split('&')
        # print(res[2])
        # res[2]='start=290'
        cop = re.compile(r"&start=\d+")
        text = cop.sub('&start=290',str)
        print(text)
    def get_digital(self,url=''):
        str='找到约 6,010 条结果 （用时 0.14 秒）'
        cop = re.compile(r"（.*）")
        text = cop.sub('',str)
        cop = re.compile("[^0-9]")
        text = cop.sub('',text)
        print(text)
    def stain_one_space(self,str=''):
        res = ' '.join(str.split())
        return res
    '''
    说明:比较两个字符串的相似性
    '''
    def compare_string(self,a='',b=''):
        a = self.stain_one_space(a).lower()
        b = self.stain_one_space(b).lower()
        res = difflib.SequenceMatcher(None,a,b).ratio()
        return float(res)
    def test_site(self):
        str1='https://keatsteamympuls.nl/sitemap.xml'
        pattern = re.compile(r'http[s]?://(.*)/(.*\.xml)',re.I)
        res2=pattern.findall(str1)
        print(res2[0][0])
    def str_len(self,str='',num=0):
        res=str.split()
        if len(res)>=num:
            return True
        else:
            return False

if __name__=='__main__':
    Strclass=HandleStr()
    # Strclass.search_str(str)
    str=r'E:\product-photo\images2\briquette-machine\briquette-machine\briquette_machine (34).jpg'
    str=r'brick and tiles crushers in uk'
    # Strclass.test_site()
    Strclass.str_len(str)