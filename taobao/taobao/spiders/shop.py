import scrapy
from scrapy.http import Request
import json
from taobao.items import TaobaoItem


class TaoBaoSpider(scrapy.Spider):
    name = "taobao"
    allowed_domains = ["taobao.com"]
    key=""
    # https://s.taobao.com/api?_ksTS=1521542029676_238&callback=jsonp239&ajax=true&m=customized&sourceId=tb.index&q=ad&spm=a21bo.2017.201856-taobao-item.1&s=36&imgfile=&initiative_id=tbindexz_20170306&bcoffset=0&commend=all&ie=utf8&rn=375b27ced5dac005940095bd615cbdc1&ssid=s5-e&search_type=item
    # https://s.taobao.com/search?q=addidas&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180320&ie=utf8
    def start_requests(self):
        print("start")
        key =self.key
        for i in range(0, 3):
            url = 'https://s.taobao.com/api?m=customized&q=' + str(key) + '&s=' + str(44 * i)
            print(url)
            yield Request(url=url, callback=self.page)
        pass        

    def page(self, response):
        data = json.loads(response.body_as_unicode())
        items = data['API.CustomizedApi']['itemlist']['auctions']
        for i in items:
            item = TaobaoItem()
            item['id'] = "taobao_"+i['nid']
            item['title'] = i['raw_title']
            item['link'] = "https://item.taobao.com/item.htm?id=" + i['nid']
            item['price'] = i['view_price']
            item['picurl'] = "http:" + i['pic_url']
            yield item
            
