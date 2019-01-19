# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
import os

class RecuitmentPipeline(object):
    def open_spider(self, spider):
        file_name = time.strftime("%Y-%m-%d", time.localtime())
        os.makedirs(file_name, exist_ok=True)
        self.file = open(file_name+'/zg.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print(item['name'], item['date'])
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
