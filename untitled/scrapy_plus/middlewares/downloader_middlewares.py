class DownloaderMiddleware(object):
    def process_request(self,request):
        print("这是下载器中间件：{}".format(request))
        return request

    def process_response(self,response):
        print("这是下载器中间件：{}".format(response))
        return response


