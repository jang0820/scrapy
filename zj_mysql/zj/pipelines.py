# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log
from zj import settings
from zj.items import ZjItem

class ZjPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASS,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == ZjItem:   #將不同Item插入不同的資料庫
            try:
                self.cursor.execute("""select * from ac where acc = %s""", item["acc"])   #是否已經在資料庫內
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute("""update ac set ac = %s where acc = %s""", (item['ac'], item['acc']))  #若存在，則更新
                else:
                    self.cursor.execute("""insert into ac(acc,ac) value (%s, %s)""", (item['acc'], item['ac']))  #若不存在，則插入
                self.connect.commit()
            except Exception as error:
                self.connect.rollback()  #發生錯誤，則退回上一次資料庫狀態
                log(error)
            return item
