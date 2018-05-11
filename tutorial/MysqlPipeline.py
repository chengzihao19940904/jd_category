#! /usr/bin/env python3
# -*- coding:utf8 -*-
# Date:2018/4/27
import pymysql
import scrapy
from scrapy.utils.project import get_project_settings
class MysqlPipeline(object):


    def __init__(self):
        settings = get_project_settings()
        self.conn = pymysql.connect(host=settings['MYSQL_HOST'],port=settings['MYSQL_PORT'],user=settings['MYSQL_USER'],passwd=settings['MYSQL_PASSWD'],db = settings['MYSQL_DBNAME'],charset='utf8')


    def process_item(self,item,spider):

        sql = "insert into muke_info(title,`desc`,`label`,imgs,studentNum,`level`) values(%s,%s,%s,%s,%s,%s);"
        cursor = self.conn.cursor()
        sql1 = "insert into jd_second_cate(`name`,url) values(%s,%s);"
        cursor.execute(sql1, (item['name'],item['url']))

        if item['child']:
            for value in item['child']:
                sql2 = "insert into jd_third_cate(pid,name,url) values(%s,%s,%s);"
                cursor.execute(sql2,(self.conn.insert_id(),value['name'],value['url']))
        
        self.conn.commit()
        # cursor.close()
        # try:
        #     print(cursor.execute(sql,(item['title'],item['content'],item['label'],item['img'][0],item['student'],item['level'])))
        #     db.commit()
            
        # except:
        #     print("error")
        #     db.rollback()
        # db.close()
        return item

    def close_item(self,spider):
        self.conn.close()


class GoodsPipeline(object):


    def __init__(self):
        settings = get_project_settings()
        self.conn = pymysql.connect(host=settings['MYSQL_HOST'],port=settings['MYSQL_PORT'],user=settings['MYSQL_USER'],passwd=settings['MYSQL_PASSWD'],db = settings['MYSQL_DBNAME'],charset='utf8')


    def process_item(self,item,spider):
        try:

            # sql = "insert into muke_info(title,`desc`,`label`,imgs,studentNum,`level`) values(%s,%s,%s,%s,%s,%s);"
            cursor = self.conn.cursor()
            scIsSql = "select id from jd_second_cate where name='%s' and url = '%s'" % (item['secondName'],item['secondUrl'])
            rowCount1 = cursor.execute(scIsSql)

            if rowCount1 == 0:
                sql1 = "insert into jd_second_cate(`name`,url) values(%s,%s);"
                cursor.execute(sql1, (item['secondName'],item['secondUrl']))
                secondId = cursor.lastrowid
            else:
                rowRet1 = cursor.fetchone()
                print(rowRet1)
                secondId = rowRet1[0]
            scIsSql2 = "select id from jd_third_cate where name='%s' and url = '%s' and pid=%s;" % (item['thirdCateName'],item['thirdUrl'],secondId)
            rowCount2 = cursor.execute(scIsSql2)

            if rowCount2 == 0 or not rowCount2:
                sql2 = "insert into jd_third_cate(pid,name,url) values(%s,%s,%s);"
                cursor.execute(sql2,(secondId,item['thirdCateName'],item['thirdUrl']))
                thirdId = cursor.lastrowid
            else:
                rowRet2 = cursor.fetchone()
                thirdId = rowRet2[0]

            sql3 = "insert into goods_detail(cate_id,title,price,imgUrl,words,shop_name,detail_url,tips) values(%s,%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(sql3,(thirdId,item['title'],item['price'],item['imgUrl'],item['words'],item['shop_name'],item['detail_url'],item['tips']))
        except Exception as e:
            self.conn.rollback()
            print("error occur ",e)
        else:

            self.conn.commit()
            # cursor.close()
            # try:
            #     print(cursor.execute(sql,(item['title'],item['content'],item['label'],item['img'][0],item['student'],item['level'])))
            #     db.commit()
                
            # except:
            #     print("error")
            #     db.rollback()
            # db.close()
            cursor.close()
        return item

    def close_item(self,spider):
        self.conn.close()    



 