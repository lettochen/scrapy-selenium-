# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from my_fake_useragent import UserAgent
import random
import settings


class DoubanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware(object):

    def __init__(self):
        self.count = 0

        '''无标题模式'''
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(3)
        self.driver.get('https://www.douban.com')

        '''跳转到frame'''
        frame = self.driver.find_element_by_xpath('//body//div[@class="login"]/iframe')
        self.driver.switch_to.frame(frame)

        try:
            self.driver.find_element_by_xpath('//body/div[1]/div[1]/ul[1]/li[2]').click()
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//input[@id="username"]').send_keys('15079076306')
            self.driver.find_element_by_xpath('//input[@id="password"]').send_keys('doubanlaji1')
            self.driver.find_element_by_xpath('//div[@class="account-form-field-submit "]').click()
            '''设置等待响应时间'''
            time.sleep(1)

        #如果没找到对应元素，再找一遍
        except NoSuchElementException as e:
            print('再加载一遍: %s' % e)
            self.driver.find_element_by_xpath('//body/div[1]/div[1]/ul[1]/li[2]').click()
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//input[@id="username"]').send_keys('xxx')
            self.driver.find_element_by_xpath('//input[@id="password"]').send_keys('xxx')
            self.driver.find_element_by_xpath('//div[@class="account-form-field-submit "]').click()
            time.sleep(1)

        else:
            print('Successful logging!')

    def process_request(self, request, spider):
        '''特殊的标记，只是运行一次，用来登录'''
        self.count += 1
        if self.count <= 1:
            return HtmlResponse(url=request.url, status=200, request=request,
                                encoding='utf-8', body=self.driver.page_source)

        #添加User-Agent，用了第三方库:my_fake_useragent
        else:
            ua = UserAgent(family='chrome', os_family='Windows')
            res = ua.random()
            request.headers['User-Agent'] = res

            '''下面也可以添加随机IP，要先在settings中写好代理池PROXIES'''

            '''
            proxies = settings.PROXIES
            proxy = random.choice(proxies)
            request.meta['proxy'] = proxy            
            '''
