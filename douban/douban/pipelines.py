# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import pymongo

class DoubanPipeline(object):

    def open_spider(self, spider):
        '''连接monogodb并事先创建一个document'''
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.test
        self.db.student.insert_one({'_id': 1, '内容': '豆瓣抓取'})
        
    def close_spider(self, spider):      
        '''
        关闭，个人认为一般情况下没用处
        '''
        self.client.close()

    def process_item(self, item, spider):
        self.db.student.update_many({'_id': 1}, {'$set': {item['author']: item['title']}}, upsert=True)


    '''
    以下为存储为Excel文件代码，Excel文件需要提前建立
    '''

    '''
    def open_spider(self, spider):
        self.df = pd.read_excel('豆瓣.xlsx')
        self.df = pd.DataFrame(columns=['作者', '标题'])

    def process_item(self, item, spider):
        self.df = self.df.append({'作者': item['author'], '标题': item['title']}, ignore_index=True)
        self.df.to_excel('豆瓣.xlsx')
        return item
    '''

