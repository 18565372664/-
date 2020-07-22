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

from multiprocessing.dummy import Pool

import importlib
from scrapy_plus.conf.settings import SPIDERS, PIPELINES, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES

class Engine(object):

    def __init__(self):
        self.spiders = self._auto_import_instances(SPIDERS,isspider=True)   # 接收爬虫字典
        self.scheduler = Scheduler()    # 初始化调度器对象
        self.downloader = Downloader()    # 初始化下载器对象

        self.pipelines = self._auto_import_instances(PIPELINES) # 管道
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES) # 爬虫中间件
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES) # 下载中间件
        self.pool = Pool()
        self.is_running = False

        self.total_request_nums = 0
        self.total_response_nums = 0

    # 此处新增函数
    def _auto_import_instances(self, path=[], isspider=False):
        '''通过配置文件，动态导入类并实例化
        path: 表示配置文件中配置的导入类的路径
        isspider: 由于爬虫需要返回的是一个字典，因此对其做对应的判断和处理
        '''
        instances = {} if isspider else []
        for p in path:
            module_name = p.rsplit(".", 1)[0]  # 取出模块名称
            cls_name = p.rsplit(".", 1)[1]  # 取出类名称
            ret = importlib.import_module(module_name)  # 动态导入爬虫模块
            cls = getattr(ret, cls_name)  # 根据类名称获取类对象

            if isspider:
                instances[cls.name] = cls()  # 组装成爬虫字典{spider_name:spider(),}
            else:
                instances.append(cls())  # 实例化类对象
                # 把管道中间件分别组装成 管道列表=[管道类1(),管道类2()] / 中间件列表 = [中间件类1(),中间件类2()]
        return instances  # 返回类对象字典或列表


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
        logger.info("重复的请求数量:{}".format(self.scheduler.repeate_request_num))

    def _call_back(self, temp):  # 这是异步线程池的callback参数指向的函数,temp参数为固定写法
        if self.is_running:
            self.pool.apply_async(self._execute_request_response_item, callback=self._call_back)

    def _start_request(self):
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():
                #1. 对start_request进过爬虫中间件进行处理
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)

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
            for downloader_mid in self.downloader_mids:
                request = downloader_mid.process_request(request)
            response = self.downloader.get_response(request)

            response.meta = request.meta

            for downloader_mid in self.downloader_mids:
                response = downloader_mid.process_response(response)
            for spider_mid in self.spider_mids:
                response = spider_mid.process_response(response)

            spider = self.spiders[request.spider_name]
            print(type(spider))


            parse = getattr(spider, request.parse)

            # getattr(类, 类中方法名的字符串) = 类方法对象
            for result in parse(response):
                if isinstance(result,Request):
                    for spider_mid in self.spider_mids:
                        result = spider_mid.process_request(result)
                    result.spider_name = request.spider_name
                    self.scheduler.add_request(result)
                else:

                    for pipline in self.pipelines:
                        pipline.process_item(result,spider)
        except Exception as e:
            print(e)
        finally:
            self.total_response_nums+=1

    def _execute_request_response_item(self):
        '''根据请求、发起请求获取响应、解析响应、处理响应结果'''
        #3. 调用调度器的get_request方法，获取request对象
        request = self.scheduler.get_request()
        if request is None: #如果没有获取到请求对象，直接返回
            return

    def _start_engine(self):
        self.is_running = True  # 启动引擎，设置状态为True
        self.pool.apply_async(self._start_request)  # 使用异步线程池中的线程执行指定的函数

        # 不断的处理解析过程中产生的request
        self.pool.apply_async(self._execute_request_response_item, callback=self._call_back)
        self._start_request()
        while True:
            time.sleep(0.001)  # 避免cpu空转,避免性能消耗
            # self._execute_request_response_item()
            if self.total_response_nums != 0:  # 因为异步，需要增加判断，响应数不能为0
                # 成功的响应数+重复的数量>=总的请求数量 程序结束
                if self.total_response_nums + self.scheduler.repeat_request_num >= self.total_request_nums:
                    self.is_running = False
                    break





