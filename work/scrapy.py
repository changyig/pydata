from bs4 import BeautifulSoup
import requests
import os
def make_file(filename):
    # path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'
    if os.path.exists(filename):
        pass
    else:
        with open(filename, mode='w', encoding='utf-8') as ff:
            print("文件创建成功！")
def write_txt(keyword,filename):
    make_file(filename)
    with open(filename, "a", encoding='utf-8') as f:
        f.write(keyword+'\n')

def read_url():
    filename='../data/url/keyword.txt'
    sitemap_url='../data/url/url.txt'
    log_txt='../data/url/log.txt'
    url = 'https://www.urbanjournalism.de/sitemap.xml'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    count = soup.find_all(name="loc")
    num = 0
    for i in count:
        url_text=i.string
        print('开始sitemap地图：'+i.string)
        res = requests.get(url_text)
        soup2 = BeautifulSoup(res.text, "html.parser")
        keyword_url = soup2.find_all(name="loc")
        for word in keyword_url:
            keyword_url=word.string
            write_txt(keyword_url,sitemap_url)
            keyword_html = requests.get(keyword_url)
            keyword = BeautifulSoup(keyword_html.text, "html.parser")
            title = keyword.title.string
            write_txt(title,filename)
            print('当前编号'+str(num)+'当前url:'+keyword_url)
            log_message='当前编号'+str(num)+'当前url:'+keyword_url+'当前h1标签:'+title
            write_txt(log_message,log_txt)
            num=num+1
            # print('暂停')
            # break
            # print(keyword)
read_url()