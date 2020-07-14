import re
import json
from lxml import etree



class Response(object):

    def __init__(self,url,status_code,header,body,meta={}):
        self.url = url
        self.statuts_code= status_code
        self.header = header
        self.body = body

        self.meta = meta



    def xpath(self,rule):
        html = etree.HTML(self.body)
        return html.xpath(rule)


    @property
    def json(self):
        return json.loads(self.body)


    def re_finall(self,rule,data=None):
        if data is None:
            data=self.body
        return re.findall(rule,data)





