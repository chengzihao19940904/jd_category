#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Date:2018/4/27
import scrapy
from tutorial.items import TutorialItem
from tutorial.items import CateItem
from scrapy_splash import SplashRequest
import re
import json
class muke_spider(scrapy.Spider):
    name = 'muke'
    allowed_domains = ['www.jd.com']
    # start_urls = [
    #     'https://www.jd.com/'
    # ]
    start_urls = [
    'https://dc.3.cn/category/get']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "www.zhihu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
    }

    root_domains = 'https://www.jd.com/'

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url=url, callback=self.parse,
    #                             args={'wait':1})

    def parse(self,response):

        data = json.loads(response.body.decode("gbk"))['data']
        for item in data:
            #主类标签
            cate_c = item['id'] 
            for second_item in item['s']:
                item = CateItem()
                item['main_cate'] = cate_c
                second = second_item['n'].split('|')
                item['url'] = second[0]
                item['name'] = second[1]
                item['child'] = []
                for third_item in second_item['s']:
                    third = third_item['n'].split('|')
                    if not re.search('list.html',third[0]):
                        third[0] = "http://list.jd.com/list.html?cat="+third[0].replace('-',',')
                    tir = {'url':third[0],'name':third[1]}
                    item['child'].append(tir)
                yield item




        
        # print(response.xpath('//div[@id="J_popCtn"]/div[contains(@class,"cate_part")]').extract())
        # for res in response.xpath('//div[@class="cate_detail"]'):
        #     print(res.extract())
        #     item = TutorialItem()
        #     item['title'] = res.xpath('a/div/h3/text()').extract()[0]
        #     item['content'] = res.xpath('a/div//p/text()').extract()[0]
        #     item['img'] = 'http:'+res.xpath('a/div/img/@src').extract()[0]
        #     item['label'] = ','.join(res.xpath('a//div[@class="course-label"]/label/text()').extract())
        #     user = res.xpath('a//div[@class="course-card-info"]/span/text()').extract()
        #     item['student'] = user[-1]
        #     item['level'] = user[0]
        #     yield item

        # next_url = response.xpath('//a[contains(text(),"下一页")]/@href').extract()
        # if next_url:
        #     page = self.root_domains+next_url[0]
        #     yield scrapy.Request(page,callback=self.parse)





