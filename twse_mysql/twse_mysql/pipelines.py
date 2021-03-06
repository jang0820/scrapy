# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twse_mysql import settings
from twse_mysql.items import TwseMysqlItem

class TwseMysqlPipeline(object):
    def __init__(self):   #連線資料庫，資料庫相關設定值放在settings.py
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASS,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        
    def process_item(self, item, spider):
        if item.__class__ == TwseMysqlItem:   #將不同Item插入不同的資料庫
            try:
                self.cursor.execute("select * from twse where date = '%s' and stockno = '%s'" % (item['date'], item['stockno'])) #檢查是否已經在資料庫內
                ret = self.cursor.fetchone()
                if not ret:  #如果沒有在資料庫內
                    insertsql = "INSERT INTO twse (date, stockno, shares, amount, open, close, high, low, diff, turnover) VALUES ('%s', '%s', %ld, %ld, %f, %f, %f, %f, %f, %d)" % (item['date'], item['stockno'], int(item['shares']), int(item['amount']), float(item['open']), float(item['close']), float(item['high']), float(item['low']), float(item['diff']), int(item['turnover']))  #新增一筆資料的SQL
                    self.cursor.execute(insertsql)  #插入到資料庫
                    self.connect.commit()  #資料庫有變更時，需要commint才會執行，select不需要commit
            except Exception as error:
                self.connect.rollback()   #發生錯誤，則退回上一次資料庫狀態
            return item