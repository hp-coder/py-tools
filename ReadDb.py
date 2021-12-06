# 引入pymysql模块
import pymysql
import pytesseract
import requests as req
from PIL import Image
from io import BytesIO


class DoMysql:
    # 初始化
    def __init__(self):
        # 创建连接
        self.conn = pymysql.Connect(
            host='192.168.0.192',
            port=3307,
            user='hupeng',
            password='123456',
            db='luban-qualify-dev',
            autocommit=True,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor  # 以字典的形式返回数据
        )
        # 获取游标
        self.cursor = self.conn.cursor()

    def connect(self):
        return self.conn

    def cur(self):
        return self.cursor

    # 返回多条数据
    def fetchAll(self, sql):
        self.cursor.execute(sql)
        result2 = self.cursor.fetchall()
        self.conn.commit()
        return result2

    # 插入一条数据
    def insert_one(self, sql):
        result = self.cursor.execute(sql)
        self.conn.commit()
        return result

    # 插入多条数据
    def insert_many(self, sql, datas):
        result = self.cursor.executemany(sql, datas)
        self.conn.commit()
        return result

    # 更新数据
    def update(self, sql):
        result = self.cursor.execute(sql)
        self.conn.commit()
        return result

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    mysql = DoMysql()
    # 查询数据
    sql = 'select distinct `phone` from 78_zzdb_all_01'
    result = mysql.fetchAll(sql)  # 返回列表,如果多条数据，列表中嵌套字典
    for item in result:
        # 循环列表，输出mobile值
        phone = item.get('phone')
        if phone and len('15600214315\n') < len(phone):
            try:
                # print(phone)
                resp = req.get(phone)
                text = pytesseract.image_to_string(Image.open(BytesIO(resp.content)), lang="eng")
                text = text[0:12]
                updateSql = 'update 78_zzdb_all_01 set `phone` = "%s" where `phone` = "%s";' % (text, phone)
                mysql.cursor.execute(updateSql)
                mysql.conn.commit()
            except:
                continue
    mysql.close()
