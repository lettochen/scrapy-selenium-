# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    start_urls = ['https://www.douban.com']

    '''
    第一次的response默认返回给parse()，并且这里也只运行一次
    '''
    def parse(self, response):
        contents = response.xpath('//body//div[@class="new-status status-wrapper    "]')
        for content in contents:
            item = DoubanItem()
            item['author'] = content.xpath('.//div[@class="text"]/a/text()').get()
            item['title'] = content.xpath('.//div[@class="title"]/a/text()').get()
            yield item