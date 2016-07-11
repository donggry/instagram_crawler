# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
import os
import sys
from scrapy import Spider, Item, Field
from elasticsearch import Elasticsearch
count=0
class InstagramProfileItems(Item):
    posts = Field()
    likes=Field()
    date=Field()
class InstagramSpider(scrapy.Spider):
    name = "test"  # Name of the Spider, required value
    def __init__(self):
        self.account = 'dok2gonzo'

        self.start_urls = ["https://www.instagram.com/"+self.account]

    def parse(self, response):

        request = scrapy.Request(response.url, callback=self.parse_page)
        return request

    def parse_page(self, response):
        print "QQQQQQQQQQQQQQQQQ"
        #print response.selector.xpath('//').extract()
        js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
        #test=response.selector.xpath('//div[@class="_pupj3"]/a/text()').extract()
        print "EEEEEEEEEEEEEEEEEEEE"
        js = js[0].replace("window._sharedData = ", "")
        print "WWWWWWWWWWWWWWWWWWWWWWw"
        print "TTTTTTTTTTTTTTT\n"
        jscleaned = js[:-1]
        print jscleaned

        locations = json.loads(jscleaned)
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
            strr = "/home/eunsoo/Downloads/tutorial/tutorial/spiders/training_insta_greedeat/hongik" + str(
                count) + ".txt"
            category = open(strr, "w")
            category.write(item["posts"])
            category.close()
            count=count+1
            print count

        if has_next:
            url = "https://www.instagram.com/" + self.account + "?max_id=" + has_next2['end_cursor']
            yield scrapy.Request(url, callback=self.parse_page)



