# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from zjac_mongo import settings
from zjac_mongo.items import ZjacMongoItem
from scrapy.exceptions import DropItem

class ZjacMongoPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        if item.__class__ == ZjacMongoItem:   #將不同Item插入不同的資料庫
            if self.collection.find({"acc": item['acc']} ).count() == 0:  #找尋資料是否已經在Mongo，如果不存在
                self.collection.insert_one(dict(item))  #插入資料到資料庫
            else:  #已經存在資料庫
                self.collection.update({"acc": item['acc']}, dict(item))  #更新資料到資料庫
            return item
