# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TaobaoPipeline(object):
    def __init__(self):
        self.es = Elasticsearch(['192.168.1.143'], port=9200)

    def process_item(self, item, spider):
        try:
            print('------------------------------')
            id = item['id']
            link = item['link']
            price = item['price']
            picurl = item['picurl']
            title = item['title']
            doc = {
                'url': link,
                'imgUrl':picurl,
                'title': title,
                'price':price,
            }
            self.es.index(index="item", doc_type='sd', id=id, body=doc)
            print('商品ID\t', id)
            print('商品名称\t', title)
            print('商品链接\t', link)
            print('商品价格\t', price)
            print('商品图片\t', picurl)
            return item
        except Exception as err:
            pass
