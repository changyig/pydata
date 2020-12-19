from bs4 import BeautifulSoup
import requests
import os
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
class scrapy:
    '''
          #说明：①需要遍历组装的文件夹目录（self.readdir）
          #说明：②将新组装txt文件放入的目录（self.writedir）
          #说明：③将新组装txt文件写入的文件名字（self.write_filename）
          #说明：④读取文件的名字（self.read_filename）
    '''
    def __init__(self):
        self.read_filename=''
        self.write_filename= 'scrapy_data/montometservice.pl.txt'
        self.readdir=r''
        self.writedir=r''
        self.url='https://www.montometservice.pl/sitemap.xml'
        self.open_filename=False
    '''
       #说明：判断文件是否存在 不存在便创建文件
    '''
    def make_file(self,filename):
        if os.path.exists(filename):
            pass
        else:
            with open(filename, mode='w', encoding='utf-8') as ff:
                print("文件创建成功！")
        # if os.path.exists(filename):
        #     self.open_filename=open(filename, mode='w', encoding='utf-8')
        #     print('第一种刚开启文件:{}'.format(filename))
        # else:
        #     if self.open_filename :
        #         pass
        #     else:
        #         self.open_filename=open(filename, mode='w', encoding='utf-8')
        #         print('第二种刚开启文件:{}'.format(filename))

    '''
       #说明：向指定文件中写入内容
    '''
    def write_txt(self,filename,keyword ):
        self.make_file(filename)
        with open(filename, "a", encoding='utf-8') as f:
            f.write(keyword + '\n')
        # if self.open_filename :
        #     self.open_filename.write(keyword+ '\n')
        # else:
        #     self.make_file(filename)

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
      #流程:sitemap.xml-->url-->txt
   '''
    def sitemap_url_txt(self):
        url = self.url
        filename=self.write_filename
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "xml")
        count = soup.find_all(name="loc")
        num = 0
        for i in count:
            url_text = i.string
            res = requests.get(url_text)
            soup2 = BeautifulSoup(res.text, "xml")
            keyword_url = soup2.find_all(name="loc")
            for url in keyword_url:
                url = word.string
                self.write_txt(filename,url)
if __name__=='__main__':
    scrapy = scrapy()
    scrapy.read_sitemap_keyword()
    print('结束执行')