# -*- coding: utf-8 -*-
#-*- coding: euc-kr -*-
import scrapy
import json
import urllib
import os
import sys
import sys####
reload(sys)####1464877867
sys.setdefaultencoding('utf-8')####
from scrapy import Spider, Item, Field
from elasticsearch import Elasticsearch
count=3
class InstagramProfileItems(Item):
    posts = Field()
    likes=Field()
    date=Field()
class InstagramSpider(scrapy.Spider):
    name = "Instagram"  # Name of the Spider, required value
    category = open("/home/eunsoo/Downloads/tutorial/tutorial/category.txt", "r").read().split()
    def __init__(self):
        self.account = 'eundong933'

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
        print "BBBBBBBBBBBBBBB\n"
        print locations

        item = InstagramProfileItems()


        has_next = locations['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page']

        media = locations['entry_data']['ProfilePage'][0]['user']['media']['nodes']
        es = Elasticsearch()
        global count

        for posts in media:
            if ("caption" in posts):
                item["posts"] = posts['caption']
            item["likes"] = posts['likes']['count']
            item["date"]=posts['date']
            print item["date"]
            """words = item['posts'].encode('utf-8').split()

            for word in words:
                word=word.replace("#","")
                if(word in self.category):
                #for c in category:
                    #if word.find(unicode(c)) >= 0:
                    #es.index(index="testsns2", doc_type="uncategorizedinstagram", id=count,
                     #        body={"contents": item["posts"], "likes": item["likes"], "date": item["date"],"category":c})
                       # print word
                       # print "발견하였ㅅ븐띠아."
                        count = count + 1"""


        if has_next:
            url="https://www.instagram.com/"+self.account+"/?max_id="+media[-1]['id']
            print "aaaaaaaaaaaaaaA"
            print media[-1]['id']
            yield scrapy.Request(url, callback=self.parse_page)