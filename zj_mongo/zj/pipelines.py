# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from zj import settings
from zj.items import ZjItem
from scrapy import log
from scrapy.exceptions import DropItem

class ZjPipeline(object):
    def __init__(self):  #連線MongoDB，設定值儲存在settings.py
        connection = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = connection[settings.MONGODB_DB]  #指定資料庫
        self.collection = db[settings.MONGODB_COLLECTION]   #指定collection，相當於資料表

    def process_item(self, item, spider):
        self.collection.insert(dict(item))  #插入資料
        return item
