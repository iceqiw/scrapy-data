import scrapy
from scrapy.http import Request
import json
from jd.items import JdItem


class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    key=""

    search_url = 'https://search.jd.com/Search?keyword={key}&enc=utf-8&page={page}'

    def start_requests(self):
        print("start")
        key =self.key
        for i in range(1, 2):
            page_num = str(2 * i - 1)
            urls = self.search_url.format(key=key, page=page_num)
            print(urls)
            yield Request(url=urls, callback=self.page)

    def page(self, response):
        all_goods = response.xpath('//div[@id="J_goodsList"]/ul/li')
        for one_good in all_goods:
            item = JdItem()
            item['id'] = "jd_"+one_good.xpath('@data-pid').extract()[0]
            data = one_good.xpath('div/div/a/em')
            item['title'] = data.xpath('string(.)').extract()[0]  
            item['price'] =one_good.xpath('div/div[@class="p-price"]/strong/i/text()').extract()[0]
            item['link'] = 'http:'+one_good.xpath('div/div[@class="p-name p-name-type-2"]/a/@href').extract()[0]
            item['picurl'] = 'http:'+one_good.xpath('div/div[@class="p-img"]/a/img/@src').extract()[0]
            yield item
            pass
