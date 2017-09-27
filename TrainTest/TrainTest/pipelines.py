# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TraintestPipeline(object):
    def __init__(self):
        #打开文件
        self.file = open('search.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):

        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #写入文件
        self.file.write(line)
        #返回item
        return item
