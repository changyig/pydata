from bs4 import BeautifulSoup
import requests
import time
import pymysql
import os
# chrome_options = Options()
class spider:
    def __init__(self,url=''):
        pass
        # self.connect = pymysql.connect(
        #     host="127.0.0.1",
        #     db="scrapy",
        #     user="root",
        #     passwd="root",
        #     charset='utf8',
        #     use_unicode=True
        # )
        # self.flag = True
        # self.start_time = time.time()
        self.url=url
        self.category_url=url


    def make_file(self,filename):
        # path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'
        if os.path.exists(filename):
            pass
        else:
            with open(filename, mode='w', encoding='utf-8') as ff:
                print("文件创建成功！")
    def write_txt(self,keyword, filename):
        self.make_file(filename)
        with open(filename, "a", encoding='utf-8') as f:
            f.write(keyword + '\n')
    #解析每个页面的内容并且进行下载图片和存入数据库
    def pare_lists_infos(self,next_url):
        response = requests.get(next_url)
        print('当前分页的url链接地址为:{}'.format(next_url))
        soup = BeautifulSoup(response.text, "html.parser")
        pages=soup.find('div',class_="pagenavi")
        keywords_list=soup.find('div',class_="service_area").find_all('li')
        filename= r'scrapy_data/ftsm.txt'
        for keywords in keywords_list:
            self.write_txt(keywords.text,filename)
            pass
        if pages:
            print('有分页')
            pages_a=pages.find_all('a')
            page_num_list=[]
            for pages_num in pages_a:
                page_num_list.append(pages_num.text)
            all_pages=[]
            for content in pages.contents:
                if content.string.strip():
                    all_pages.append(content.string.strip())
            current_page =int([x for x in all_pages if x not in page_num_list][0])
            next_page=current_page+1
            if str(next_page) in page_num_list:
                next_page_url=self.category_url+'index{}.html'.format(next_page)
                self.pare_lists_infos(next_page_url)
        else:
            print('没有分页')



    def page_list_url(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        product_list=soup.findAll('div',class_="footer_widget")[0]
        url_list=product_list.find_all('li')
        for url in url_list:
            category_url=url.find('a').get('href')
            category_url=self.url+category_url
            print('当前类别的url链接地址为:{}'.format(category_url))
            self.category_url=category_url
            self.pare_lists_infos(category_url)
        pass
if __name__=="__main__":
    url='https://www.sfsm.ch'
    spider = spider(url)
    # spider.page_list_url(url)
    # url='https://www.sfsm.ch/zimbabwe/'
    # url='https://www.sfsm.ch/zimbabwe/index2.html'
    # url='https://www.sfsm.ch/zimbabwe/index3.html'
    spider.page_list_url(url)
