import scrapy


class StockSpider(scrapy.Spider):
    name = "stock"

    start_urls = ['https://blog.csdn.net/dayun555/article/details/79415782']

    def parse(self, response):
        self.logger.info('start: %s', response.url)
