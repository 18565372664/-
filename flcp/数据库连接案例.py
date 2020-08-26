import pymysql


class Dbconnet():
    def __init__(self):
        self.db = pymysql.connect(host='192.168.146.132', user="root", passwd="mysql", db="flcp", port=3306, charset="utf8")
        self.cur = self.db.cursor()

    def dbcon(self):
        self.cur.execute("select * from facaimeng")
        print(self.cur.fetchall())
        #sql = """INSERT INTO facaimeng(time, term, em1, em2, em3, em4, em5, em6, em7, keys) VALUES('time', 'term', 'em1', 'em2', 'em3', 'em4', 'em5', 'em6', 'em7','1');"""
        sql = "INSERT INTO `facaimeng`(`time`, `term`, `em1`, `em2`, `em3`, `em4`, `em5`, `em6`, `em7`, `keys`) " \
              "VALUES ('2020-01-01', '1', '12', '12', '13', '14', '15', '16', '17', '182222');"
        comit = self.cur.execute(sql)
        self.db.commit()

        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    dbconct= Dbconnet()
    dbconct.dbcon()
