# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
import os
import sys
from scrapy import Spider, Item, Field
from elasticsearch import Elasticsearch
import numpy as np
count=0
class InstagramProfileItems(Item): #compile 명령:scrapy crawl "name"->name은 내가 정할 수 있다.
    posts = Field()
    likes=Field()
    date=Field()
    score=Field()
    id=Field()

class InstagramSpider(scrapy.Spider):
    name = "search_category"  #내가 정할 크롤러 이름
    category = open("/home/eunsoo/Downloads/tutorial/tutorial/category.txt", "r").read().split()

    def __init__(self):
        self.account = 'explore/tags/은수니/'
        self.start_urls = ["https://www.instagram.com/"+self.account]
        self.es = Elasticsearch()

    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        return request

    def parse_page(self, response):
        js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]
        locations = json.loads(jscleaned)
        print "aaaaaaaaaaaaaaaaa"
       # print locations
        print "BBBBBBBBBBBBBBBBBBBBBB"
        item = InstagramProfileItems()
        has_next = locations['entry_data']['TagPage'][0]['tag']['media']['page_info']['has_next_page']
        has_next2 = locations['entry_data']['TagPage'][0]['tag']['media']['page_info']
        media = locations['entry_data']['TagPage'][0]['tag']['media']['nodes']

        global count
        for posts in media:
            if("caption" in posts ):
                item["posts"] = posts['caption']
            item["likes"] = posts['likes']['count']
            item["date"] = posts['date']
            item["id"]=posts['code']
            print item['id']
           # item["score"]=self.scoring(item['likes'],item['date'])
           # words = item['posts'].encode('utf-8').split()

            """for word in words:
                word = word.replace("#", "")
                if (word in self.category):
                        self.es.index(index="instagram", doc_type="categorizedinstagram", id=count,
                            body={"contents": item["posts"], "likes": item["likes"], "date": item["date"],"category":word})
                        count = count + 1
                else:
                    self.es.index(index="instagram", doc_type="uncategorizedinstagram",
                             body={"contents": item["posts"], "likes": item["likes"], "date": item["date"]})
            yield item"""


        if has_next:
            url = "https://www.instagram.com/" + self.account + "?max_id=" + has_next2['end_cursor']
            yield scrapy.Request(url, callback=self.parse_page)

    def scoring(self,likes,date):
        return likes*date
