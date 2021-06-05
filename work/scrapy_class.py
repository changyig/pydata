from bs4 import BeautifulSoup
import requests
import os
from string_class import HandleStr
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
class Scrapy:
    '''
          #说明：①需要遍历组装的文件夹目录（self.readdir）
          #说明：②将新组装txt文件放入的目录（self.writedir）
          #说明：③将新组装txt文件写入的文件名字（self.write_filename）
          #说明：④读取文件的名字（self.read_filename）
    '''
    def __init__(self,Strclass=None):
        self.read_filename=''
        self.write_filename= 'scrapy_data/sitemap_url.txt'
        self.readdir=r''
        self.writedir=r''
        self.url='https://ardek.pl/sitemap.xml'
        # self.url='https://www.polyvert.it/sitemap.xml'
        self.open_filename=False
        self.Strclass=Strclass
    '''
       #说明：判断文件是否存在 不存在便创建文件
    '''
    def make_file(self,filename):
        if os.path.exists(filename):
            pass
        else:
            with open(filename, mode='w', encoding='utf-8') as ff:
                print("文件创建成功！")

    '''
       #说明：向指定文件中写入内容
    '''
    def write_txt(self,filename,keyword ):
        self.make_file(filename)
        with open(filename, "a", encoding='utf-8') as f:
            f.write(keyword.strip('\n') + '\n')
        # if self.open_filename :
        #     self.open_filename.write(keyword+ '\n')
        # else:
        #     self.make_file(filename)

    '''
     #说明：清空txt文本
    '''
    def empty_txt(self):
        open(self.write_filename, 'w').close()

    '''
       #说明: 根据站点地图中的url读取相应的内容 并且存入到指定的文件中
       #说明:sitemap.xml-->url-->request.get-->titile-->txt
    '''
    def read_sitemap_keyword(self):
        url = self.url
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        count = soup.find_all(name="loc")
        num = 0
        print(count)
        try:
            for i in count:
                url_text = i.string
                print('开始sitemap地图：' + i.string)
                res = requests.get(url_text)
                soup2 = BeautifulSoup(res.text, "html.parser")
                keyword_url = soup2.find_all(name="loc")
                for word in keyword_url:
                    try:
                        keyword_url = word.string
                        keyword_html = requests.get(keyword_url)
                        keyword = BeautifulSoup(keyword_html.text, "html.parser")
                        title = keyword.title.string
                        h1 = keyword.find('h1').string
                        log_message = '当前编号' + str(num) + '当前url:' + keyword_url + '当前t标签:' + title
                        print('当前编号:{},当前url:{},当前h1标签:{},当前title标题:{}'.format(str(num),keyword_url,h1,title))
                        # self.write_txt(self.write_filename, h1)
                        self.write_txt(self.write_filename, title)
                        # if num==2:
                        #     break
                        num = num + 1
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)

    '''
      #说明: 根据站点地图网址，读取所有的链接并且存入指定的文件中
      #流程:sitemap.xml-->sitemap(1,2,3..).xml-->url-->txt
   '''
    def sitemap_url_txt(self):
        url = self.url
        filename=self.write_filename
        r = requests.get(url)
        # soup = BeautifulSoup(r.content.decode("utf-8-sig").encode("utf-8"), "xml")
        soup = BeautifulSoup(r.text, "xml")
        count = soup.find_all(name="loc")
        num = 0
        for i in count:
            url_text = i.string
            res = requests.get(url_text)
            soup2 = BeautifulSoup(res.text, "xml")
            # soup2 = BeautifulSoup(res.content.decode("utf-8-sig").encode("utf-8"), "xml")
            keyword_url = soup2.find_all(name="loc")
            for url in keyword_url:
                url = url.string
                # print(url)
                self.write_txt(filename,url)

    '''
          #说明: 根据站点地图网址，读取所有的链接并且存入指定的文件中
          #流程:sitemap.xml-->sitemap(1,2,3..).xml-->sitemap.xml-->url-->txt
    '''

    def sitemap_3_url_txt(self):
        url = self.url
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"xml")
        count = soup.find_all(name="loc")
        for i in count:
            url_text = i.string
            res = requests.get(url_text)
            soup2 = BeautifulSoup(res.text,"xml")
            sitemap_site = soup2.find_all(name="loc")
            for sitemap in sitemap_site:
                res = requests.get(sitemap.string)
                soup3 = BeautifulSoup(res.text,"xml")
                keyword_url = soup3.find_all(name="loc")
                for url in keyword_url:
                    url = url.string
                    print(url)
                    filename = self.write_filename
                    self.write_txt(filename,url)

    '''
          #说明: 根据站点地图网址，读取所有的链接并且存入指定的文件中
          #流程:sitemap.xml-->sitemap(1,2,3..).xml-->url(过滤功能)-->txt
       '''

    def sitemap_zh_url_txt(self):
        url = self.url
        filename = self.write_filename
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"xml")
        keyword_url = soup.find_all(name="loc")
        for url in keyword_url:
            url = url.string
            print(url)
            res = self.Strclass.search_str(url)
            if res:
                self.write_txt(filename,url)
    '''
         #说明: 根据站点地图网址，读取所有的链接并且存入指定的文件中
         #流程:sitemap.xml-->url-->存储到txt
      '''

    def sitemap_url(self):
        url = self.url
        filename = self.write_filename
        r = requests.get(url,timeout=10)
        soup = BeautifulSoup(r.text,"xml")
        keyword_url = soup.find_all(name="loc")
        for url in keyword_url:
            url = url.string
            print(url)
            self.write_txt(filename,url)

    '''
      #说明:根据抓取到的链接地址eg:https://test.in/13096/machine_needed_for_stone_crushing_plant.html 将关键词进行分析存储起来
      #流程:打开文件-->读取url-->keyword解析-->存储
    '''
    def test(self,filename=''):
        write_filename='scrapy_data/in.txt'
        with open(filename,mode='r',encoding='utf-8') as ff:
            for url in ff.readlines():
                path1 = url.split('/')[-1]
                str_list = path1.replace('.html','').split('_')
                keyword = ' '.join(str_list)
                self.write_txt(write_filename,keyword)

    '''
     #说明:根据抓取到的链接地址eg:https://test.in/13096/machine_needed_for_stone_crushing_plant.html 将关键词进行分析存储起来
     #流程:打开文件-->读取url-->keyword解析-->存储
    '''

    def get_str_string(self,filename=''):
        write_filename = 'scrapy_data/www.gim2pno.pl.txt'
        with open(filename,mode='r',encoding='utf-8') as ff:
            for url in ff.readlines():
                url=url.strip()
                if url:
                    # print(url)
                    keyword=self.Strclass.get_str(url)
                    # print(keyword)
                    self.write_txt(write_filename,keyword)
    def run_sitemap(self,sitemap=''):
        self.url=sitemap
        self.empty_txt()
        self.sitemap_url_txt()
        return True

    '''
      #说明: 根据站点地图网址，读取所有的链接并且提取其中的指定的内容到指定的文件中
      #流程:sitemap.xml-->sitemap(1,2,3..).xml-->url（提取其中的内容）-->txt
   '''

    def sitemap_url_sort_txt(self):
        url = self.url
        filename = self.write_filename
        r = requests.get(url)
        # soup = BeautifulSoup(r.content.decode("utf-8-sig").encode("utf-8"), "xml")
        soup = BeautifulSoup(r.text,"xml")
        count = soup.find_all(name="loc")
        num = 0
        dict_sort={}
        for i in count:
            url_text = i.string
            res = requests.get(url_text)
            soup2 = BeautifulSoup(res.text,"xml")
            # soup2 = BeautifulSoup(res.content.decode("utf-8-sig").encode("utf-8"), "xml")
            keyword_url = soup2.find_all(name="loc")
            for url in keyword_url:
                sort = self.Strclass.get_url_sort(url.string)
                if sort :
                    if sort in dict_sort:
                        dict_sort[sort]=dict_sort[sort]+1
                    else:
                        dict_sort[sort] =1
        print(dict_sort)

if __name__=='__main__':
    filename='https://www.numismaticaleuven.be/sitemap.xml'
    # Strclass=HandleStr()
    # scrapy = scrapy(Strclass)
    scrapy = Scrapy()
    #英文sitemap站点地图获取
    # scrapy.empty_txt()
    # scrapy.sitemap_url_txt()
    scrapy.run_sitemap(filename)
    # scrapy.sitemap_3_url_txt()
    # scrapy.get_str_string('scrapy_data/sitemap_url.txt')
    #中文sitemap站点地图获取
    # scrapy.sitemap_zh_url_txt()
    # scrapy.test(filename)
    print('结束执行')