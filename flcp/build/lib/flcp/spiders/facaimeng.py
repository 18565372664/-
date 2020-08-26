import scrapy
from bs4 import BeautifulSoup
from lxml import etree
from flcp.items import FlcpItem
import re

num = 1

class FacaimengSpider(scrapy.Spider):
    name = 'facaimeng'
    allowed_domains = ['kaijiang.zhcw.com']

    start_urls = ['http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=1']

    def parse(self, response):
        html = response.xpath('//tr')[2:-1]
        # print(html.extract_first())
        # print(50*'*')
        for th in html:
            iterm = FlcpItem()
            iterm['time'] = th.xpath('./td[1]/text()').extract_first()
            iterm['term'] = th.xpath('./td[2]/text()').extract_first()
            iterm['em1'] = th.xpath('./td[3]/em[1]/text()').extract_first()
            iterm['em2'] = th.xpath('./td[3]/em[2]/text()').extract_first()
            iterm['em3'] = th.xpath('./td[3]/em[3]/text()').extract_first()
            iterm['em4'] = th.xpath('./td[3]/em[4]/text()').extract_first()
            iterm['em5'] = th.xpath('./td[3]/em[5]/text()').extract_first()
            iterm['em6'] = th.xpath('./td[3]/em[6]/text()').extract_first()
            iterm['em7'] = th.xpath('./td[3]/em[7]/text()').extract_first()
            yield iterm

        next_url_num = response.xpath("//a[text()='下一页']/@href").extract_first()
        next_url_num1 = next_url_num.split('=')[1]
        if next_url_num1 is not None:
            # next_url_num= int(next_url_num)
            # next_url_num+=1
            next_url = 'http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum={}'.format(next_url_num1)
            print(next_url)
            yield scrapy.Request(next_url,callback=self.parse)





