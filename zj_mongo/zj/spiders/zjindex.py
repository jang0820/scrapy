# -*- coding: utf-8 -*-
import scrapy


class ZjindexSpider(scrapy.Spider):
    name = 'zjindex'
    allowed_domains = ['zerojudge.tw']
    index_url = 'https://zerojudge.tw/Index'
    start_urls = [index_url]    
    
    def parse(self, response):
        filename = 'index.txt'
        with open(filename, 'wb') as f: #找出最近新增的題目標題與網址
            title = response.xpath('//div[@id="LatestProblem"]/table/tbody/tr/td/a/text()').extract()  #取出題目標題
            url = response.xpath('//div[@id="LatestProblem"]/table/tbody/tr/td/a/@href').extract()   #取出網址
            result = zip(title, url)
            for a,b in result:  #將結果寫入檔案index.txt
                f.write(a.encode(encoding="utf-8", errors="ignore"))
                f.write('\r\n'.encode(encoding="utf-8", errors="ignore"))
                f.write(b.encode(encoding="utf-8", errors="ignore"))
                f.write('\r\n'.encode(encoding="utf-8", errors="ignore"))
