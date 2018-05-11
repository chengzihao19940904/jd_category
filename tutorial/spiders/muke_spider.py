#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Date:2018/4/27
import scrapy
from tutorial.items import TutorialItem
from tutorial.items import CateItem
from tutorial.items import GoodsListItem
from scrapy_splash import SplashRequest
import re
import json
class muke_spider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['www.jd.com',"search.jd.com","item.jd.com","club.jd.com",""]
    # start_urls = [
    #     'https://www.jd.com/'
    # ]

    base_url = "https://list.jd.com/"
    start_urls = [
    'https://dc.3.cn/category/get'
    ]
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
                # item = CateItem()
                # item['main_cate'] = cate_c
                second = second_item['n'].split('|')
                # item['url'] = second[0]
                # item['name'] = second[1]
                # item['child'] = []
                for third_item in second_item['s']:
                    third = third_item['n'].split('|')
                    if not re.search('list.html',third[0]):
                        third[0] = "http://list.jd.com/list.html?cat="+third[0].replace('-',',')
                    
                    if not re.search('http://',third[0]):
                        third[0] = "http://"+third[0]
                    # tir = {'url':third[0],'name':third[1]}
                    # item['child'].append(tir)
                    yield SplashRequest(third[0].strip(),meta={'thirdCateName':third[1],'thirdUrl':third[0],'secondName':second[1],'secondUrl':second[0],'main_cate':cate_c},callback=self.parse_item,dont_filter=True)
                
    def parse_item(self,response):
        for ret in response.xpath('//ul[contains(@class,"gl-warp")]/li[contains(@class,"gl-item")]'):
            item = GoodsListItem()
            item['main_cate'] = response.meta['main_cate']
            item['thirdCateName'] = response.meta['thirdCateName']
            item['thirdUrl'] = response.meta['thirdUrl']
            item['secondName'] = response.meta['secondName']
            item['secondUrl'] = response.meta['secondUrl']
            item['imgUrl'] = "".join(ret.xpath('div/div[contains(@class,"p-img")]/a/img/@src').extract())
            item['price'] ="".join(ret.xpath('div/div[@class="p-price"]/strong[@class="J_price"]/i/text()').extract())
            item['title'] ="".join(ret.xpath('div/div[@class="p-name"]/a/em/text()').extract()).strip()
            item['words'] = "".join(ret.xpath('div/div[@class="p-name"]/a/@title').extract())
            item['shop_name'] = "".join(ret.xpath('div/div[@class="p-shop"]/span/a/@title').extract())
            # tipsRet = ret.xpath('div/div[contains(@class,"p-icons")]')
            tips = ret.xpath('div/div[contains(@class,"p-icons")]/i/@data-tips').extract()
            item['tips'] =  "|".join(tips)
            item['detail_url'] = "".join(ret.xpath('div/div[contains(@class,"p-img")]/a/@href').extract())
            yield item

        next_url = response.xpath('//a[@class="pn-next"]/@href').extract()
        if next_url:
            page = self.root_domains+next_url[0]
            yield SplashRequest(page,meta={'thirdCateName':response.meta['thirdCateName'],'thirdUrl':response.meta['thirdUrl'],'secondName':response.meta['secondName'],'secondUrl':response.meta['secondUrl'],'main_cate':response.meta['main_cate']},callback=self.parse_item,dont_filter=True)


