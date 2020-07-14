from scrapy_plus.core.spider import Spider
from scrapy_plus.https.request import Request
from scrapy_plus.item import Item


class BaiduSpider(Spider):
    start_urls = ['http://www.baidu.com']


class DoubanSpider(Spider):
    start_url = []

    def start_requests(self):
        base_url = 'https://movie.douban.com/top250?start='
        for i in range(0,250,25):
            url = base_url+str(i)
            yield Request(url)

    def parse(self,response):
        title_list = []
        # for li in response.xpath(".//ol[@class='grid_view']/li"):
        #     title = li.xpath(".//span[@class='title'][1]/text()")
        #     title_list.append(title[0])
        # yield Item(title_list)
        for li in response.xpath("//ol[@class='grid_view']/li"):    # 遍历每一个li标签
            item = {}
            item["title"] =  li.xpath(".//span[@class='title'][1]/text()")[0]    # 提取该li标下的 标题
            # title_list.append(title[0])

            detail_url = li.xpath(".//div[@class='info']/div[@class='hd']/a/@href")[0]
            yield Request(detail_url, parse="parse_detail",meta={"item":item})    # 发起详情页的请求，并指定解析函数是parse_detail方法

    def parse_detail(self, response):
        '''解析详情页'''
        item = response.meta["item"]
        item["url"] = response.url
        print('item：', item)  # 打印一下响应的url
        return []  # 由于必须返回一个容器，这里返回一个空列表
        # yield Item(item)  #或者yield Item对象



