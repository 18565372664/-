class Request(object):

    def __init__(self,url,method='GET',\
                 headers=None,params=None,data=None,parse = 'parse',meta ={}):

        self.url = url
        print("这是初始请求URL：{}".format(self.url))
        self.method = method
        self.headers = headers
        self.params= params
        self.data = data

    #         新增解析函数属性
        self.parse = parse
        self.meta = meta


