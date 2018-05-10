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
        cursor.close()
        # try:
        #     print(cursor.execute(sql,(item['title'],item['content'],item['label'],item['img'][0],item['student'],item['level'])))
        #     db.commit()
            
        # except:
        #     print("error")
        #     db.rollback()
        # db.close()
        return item