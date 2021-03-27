import time
from googletrans import Translator
import quicktranslate
from bs4 import BeautifulSoup
import requests
from lxml import etree
import collections
import re
from mysql_class import Mysql
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
    txt = open(r"C:\Users\CYG\Desktop\test.txt","r",encoding='utf-8').read()
    # print(txt)
    txt = txt.lower()
    pattern = re.compile(r'\t|\n|\.|-|:|;|\)|\(|\?|\s[0-9]{1,2}\s|"')  # 定义正则表达式匹配模式（空格等）
    txt = re.sub(pattern,' ',txt)
    # print(string_data)
    text=txt.split()
    res=collections.Counter(text)
    word_counts_top = res.most_common(500)
    # print(word_counts_top)
    mysql=Mysql(dbname='646')
    for sort_name,num in word_counts_top:
        if len(sort_name)>=3:
            try:
                print(sort_name,num)
                insert_data=[]
                pattern = re.compile("[^a-zA-Z0-9]")
                sort_name = pattern.sub('',sort_name)
                insert_data.append({'sort_name':sort_name})
                insert_data.append({'num':num})
                mysql.table('sort_name').insert(insert_data)
            except BaseException as e:
                print(e)

data=getText()
# print(data)