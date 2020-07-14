from datetime import datetime
# from scrapy_plus.utils.log import logging
from scrapy_plus.utils.log import logger
import time

from .spider import Spider
from scrapy_plus.https.request import   Request
from .downloader import Downloader
from .pipline import Pipeline
from .scheduler import Scheduler
from scrapy_plus.middlewares.spider_midddlewares import SpiderMiddleware
from scrapy_plus.middlewares.downloader_middlewares import DownloaderMiddleware



class Engine(object):

    def __init__(self,spiders):
        self.spiders = spiders
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddleware()

        self.total_request_nums = 0
        self.total_response_nums = 0


    def start(self):
        start_time = datetime.now()
        logger.info("开始运行时间：%s"%start_time)

        self._start_engine()
        stop = datetime.now()
        end_time = datetime.now()
        logger.info("结束运行时间：%s"% end_time)
        logger.info("耗时：%.2f" % (stop - start_time).total_seconds())
        logger.info("总的请求数量：{}".format(self.scheduler.total_request_number))
        logger.info("总的响应数量：{}".format(self.total_response_nums))

    def _start_request(self):
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():
                #1. 对start_request进过爬虫中间件进行处理
                start_request = self.spider_mid.process_request(start_request)

                # 为请求对象绑定它所属的爬虫的名称
                start_request.spider_name = spider_name

                #2. 调用调度器的add_request方法，添加request对象到调度器中
                self.scheduler.add_request(start_request)
                #请求数+1
                self.total_request_nums += 1
    def _execute_request_item(self):
        request = self.scheduler.get_request()
        if request is None:
            return
        try:
            request = self.downloader_mid.process_request(request)
            response = self.downloader.get_response(request)

            response.meta = request.meta


            response = self.downloader_mid.process_response(response)
            response = self.spider_mid.process_response(response)

            spider = self.spiders[request.spider_name]
            print(type(spider))


            parse = getattr(spider, request.parse)

            # getattr(类, 类中方法名的字符串) = 类方法对象
            for result in self.spiders.parse(response):
                if isinstance(result,Request):
                    result = self.spider_mid.process_request(result)
                    result.spider_name = request.spider_name
                    self.scheduler.add_request(result)
                else:
                    self.pipeline.process_item(result)
        except Exception as e:
            print(e)
        finally:
            self.total_response_nums+=1

    def _start_engine(self):
        self._start_request()
        while True:
            time.sleep(0.002)
            self._execute_request_item()
            if self.total_response_nums>=self.scheduler.total_request_number:
                break





