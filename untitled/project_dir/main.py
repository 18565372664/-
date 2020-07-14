from scrapy_plus.core.engine import Engine
from scrapy_plus.core.spider import Spider

from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider
from pipelines import DoubanPipline


from spider_middlewares import TestSpidermiddleware1, TestSpiderMiddleware2
from downloader_middlewares import TestDownloaderMiddleware1, TestDownloaderMiddleware2

# if __name__ == '__main__':
#     # spider = BaiduSpider()
#     # baidu_spider = BaiduSpider()    # 实例化爬虫对象
#     douban_spider = DoubanSpider()    # 实例化爬虫对象
#     spiders = {DoubanSpider.name: douban_spider}
#     pipelines = [DoubanPipline()]
#
#     spider_mids = [TestSpidermiddleware1(), TestSpiderMiddleware2()]
#     downloader_mids = [TestDownloaderMiddleware1(), TestDownloaderMiddleware2()]
#
#
#     engine = Engine(spiders,piplines=pipelines,spider_mids=spider_mids, downloader_mids=downloader_mids)    # 传入爬虫对象
#     engine.start()    # 启动引擎

if __name__ == '__main__':
    # spider = BaiduSpider()
    # # baidu_spider = BaiduSpider()    # 实例化爬虫对象
    # douban_spider = DoubanSpider()    # 实例化爬虫对象
    # spiders = {DoubanSpider.name: douban_spider}
    # pipelines = [DoubanPipline()]
    #
    # spider_mids = [TestSpidermiddleware1(), TestSpiderMiddleware2()]
    # downloader_mids = [TestDownloaderMiddleware1(), TestDownloaderMiddleware2()]


    engine = Engine()    # 传入爬虫对象
    engine.start()    # 启动引擎