import scrapy
from scrapy.http import Request
import json
import re


class GhSpider(scrapy.Spider):
    name = "gh"

    search_url = 'http://xy.59iedu.com/Study/Learning?sscId=ee58cb9f54644e3cbdd80b8a973f390b'

    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language":
        "zh-CN,zh;q=0.8",
        "Connection":
        "keep-alive",
        "Cookie":
        "hbjyUsersCookiesxy.59iedu.com=756|756|21e65008700644948e6166121897395a; UM_distinctid=16261b65d3c3f3-0c3c3a5cd90e4a-3a7f0e5a-1fa400-16261b65d3d19ac; ASP.NET_SessionId=dvn2rkym3rap3iapoy5idrlx; IsLoginUsersCookies_xy.59iedu.comxy.59iedu.com=IsLogin; CNZZDATA5050476=cnzz_eid%3D1971169959-1522054592-null%26ntime%3D1522203047; menu_bind=-1",
        "Upgrade-Insecure-Requests":
        "1",
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
    }

    def start_requests(self):
        print("start")
        yield Request(
            url=self.search_url, headers=self.headers, callback=self.page)

    def page(self, response):
        link = response.xpath('//table[@class="xktable"]/tbody/tr/td/a/@href')
        for u in link.extract():
            url = 'http://xy.59iedu.com' + u
            print(url)
            yield Request(url=url, headers=self.headers, callback=self.video)

    # http://fjwcf.59iedu.com/Home/Timing?usrId=da6c64faa2ed412682f683ad394fbc92&medId=fzrs201712110002&studyId=7ea9356aea1f4c35a1f225b2b0868ffb&callback=jsonp1522058645347&CurrentTimespan=54&Id=7481fb1ae7a047bb8a6660b615b5163b&SscId=ee58cb9f54644e3cbdd80b8a973f390b&SstId=1497ca5583554eca85fc0aa34e673d43&CourseSdlId=9e4f4f6f655e41b6a85dd72069dd78df&TrainSdlId=0b6d2328e6f145ca973c502a2bf082f3&Type=1&CurrentLength=30
    def video(self, response):
        script_u = response.xpath('//script[@type="text/javascript"]')[
            15].extract()
        #    print(script_u)
        params = '&CurrentTimespan=54&Id={Id}&SscId=ee58cb9f54644e3cbdd80b8a973f390b&SstId=1497ca5583554eca85fc0aa34e673d43&CourseSdlId=9e4f4f6f655e41b6a85dd72069dd78df&TrainSdlId=0b6d2328e6f145ca973c502a2bf082f3&Type=1&CurrentLength=30'
        timingUrl_re = 'var timingUrl = "(.*?)"'
        timingUrl = re.compile(timingUrl_re).findall(script_u)[0]
        id_re = 'Id: "(.*?)"'
        Id = re.compile(id_re).findall(script_u)[0]
        mediaId_re = 'var mediaId = "(.*?)"'
        mediaId = re.compile(mediaId_re).findall(script_u)[0]
        mediaLoadURL = "http://xy.59iedu.com/Study/Learning/MediaAddress"
        print(mediaId + '\001' +"nnn")
