# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time
import datetime
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import MySQLdb
import pdb

class ChainxyPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_%s.csv' % (spider.name, datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ["name","number","item_type","location","building","bedroom","bathroom","size","title_deep_number","description","date","link","photo"]
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.conn = MySQLdb.connect(db=db,
                                    user=user,
                                    passwd=passwd,
                                    host=host,
                                    charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    
    def process_item(self, item, spider):

        try:
            query = ("INSERT INTO listing_%s (id, name, number, item_type, location, building, bedroom, bathroom, size, price, title_deep_number, description, date, link, photo ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            self.cursor.execute(query, (str(item["item_type"]), str(item["item_id"]), str(item["name"].encode('utf-8')),str(item["number"]),str(item["item_type"]),str(item["location"].encode('utf-8')),str(item["building"]),str(item["bedroom"]),str(item["bathroom"]),str(item["size"]), str(item["price"]),str(item["title_deep_number"]),str(item["description"].encode('utf-8')),str(item["date"].encode('utf-8')),str(item["link"]),str(item["photo"])))
        except:
            # pdb.set_trace()
            query = ("UPDATE listing_%s SET name = %s, number= %s, item_type= %s, location= %s, building= %s, bedroom= %s, bathroom= %s, size= %s, price= %s, title_deep_number= %s, description=%s, date=%s, link= %s, photo= %s WHERE id = %s;")

            self.cursor.execute(query, (str(item["item_type"]), str(item["name"]).encode('utf-8') ,str(item["number"]).encode('utf-8') ,str(item["item_type"]).encode('utf-8') ,str(item["location"]).encode('utf-8') ,str(item["building"]).encode('utf-8') ,str(item["bedroom"]).encode('utf-8') ,str(item["bathroom"]).encode('utf-8') ,str(item["size"]).encode('utf-8'), str(item["price"]).encode('utf-8'),str(item["title_deep_number"]).encode('utf-8') ,str(item["description"].encode('utf-8')),str(item["date"].encode('utf-8')),str(item["link"].encode('utf-8')),str(item["photo"]), str(item["item_id"])))
            pass

        self.conn.commit()
        return item

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)