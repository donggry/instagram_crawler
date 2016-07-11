# -- coding: utf-8 --
from elasticsearch import Elasticsearch

class ScoreMerge(object):

    def __init__(self):
        self.es = Elasticsearch()
        self.count = 0
        self.category = open("/home/eunsoo/Downloads/tutorial/tutorial/category.txt", "r").read().split()

    def scoreMerge(self):
        self.es.indices.delete(index='merge', ignore=[400, 404])
        for cat in self.category:
            self.count = self.count + 1
            acc_score = 0.0
            post_count = 0
            search_results = self.es.search(index="scoretest", doc_type='categorized', body={"query": { "match": {"category": cat}}})
            if('hits' in search_results):
                #print search_results['hits']['hits']
                for search_result in search_results['hits']['hits']:
                    acc_score = acc_score + search_result['_source']['score']
                    post_count = post_count + 1

                self.es.index(index="mergetest", doc_type="merge", id = cat,
                              body={"category": cat, "acc_score": acc_score, "post_count" : post_count })
                print cat+"successfully merged"

    def displaySortedCategory(self):
        search_results = self.es.search(index="mergetest", doc_type='merge',
                                        body={"sort": {"acc_score": {"order": "desc"}}})

        print search_results
        #print "category / acc_likes / acc_comments_count / acc_score / post_count"
        for search_result in search_results['hits']['hits']:
            print ("%s/%10f/%10f" %(search_result['_source']['category'],search_result['_source']['acc_score'],search_result['_source']['post_count']))

sm = ScoreMerge()
#sm.scoreMerge()
sm.displaySortedCategory()
