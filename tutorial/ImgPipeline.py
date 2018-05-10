#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Date:2018/4/27
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
    
class ImgPipeline(ImagesPipeline):
#通过抓取的图片url获取一个Request用于下载
    def get_media_requests(self, item, info):
#返回Request根据图片图片url下载
        yield scrapy.Request(item['img'])
#当下载请求完成后执行该方法
    def item_completed(self, results, item, info):
#获取下载地址
        image_path = [x['path'] for ok, x in results if ok]
#判断是否成功
        if not image_path:
            raise DropItem("Item contains no images")
#将地址存入item
        item['img'] = image_path
        return item