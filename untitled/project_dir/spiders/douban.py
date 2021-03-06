from scrapy_plus.core.spider import Spider
from scrapy_plus.https.request import Request
from scrapy_plus.item import Item


class DoubanSpider(Spider):
    name = 'douban'
    start_urls = []  # 重写start_requests方法后，这个属性就没有设置的必要了

    def start_requests(self):
        # 重写start_requests方法，返回多个请求
        useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        headers = {'User-Agent': useragent}
        base_url = 'http://movie.douban.com/top250?start='
        for i in range(0, 250, 25):    # 逐个返回第1-10页的请求属相
            url = base_url + str(i)
            yield Request(url,parse='parse',headers=headers)

    def parse(self, response):
        '''解析豆瓣电影top250列表页'''
        title_list = []    # 存储所有的
        for li in response.xpath("//ol[@class='grid_view']/li"):    # 遍历每一个li标签
            # title = li.xpath(".//span[@class='title'][1]/text()")    # 提取该li标下的 标题
            # title_list.append(title[0])
            detail_url = li.xpath(".//div[@class='info']/div[@class='hd']/a/@href")[0]
            yield Request(detail_url, parse="parse_detail")    # 发起详情页的请求，并指定解析函数是parse_detail方法
        # yield Item(title_list)    # 返回标题

    def parse_detail(self, response):
        '''解析详情页'''
        print('详情页url：', response.url)    # 打印一下响应的url
        return []    # 由于必须返回一个容器，这里返回一个空列表