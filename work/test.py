import time
from googletrans import Translator
import quicktranslate
from bs4 import BeautifulSoup
import requests
from lxml import etree
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
    url='https://www.hnhxpsj.com/cp/n1851.htm'
    html = requests.get(url,timeout=10).content.decode('utf8')
    # print(html)
    tree=etree.HTML(html)
    title=tree.xpath("//h1/text()")
    # content = tree.xpath("//div[@class='news-left']/*[not(name=div)]/text()")
    content = tree.xpath("//div[@class='news-left']/*[not(contains(@class,'news-art1')) and not(contains(@class,'show-msg')) and not(contains(@class,'xg-news'))]//text()")
    print(title)
    print(content)
# res=quicktranslate.get_translate_google('星期日')
# print(res)
test1()