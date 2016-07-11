# -- coding: utf-8 --
import scrapy
import json
import time as testtimecrawl
from scrapy import Spider, Item, Field
from elasticsearch import Elasticsearch

class InstagramProfileItems(Item): #compile 명령:scrapy crawl "name"->name은 내가 정할 수 있다.
    posts = Field()
    likes=Field()
    date=Field()
    score=Field()
    comments_count = Field()
    id=Field()

class InstagramSpider(scrapy.Spider):
    name = "instagram_search_trend"  #내가 정할 크롤러 이름
    category = open("/home/eunsoo/Downloads/tutorial/tutorial/category.txt", "r").read().split()

    def __init__(self):
        self.account = 'explore/tags/대세/'
        self.start_urls = ["https://www.instagram.com/"+self.account]
        self.es = Elasticsearch()
        self.start_time = testtimecrawl.time()
        three_month = 60*60*24*90
        self.limit_time = self.start_time -three_month

    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        return request

    def parse_page(self, response):
        js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]
        locations = json.loads(jscleaned)
        item = InstagramProfileItems()
        has_next = locations['entry_data']['TagPage'][0]['tag']['media']['page_info']['has_next_page']
        has_next2 = locations['entry_data']['TagPage'][0]['tag']['media']['page_info']
        media = locations['entry_data']['TagPage'][0]['tag']['media']['nodes']


        for posts in media:
            if("caption" in posts ):
                item["posts"] = posts['caption']
            if ("likes" in posts):
                item["likes"] = posts['likes']['count']
            if ("date" in posts):
                item["date"] = posts['date']
            else:
                item["date"] = 0
            if ("comments" in posts):
                item["comments_count"] = posts['comments']['count']
            else: # 댓글 없는 경우 처리
                item["comments_count"] = 0

            item["id"]=posts['code']

            words = item['posts'].encode('utf-8').replace("#", " ").split()

            """scoring 하는 부분"""
            score_time = (self.start_time - item["date"]) / (60*60*24) # 2일
            score_likes = 0
            if ("likes" in posts):
                score_likes = item["likes"]
            score_comments = 0
            if ("comments" in posts):
                score_comments = item['comments_count']
            score = (score_likes + score_comments) / (score_time)*10
           # print item['posts'].encode('utf-8')
            global count

            for word in words:
                if (word in self.category):
                    cat_word = word.decode('utf-8')
                    self.es.index(index="scoretest3", doc_type="categorized",id=cat_word+item['id'].encode('utf-8'),
                        body={"contents": item["posts"], "likes": item["likes"], "date": item["date"], "comments_count" : item["comments_count"], "score" : score, "category":cat_word})
        """시간 출력부"""
        print self.limit_time, item["date"]
        if(self.limit_time > item["date"]):
            print "3개월 지남"
            has_next = False
        if has_next:
            url = "https://www.instagram.com/" + self.account + "?max_id="+has_next2['end_cursor'].encode('utf-8')
            yield scrapy.Request(url, callback=self.parse_page)
