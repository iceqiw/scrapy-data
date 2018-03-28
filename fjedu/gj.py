import requests
import time
import re
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

timeUrl = '&CurrentTimespan=1060&Id={Id}&SscId=ee58cb9f54644e3cbdd80b8a973f390b&SstId=1497ca5583554eca85fc0aa34e673d43&CourseSdlId=9e4f4f6f655e41b6a85dd72069dd78df&TrainSdlId=0b6d2328e6f145ca973c502a2bf082f3&Type=1&CurrentLength=30'

with open("data.txt", "r") as f:
    for line in f.readlines():
        meId = line.split('\001')[0]
        url_ch = 'http://xy.59iedu.com/Study/Learning/MediaLi?sscId=ee58cb9f54644e3cbdd80b8a973f390b&medId=' + meId
        print(url_ch)
        r = requests.get(url_ch, headers=headers)
        # print(r.text)
        timingUrl_re = 'var timingUrl = "(.*?)"'
        timingUrl = re.compile(timingUrl_re).findall(r.text)[0]
        id_re = 'Id: "(.*?)"'
        Id = re.compile(id_re).findall(r.text)[0]
        url = timingUrl + timeUrl.format(Id=Id)
        print(url)

        ok = True
        while ok:
            rt = requests.get(url, headers=headers)
            print(rt.text)
            id_re = '"Process":(.*?),'
            Id = re.compile(id_re).findall(rt.text)
            if Id:
                print(Id)
                if Id[0] == '100.0':
                    print("hh")
                    ok = False
                else:
                    print("xx")
            time.sleep(1)
        print('----------------------------')
