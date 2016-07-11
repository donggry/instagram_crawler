# -*- coding: utf-8 -*-
#-*- coding: euc-kr -*-
import scrapy
import json
import urllib
import os
import sys
import sys####
reload(sys)####
sys.setdefaultencoding('utf-8')####
from scrapy import Spider, Item, Field
from elasticsearch import Elasticsearch
#greedeat
#bobstagramh_
count=0
class InstagramProfileItems(Item):
    posts = Field()
    likes=Field()
    date=Field()
class InstagramSpider(scrapy.Spider):
    name = "textmove"  # Name of the Spider, required value
    #category = open("/home/eunsoo/Downloads/tutorial/tutorial/trainingdata.txt", "w")
    def __init__(self):
        self.account = 'gwang_ju_food'

        self.start_urls = ["https://www.instagram.com/"+self.account]

    # Entry point for the spider
    def parse(self, response):

        request = scrapy.Request(response.url, callback=self.parse_page)
        return request

    # Method for parsing a page
    def parse_page(self, response):

        js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]


        locations = json.loads(jscleaned)

        item = InstagramProfileItems()


        has_next = locations['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page']

        media = locations['entry_data']['ProfilePage'][0]['user']['media']['nodes']

        #es = Elasticsearch()
        global count
       # print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
        for posts in media:
            item["posts"]=posts['caption']
            item["likes"] = posts['likes']['count']
            item["date"]=posts['date']
           # print "BBBBBBBBBBBBBBBBBBBBB"/home/eunsoo/Downloads/tutorial/tutorial/spiders/training_insta_greedeat
            #words = item['posts'].encode('utf-8').split()
            strr="/home/eunsoo/Downloads/tutorial/tutorial/spiders/training_insta_greedeat/training_gwang_ju_food"+str(count)+".txt"
           # print "AAAAAAAAAAAAAAAAAAAA"
            #print strr
            category = open(strr, "w")
            category.write(item["posts"])
            category.close()
            #self.category.write("\n")
            count=count+1



        if has_next:
            url="https://www.instagram.com/"+self.account+"/?max_id="+media[-1]['id']
            yield scrapy.Request(url, callback=self.parse_page)