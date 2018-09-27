# coding=utf-8
# @File  : sql.py
# @Author: "maiyajj"
# @Date  : 2018/9/25

import mysql.connector
from Premium import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB)
cur = cnx.cursor(buffered=True)


class Sql(object):
    def insert_data(self, db, origin, category, name, model, price, premium, url, name_id):
        sql = "INSERT INTO {} (`origin`, `category`, `name`, `model`, `price`, `premium`, `url`, `name_id`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            db, origin, category, name, model, price, premium, url, name_id)
        cur.execute(sql)
        cnx.commit()

    def select_name(self, db, name_id):
        sql = "select exists(SELECT 1 from {} where name_id='{}')".format(db, name_id)
        cur.execute(sql)
        result = cur.fetchall()[0]
        return result

    def update_data(self, db, key, value, name_id):
        sql = "update {} set {}='{}' where name_id='{}'".format(db, key, value, name_id)
        cur.execute(sql)
        cnx.commit()

    def get_all_data_form_category(self, db, category):
        sql = "select * from {} where category='{}'".format(db, category)
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def get_all_category(self, db):
        sql = "select category from {} group by category".format(db)
        cur.execute(sql)
        result = cur.fetchall()
        result = [i[0] for i in result]
        return result

    def update_special_items(self, db, url):
        sql = "insert into {}_other (`url`) values ('{}')".format(db, url)
        cur.execute(sql)
        cnx.commit()

if __name__ == '__main__':
    sql = Sql()
    db = 'jd'
    # print(sql.get_all_category(db))
    # print(sql.update_special_items(db, 'ss'))
    vv = '{"category": "空调", "model": "KFR-72LW/BpYH700（A2）a", "name": "奥克斯（AUX） 变频冷暖圆柱立柜式空调柜机智能清洗二级效能 雪龙一号 KFR-72LW/BpYH700(A2)a 大3匹", "name_id": "11605177162", "origin": "奥克斯（AUX）", "other": "", "premium": "[[("全保修7年", "139"), ("全保修8年", "229"), ("全保+清洗", "249"), ("延保至8年", "199"), ("延保至9年", "399"), ("意外保2年", "149"), ("意外保3年", "169")], [("全保修7年", "139"), ("全保修8年", "229"), ("全保+清洗", "249"), ("延保至8年", "199"), ("延保至9年", "399"), ("意外保2年", "149"), ("意外保3年", "169")]]", "price": "6799.00", "url": "https://item.jd.com/11605177162.html"}'
    sql.update_data(db, 'premium', vv, name_id='11605177162')