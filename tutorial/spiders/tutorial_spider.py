import re
import json

from scrapy import Spider, Item, Field




from tutorial.util import get_extracted
class InstagramProfileItems(Item):
    is_private = Field()
    posts = Field()
    username = Field()
    bio = Field()
    website = Field()
    profile_picture = Field()
    full_name = Field()
    total_posts = Field()
    followers = Field()
    following = Field()

class Instagram(Spider):
    name = "tutorial"
    start_urls = ["http://instagram.com/greedeat"]

    download_delay = 0.5

    def parse(self, response):
        javascript = "".join(response.xpath('//script[contains(text(), "sharedData")]/text()').extract())
       # print javascript(.*);
        item = InstagramProfileItems()
        json_data = json.loads("".join(re.findall(r'window._sharedData =(.*);', javascript)))
        #print json_data
        data = get_extracted(json_data["entry_data"]["ProfilePage"])
        #print data
        item["posts"] = data["user"]["media"]["nodes"]
        return item

""""
        item = InstagramProfileItems()
        data = get_extracted(json_data["entry_data"])
       # data = get_extracted(json_data["entry_data"]["ProfilePage"])
        #item["is_private"] = data["relationship"]["is_private"]
        item["posts"] = data["user"]["media"]
        item["username"] = data["user"]["username"]
       # item["bio"] = data["user"]["bio"]
       # item["website"] = data["user"]["website"]
        #item["profile_picture"] = data["user"]["profile_picture"]
        #item["full_name"] = data["user"]["full_name"]
        #item["total_posts"] = data["user"]["counts"]["media"]
        item["followers"] = data["user"]["followed_by"]
        item["following"] = data["user"]["follows"]
        #yield item
        return item
"""