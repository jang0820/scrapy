# -*- coding: utf-8 -*-
import scrapy
import json
from twse_mysql.items import TwseMysqlItem
import time
import datetime

class TwseSpider(scrapy.Spider):
    name = 'twse'
    allowed_domains = ['www.twse.com.tw']
    start_urls = []
    
    def __init__(self):
        dates = []
        years = [2017, 2018]
        today = datetime.datetime.now()
        for y in years:
            if y < int(today.year):
                for m in range(1, 13):  #產生去年以前的年與月
                    if m < 10:
                        s = str(y) + '0' + str(m) +'01'
                    else:
                        s = str(y) + str(m) +'01'
                    dates.append(s)
            if y ==  int(today.year):   #產生今年的年與月
                for m in range(1, int(today.month)+1):
                    if m < 10:
                        s = str(y) + '0' + str(m) +'01'
                    else:
                        s = str(y) + str(m) +'01'
                    dates.append(s)
        stockno_list = ['2892','2330']
        for stockno in stockno_list:
            for date in dates:
                url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % ( date, stockno)  #產生證交所所需要的股票與日期的網址
                self.start_urls.append(url)
    
    def transform_date(self, date):  #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d
    
    def transform_data(self, data):
        data[0] = datetime.datetime.strptime(self.transform_date(data[0]), '%Y/%m/%d')
        data[1] = int(data[1].replace(',', ''))#把千進位的逗點去除
        data[2] = int(data[2].replace(',', ''))
        data[3] = float(data[3].replace(',', ''))
        data[4] = float(data[4].replace(',', ''))
        data[5] = float(data[5].replace(',', ''))
        data[6] = float(data[6].replace(',', ''))
        data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
        data[8] = int(data[8].replace(',', ''))
        return data

    def transform(self, data):   #進行資料格式轉換
        return [self.transform_data(d) for d in data]
    
    def parse(self, response):
        data_src = json.loads(response.body_as_unicode()) #將json轉換成python的字典結構
        stockno = response.url[-4:]  #取出股票代碼
        item = TwseMysqlItem()  #定義在items.py
        data = self.transform(data_src['data'])
        for d in data:
            item['date'] = d[0]         #資料與item結合，會傳到pipeline進行處理
            item['stockno'] = stockno
            item['shares'] = d[1]
            item['amount'] = d[2]
            item['open'] = d[3]
            item['close'] = d[4]
            item['high'] = d[5]
            item['low'] = d[6]
            item['diff'] = d[7]
            item['turnover'] = d[8]
            yield item
        
