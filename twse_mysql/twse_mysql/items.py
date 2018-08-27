# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwseMysqlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    stockno = scrapy.Field()
    shares = scrapy.Field()
    amount = scrapy.Field()
    open = scrapy.Field()
    close = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    diff = scrapy.Field()
    turnover = scrapy.Field()
