from scrapy_plus.item import Item
from scrapy_plus.https.request import Request



class Spider(object):

    start_url = "http://www.baidu.com"
    start_urls = []

    def start_requests(self):
        for url in self.start_urls:
                yield Request(url)


    def parse(self,response):
        yield Item(response.body)



