# -*- coding: utf-8 -*-
import scrapy
from zjac_mongo.items import ZjacMongoItem
import os

class AcSpider(scrapy.Spider):
    name = 'ac'
    allowed_domains = ['zerojudge.tw']
    login_url = 'https://zerojudge.tw/Login'
    start_urls = [login_url]    
    logout_url = 'https://zerojudge.tw/Logout'
    user_url = 'https://zerojudge.tw/UserStatistic?account=%s'
    
    def parse(self, response):
        data = {
            'account' : '你的帳號',  #登入zerojudge帳號
            'passwd' : '你的密碼',  #登入zerojudge密碼
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_user)  #登入zerojudge取出指定的使用者AC題數
             
    def parse_user(self, response):
        userlist=['指定的帳號1','指定的帳號2','指定的帳號3']  #學生帳號名稱串列
        for user in userlist:
            yield scrapy.Request(url=self.user_url % user , callback = self.parse_user_process)  #呼叫https://zerojudge.tw/UserStatistic?account=%s抓出使用者AC題數
            
    def parse_user_process(self, response):
        item = ZjacMongoItem()
        account = response.xpath('//button/@data-receiver').extract_first()  #取出button的屬性data-receiver值為zerojudge帳號
        ac = response.xpath('//p[@align="left"]/a/text()').extract_first()  #取出p的屬性align為left的標籤a所包夾的文字為AC題數
        acitems = response.xpath('//a[@id="acstyle"]/text()').extract()
        print(acitems)
        item['acc'] = account
        item['ac'] = ac
        item['acitems'] = acitems
        return item