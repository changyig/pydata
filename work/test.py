import time
from googletrans import Translator
import quicktranslate
from bs4 import BeautifulSoup
import requests
from lxml import etree
import collections
import re
from mysql_class import Mysql
import math
#实例化

'''
    依据不同的选择器方式，获取页面的中想要获取的指定的元素 
    参数：style:选择器方式 handle:当前对象（浏览器对象或者父对象） pattern:定位元素的类属性之类的 more:返回多个对象或者一个对象 
    返回的数据：1.selenium对象 2.false
    '''


def try_selector(style='css',handle='',pattern='',more=False):
    try:
        if style == 'css':
            if more:
                content = handle.find_elements_by_css_selector(pattern)
            else:
                content = handle.find_element_by_css_selector(pattern)
        elif style == 'xpath':
            if more:
                content = handle.find_elements_by_xpath(pattern)
            else:
                content = handle.find_element_by_xpath(pattern)
        elif style == 'id':
            if more:
                content = handle.find_elements_by_id(pattern)
            else:
                content = handle.find_element_by_id(pattern)
        else:
            if more:
                content = handle.find_elements_by_tag_name(pattern)
            else:
                content = handle.find_element_by_tag_name(pattern)
        return content
    except Exception as e:
        print(e)
        return False
def test():
    service_urls=[
          'translate.google.cn',
        ]
    translator = Translator(service_urls)
    print(translator.translate('星期日').text)
def test1():
    try:
        url='https://www.hnhxpsj.com/cp/n1851.htm'
        html = requests.get(url,timeout=10).content.decode('utf8')
        # print(html)
        tree=etree.HTML(html)
        title=tree.xpath("//h1/text()")
        content_list = tree.xpath("//div[@class='news-left']/*[not(contains(@class,'news-art1')) and not(contains(@class,'show-msg')) and not(contains(@class,'xg-news'))]//text()")
        content=''.join(content_list)
        title=''.join(title)
        print(title)
        print(content)
        if title and content:
            return [title,content]
    except Exception as e:
        print(e)
        return None


def getText():
    txt = open(r"C:\Users\CYG\Desktop\keyword_text.txt","r",encoding='utf-8').read()
    # print(txt)
    txt = txt.lower()
    pattern = re.compile(r'\t|\n|\.|-|:|;|\)|\(|\?|\s[0-9]{1,2}\s|"')  # 定义正则表达式匹配模式（空格等）
    txt = re.sub(pattern,' ',txt)
    # print(string_data)
    text=txt.split()
    res=collections.Counter(text)
    word_counts_top = res.most_common(1500)
    # print(word_counts_top)
    mysql=Mysql(dbname='706')
    for sort_name,num in word_counts_top:
        if len(sort_name)>=3:
            try:
                print(sort_name,num)
                insert_data=[]
                # pattern = re.compile("[^a-zA-Z0-9]")
                # sort_name = pattern.sub('',sort_name)
                filter_list=['con','product','products','solutions','solution','blog','css','js','images','infoimages','fonts','static','ajax']
                if sort_name not in filter_list and len(sort_name)>=3:#注意一些特殊语言的掺杂其中 所以加了个长度判定
                    insert_data.append({'sort_name':sort_name})
                    insert_data.append({'num':num})
                    mysql.table('sort_name').insert(insert_data)
            except BaseException as e:
                print(e)
def test_sort():
    dict={}
    sort='limi'
    sort2='limi2'
    for i in range(10):
        if sort:
            if sort in dict:
                dict[sort] = dict[sort] + 1
            else:
                dict[sort] = 1
    for i in range(10):
        if sort2:
            if sort2 in dict:
                dict[sort2] = dict[sort2] + 1
            else:
                dict[sort2] = 1
    print(dict)
def test_list(content=[]):
    content = ['GADF making process from quarry','gold manganese and iron ore resources of africa','gold melting rajkot made machine']
    # res=list(filter(lambda i: len((i.strip().lower()+'\n').split())>=3 , content))
    res2=[i.lower()  for i in content   if len((i.strip().lower()+'\n').split())>=3]
    print(res2)
    # print(res2)
def square_xy(square1={},square2={}):
    x=[]
    y=[]
    square1_x=[]
    square1_y=[]
    square2_x=[]
    square2_y=[]
    for xy in square1:
        square1_x.append(xy[0])
        square1_y.append(xy[1])
    for xy in square2:
        square2_x.append(xy[0])
        square2_y.append(xy[1])
    print('xx xx yy yy')
    print(square1_x,square2_x,square1_y,square2_y)
    for xx in square1_x:
        max_x=max(square2_x)
        min_x=min(square2_x)
        if xx>=min_x and xx<=max_x :
            x.append(xx)
    for yy in square1_y:
        max_y=max(square2_y)
        min_y=min(square2_y)
        if yy>=min_y and yy<=max_y :
            y.append(yy)
    for xx in square2_x:
        max_x=max(square1_x)
        min_x=min(square1_x)
        if xx>=min_x and xx<=max_x  :
            x.append(xx)
    for yy in square2_y:
        max_y=max(square1_y)
        min_y=min(square1_y)
        if yy>=min_y and yy<=max_y :
            y.append(yy)
    print(x,y)
    x,y=list(set(x)),list(set(y))
    if len(x)<2 or len(y)<2:
        square_size =0
    else:
        square_size=abs(x[0]-x[1])*abs(y[0]-y[1])
    print(square_size)
class elem(object):
    def __init__(self, c, n):
        self.nums = n
        self.char = c


def parse(string):
    stack = []
    i = 0
    while i < len(string):
        c = string[i]
        if c == "(" or c == "[":
            stack.append(c)
        elif c == ")" or c == "]":
            tmp = []
            i += 1
            if i >= len(string):
                c = '1'
            else:
                c = string[i]
            if not c.isdigit():
                i -= 1
                c = 1
            else:
                c = int(c)
            while 1 :
                # print(stack)
                em = stack.pop()
                if em == "(" or em == "[":
                    break
                em.nums = em.nums * c
                tmp.append(em)
            if tmp:
                stack.extend(tmp)
        else:
            s = "" + c
            nums = 1
            while 1:
                i += 1
                if i >= len(string):
                    break
                c = string[i]
                if c.isupper():
                    i-=1
                    break
                elif c.isdigit():
                    nums = int(c)
                    break
                elif c in ["(", "[", ")", "]"]:
                    i -= 1
                    break
                else:
                    s += c
            em = elem(s, nums)
            stack.append(em)
        i += 1
    i, j = 0, 0
    while i < len(stack):
        j = i+1
        while j < len(stack):
            if stack[i].char == stack[j].char:
                stack[i].nums += stack[j].nums
                stack.pop(j)
            j += 1
        i+=1
    stack.sort(key=lambda em : em.char[0])
    string = ''
    for em in stack:
        string += em.char + str(em.nums)
    print(string)
string = 'K4[ON(MgSO3)2]2'
parse(string)

# mytest()
# print(data)