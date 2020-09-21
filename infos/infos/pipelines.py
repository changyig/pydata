# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter



class InfosPipeline:
    def __init__(self):
        # 创建数据库链接
        self.client = pymysql.Connect(
            '127.0.0.1', 'root', 'root',
            'pydata', 3306, charset='utf8'
        )
        # 创建游标
        self.cursor = self.client.cursor()

    def open_spider(self, spider):
        print('爬虫开启')
        pass
    def process_item(self, item, spider):
        # # 往数据库里写
        sql = """
            insert into data(content) values (%s)
        """
        # sql, data = item.get_insert_sql_data(data_dict)
        # try:
        #     self.cursor.execute(sql, (item['content']))
        #     self.client.commit()
        # except Exception as err:
        #     self.client.rollback()
        #     print(err)
        # 如果有多个管道文件,一定要return item , 否则下一管道无法接收到item
        print('经过了管道')
        return item

    def close_spider(self, spider):
        '''
        爬虫结束的时候调用一次
        :param spider:
        :return:
        '''
        self.cursor.close()
        self.client.close()
        print('爬虫结束')
