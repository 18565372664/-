from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider


class DoubanPipline(object):
    def process_item(self,item,spider):
        if isinstance(spider,BaiduSpider):
            print("百度的爬虫数据",item)
        return item


