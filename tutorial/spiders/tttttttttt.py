# -- coding: utf-8 --
from elasticsearch import Elasticsearch
import time

class ScoreMerge(object):
    def __init__(self):
        self.es = Elasticsearch()
        self.count = 0
        self.category = open("/home/eunsoo/Downloads/tutorial/tutorial/category.txt", "r").read().split()
        self.total_posts = 0
        self.start_time = time.time()

    def scoreMerge(self):
        self.es.indices.delete(index='merge', ignore=[400, 404])
        self.total_posts = 0
        for cat in self.category:
            self.count = self.count + 1
            acc_score = 0.0
            acc_likes = 0
            acc_comments_count = 0
            post_count = 0
            search_results = self.es.search(index="scoretest3", doc_type='categorized', body={"query": { "match": {"category": cat}}}, size= 10000)
            if('hits' in search_results):
                for search_result in search_results['hits']['hits']:
                    """score 다시 계산 하고 싶을 경우 여기에서 계산 바람"""
                    #self.time 이 스코어 합산시의 시간으로 변경됨을 유의/ 60*60*24 를 빼면 하루전의 시간으로 돌아갈 수 있음
                    #score_time = (self.start_time - search_result['_source']['date'])(60*60*24)   # 2일
                    #score_likes = search_result['_source']["likes"]
                    #score_comments = search_result['_source']['comments_count']
                    #score = (score_likes + score_comments) / (score_time*10)

                    """"""""""""""""""""""""""""""""""""""""""""""""
                    acc_score = acc_score + search_result['_source']['score'] #여기에서 search_result['_source']['score'] 를 score로 바꿔주면 새로운 score로 바뀜
                    acc_likes = acc_likes + search_result['_source']['likes']
                    acc_comments_count = acc_comments_count + search_result['_source']['comments_count']

                    post_count = post_count + 1
                self.es.index(index="merge", doc_type="merge", id = self.count,
                              body={"category": cat, "acc_likes": acc_likes, "acc_comments_count": acc_comments_count, "acc_score": acc_score, "post_count" : post_count })
                self.total_posts = self.total_posts + post_count
    def displaySortedCategory(self):
        search_results = self.es.search(index="merge", doc_type='merge',
                                        body={"sort": {"acc_score": {"order": "desc"}}}, size=30)

        print "총 글 수 : ", self.total_posts
        print "category / acc_likes / acc_comments_count / acc_score / post_count"
        for search_result in search_results['hits']['hits']:
            print ("%s/%10f/%10f/%10f/%10f" %(search_result['_source']['category'], search_result['_source']['acc_likes'],search_result['_source']['acc_comments_count'],search_result['_source']['acc_score'],search_result['_source']['post_count']))
            self.es.index(index="please",doc_type="please",body={"category":search_result['_source']['category'],"score":search_result['_source']['acc_likes']})

sm = ScoreMerge()
sm.scoreMerge()
sm.displaySortedCategory()
