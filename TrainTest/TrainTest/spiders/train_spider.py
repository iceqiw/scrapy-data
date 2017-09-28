# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import *

class StationSpider(scrapy.Spider):
    name = "TrainTest"

    #填写爬取地址
    start_urls = [
        'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9026'
    ]

    # def parse(self, response):
    #     line = 'http://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'
    #     stations = response.body_as_unicode().split('@')
    #     i = 0
    #     for start in stations:
    #         i = i + 1
    #         startline = start.split('|')
    #         if len(startline) > 2:
    #             for end in stations:
    #                 endline = end.split('|')
    #                 if len(endline) > 2:
    #                     url = line % ('2017-10-01', startline[2], endline[2])
    #                     yield scrapy.Request(
    #                         url=url, callback=self.parse_detail)

    def parse(self, response):
        begin_date = datetime.now()
        line = 'http://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'
        for i in range(1,30):
            date_str = begin_date.strftime("%Y-%m-%d")
            url = line % (date_str, 'FZS', 'XAY')
            yield scrapy.Request(url=url, callback=self.parse_detail)
            begin_date += timedelta(days=1)
            

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
        train_detail = {}
        train_detail['train'] = line[3]
        train_detail['date'] = line[13]
        train_detail['key'] = line[6] + '_' + line[7]
        train_detail['soft_sleeper'] = self.getSeatNum(line[23])  #软卧
        train_detail['hard_sleeper'] = self.getSeatNum(line[28])  #硬卧
        train_detail['hard_seat'] = self.getSeatNum(line[29])  #硬座
        train_detail['none_seat'] = self.getSeatNum(line[26])  #无座

        train_detail['top_seat'] = self.getSeatNum(line[31])
        train_detail['second_seat'] = self.getSeatNum(line[30])
        return train_detail

    def getSeatNum(self, word):
        if word == '无':
            return 0
        if word == '有':
            return 100
        if word =='':
            return 0
        return word
