# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlcpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

    time = scrapy.Field()
    term = scrapy.Field()
    em1 = scrapy.Field()
    em2 = scrapy.Field()
    em3 = scrapy.Field()
    em4 = scrapy.Field()
    em5 = scrapy.Field()
    em6 = scrapy.Field()
    em7 = scrapy.Field()