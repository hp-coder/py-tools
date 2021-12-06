import pymysql
import pytesseract
import requests as req
from PIL import Image
from io import BytesIO

if __name__ == '__main__':
    # 打开数据库连接
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='luban-qualify-dev',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor  # 以字典的形式返回数据
    )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 更新语句
    sql = 'select distinct `联系电话` from 78data_hire'
    try:
        # 执行SQL语句
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        for item in result:
            # 循环列表，输出mobile值
            phone = item.get('联系电话')
            if (phone):
                resp = req.get(phone)
                text = pytesseract.image_to_string(Image.open(BytesIO(resp.content)), lang="eng")
                text = text[0:12]
                updateSql = 'update 78data_hire set `联系电话` = "%s" where `联系电话` = "%s"' % (text, phone)
                print(updateSql)
                cursor.update(sql)
                db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
