import scrapy
from recuitment.items import RecuitmentItem

class ZgSpider(scrapy.Spider):
    name = 'zg'

    def start_requests(self):
        urls = [
            'http://www.wenwu8.com/news/news_246.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, respones):
        infos = respones.css('#listul li')
        for info in infos:
            if '小学' in info.css('a::text').extract_first():
                ri = RecuitmentItem()
                ri['name'] = info.css('a::text').extract_first()
                if info.xpath('span/text()').extract_first():
                    ri['date'] = info.css('span::text').extract_first()
                else:
                    ri['date']=info.xpath('span/font/text()').extract_first()
                yield ri
