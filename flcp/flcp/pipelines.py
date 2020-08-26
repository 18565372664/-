# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class FlcpPipeline:
    def process_item(self, item, spider):
        return item


class FcMPipeline(object):

    def open_spider(self,spider):
        if spider.name =='facaimeng':
            self.db = pymysql.connect(host='192.168.146.132', user="root", passwd="mysql", db="flcp", port=3306,
                                      charset="utf8")
            self.cur = self.db.cursor()


    def process_item(self,item,spider):
        print("*" * 500)
        print(item['time'])
        print("*"*500)

        ###"""INSERT
        #INTO `flcp`.`facaimeng`(`time`, `term`, `em1`, `em2`, `em3`, `em4`, `em5`, `em6`, `em7`, `keys`)
        #VALUES('1212', '1', '12', '12', '13', '14', '15', '16', '17', '18');"""

        #sql = "INSERT INTO `facaimeng`(`time`, `term`, `em1`, `em2`, `em3`, `em4`, `em5`, `em6`, `em7`, `keys`) " \
         #     "VALUES ({},{} ,{} ,{} ,{},{},{} ,{} ,{}, '182222');".format(item['time'],item['term'],item['em1'],item['em2'],item['em3'],item['em4'],item['em5'],item['em6'],item['em7'])


        sql = "INSERT INTO `facaimeng`(`time`,`mainkeys`, `term`, `em1`, `em2`, `em3`, `em4`, `em5`, `em6`, `em7`, `keys`) " \
              "VALUES ('','%s',%s ,%s ,%s ,%s,%s,%s ,%s ,%s, '182222');" \
              % (str(item['time']),item['term'],item['em1'],item['em2'],item['em3'],item['em4'],item['em5'],item['em6'],item['em7'])
        self.cur.execute(sql)
        self.db.commit()

        return item

    def close_spider(self,spider):
        if spider.name == 'facaimeng':
            self.cur.close()
            self.db.close()








