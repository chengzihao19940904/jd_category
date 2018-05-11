# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    label = scrapy.Field()
    student = scrapy.Field()
    level = scrapy.Field()
    img = scrapy.Field()
    image_path = scrapy .Field()
    pass

class CateItem(scrapy.Item):
    main_cate = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    child = scrapy.Field()
    pass

class GoodsListItem(scrapy.Item):
    main_cate = scrapy.Field()
    thirdCateName = scrapy.Field()
    thirdUrl = scrapy.Field()
    secondName = scrapy.Field()
    secondUrl = scrapy.Field()
    imgUrl = scrapy.Field() #图片地址
    title = scrapy.Field()  #标题
    price = scrapy.Field()  #价格
    words = scrapy.Field()  #关键词
    shop_name = scrapy.Field()  #店铺名称
    tips = scrapy.Field()   
    detail_url = scrapy.Field() #详情url
    pass
