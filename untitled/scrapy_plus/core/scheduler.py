from queue import Queue
import six
# import w3lib.url
from hashlib import sha1

import w3lib.url

from scrapy_plus.utils.log import logger



class Scheduler(object):
    def __init__(self):
        self.queue = Queue()
        self.total_request_number =0
        self._filter_container=set()


    def add_request(self,request):
        if self._filter_request(request):
            self.queue.put((request))

    def get_request(self):
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            return request

    def _filter_request(self, request):
        # 去重方法
        request.fp = self._gen_fp(request) # 给request对象增加一个fp指纹属性
        if request.fp not in self._filter_container:
            self._filter_container.add(request.fp) # 向指纹容器集合添加一个指纹
            return True
        else:
            self.total_request_number += 1
            logger.info("发现重复的请求：<{} {}>".format(request.method, request.url))
            return False


    def _gen_fp(self, request):
        """生成并返回request对象的指纹
        用来判断请求是否重复的属性：url，method，params(在url中)，data
        为保持唯一性，需要对他们按照同样的排序规则进行排序
        """
        # 1. url排序：借助w3lib.url模块中的canonicalize_url方法
        url = w3lib.url.canonicalize_url(request.url)
        # 2. method不需要排序，只要保持大小写一致就可以 upper()方法全部转换为大写
        method = request.method.upper()
        # 3. data排序：如果有提供则是一个字典，如果没有则是空字典
        data = request.data if request.data is not None else {}
        data = sorted(data.items(), key=lambda x: x[0])  # 用sorted()方法 按data字典的key进行排序
        # items()返回元祖 key参数表示按什么进行排序 x表示data.items() x[0]表示元祖第一个值,也就是data的键
        # 4. 利用sha1计算获取指纹
        s1 = sha1()
        s1.update(self._to_bytes(url))  # sha1计算的对象必须是字节类型
        s1.update(self._to_bytes(method))
        s1.update(self._to_bytes(str(data)))

        fp = s1.hexdigest()
        return fp

    def _to_bytes(self, string):
        """为了兼容py2和py3，利用_to_bytes方法，把所有的字符串转化为字节类型"""
        if six.PY2:
            if isinstance(string, str):
                return string
            else:  # 如果是python2的unicode类型，转化为字节类型
                return string.encode('utf-8')
        elif six.PY3:
            if isinstance(string, str):  # 如果是python3的str类型，转化为字节类型
                return string.encode("utf-8")
            else:
                return string