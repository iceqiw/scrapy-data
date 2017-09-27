# -*- coding: utf-8 -*-
import scrapy
import json


class StationSpider(scrapy.Spider):
    name = "TrainTest"

    #填写爬取地址
    start_urls = [
        'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9026'
    ]

    def parse(self, response):
        line = 'http://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'
        stations = response.body_as_unicode().split('@')
        i = 0
        for start in stations:
            i = i + 1
            startline = start.split('|')
            if len(startline) > 2:
                for end in stations:
                    endline = end.split('|')
                    if len(endline) > 2:
                        url = line % ('2017-10-01', startline[2], endline[2])
                        yield scrapy.Request(
                            url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        try:
            data = json.loads(response.body_as_unicode())
            trains_detail = data['data']['result']
            for train in trains_detail:
                train_detail = self.parseTrain(train)
                self.logger.info('%s', train_detail)
                yield train_detail
        except:
            pass

    def parseTrain(self, train):
        line = train.split('|')
        res = {}
        res['train'] = line[3]
        res['date'] = line[13]
        res['start'] = line[6]  #起点
        res['end'] = line[7]  #终点
        res['soft_sleeper'] = line[23]  #软卧
        res['hard_sleeper'] = line[28]  #硬卧
        res['hard_seat'] = line[29]  #硬座
        res['none_seat'] = line[26]  #无座

        res['top_seat'] = line[31]
        res['second_seat'] = line[30]
        return res
