# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InfosItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    print('item')
    pass

