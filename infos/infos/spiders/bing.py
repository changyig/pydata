import scrapy
from infos.items import InfosItem
class BingSpider(scrapy.Spider):
    name = 'bing'
    # allowed_domains = ['www.zurgutenquelle2.de']
    # start_urls = ['https://www.zurgutenquelle2.de/solutions/stone_crushing_production_line.html']
    allowed_domains = ['www.bing.com']
    start_urls = ['https://www.bing.com/search?q=used+trommel+screeners+for+sale&ensearch=1&mkt=zh-CN&first=1&FORM=PERE']


    def parse(self, response):
        item=InfosItem()
        # print(response.xpath('//h1').get())
        # print(response.xpath('//div[@class="pro_in"]'))
        # print(response.xpath('//div[@class="pro_in"]').get())
        print('获取到的数据')
        item['content']=response.css('h2').get()
        print(response.css('h2').get())
        # yield item
        # print(response.css('h1').get())
        print(response.status)
        pass
