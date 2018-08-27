# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from twse_mongo import settings
from twse_mongo.items import TwseMongoItem
from pymongo import MongoClient

class TwseMongoPipeline(object):
    def __init__(self):
        self.client = MongoClient(settings.MONGO_HOST, 27017)
        self.db = self.client[settings.MONGO_DB]
        self.collection = self.db[settings.MONGO_COLLETION]
        
    def process_item(self, item, spider):
        if item.__class__ == TwseMongoItem:   #將不同Item插入不同的資料庫
            if self.collection.find({"date": item['date'], "stockno": item['stockno']} ).count() == 0:  #找尋資料是否已經在Mongo
                element={'date':item['date'], 'stockno':item['stockno'], 'shares':item['shares'], 'amount':item['amount'], 'open':item['open'], 'close':item['close'], 'high':item['high'], 'low':item['low'], 'diff':item['diff'], 'turnover':item['turnover']};  #一天的股價與成交量
                self.collection.insert_one(element)  #插入資料到資料庫
            return item
