import requests
import time
import re
import http.cookiejar
import argparse

FLAGS = {}

parser = argparse.ArgumentParser()

parser.add_argument('--mycookie', type=str, default='11111', help='mycookie')

parser.add_argument(
    '--SscId',
    type=str,
    default='e680cdffa65543a2a22ea0eacdd5ad54',
    help='SscId')

parser.add_argument(
    '--SstId',
    type=str,
    default='8e576ed062154ecf93c75f8020768f26',
    help='SstId')

parser.add_argument(
    '--CourseSdlId',
    type=str,
    default='7deb36fee2dd4a34bbea0e35b9bebaf9',
    help='CourseSdlId')

parser.add_argument(
    '--TrainSdlId',
    type=str,
    default='63c37eaf17ae43cd8cc24365828d7565',
    help='TrainSdlId')

headers = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language":
    "zh-CN,zh;q=0.8",
    "Connection":
    "keep-alive",
    "Upgrade-Insecure-Requests":
    "1",
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
}
sessionurl='http://xy.59iedu.com/Public/MessageNotice/ReloadSession'
timeUrl = '&CurrentTimespan=1060&Id={Id}&SscId={SscId}&SstId={SstId}&CourseSdlId={CourseSdlId}&TrainSdlId={TrainSdlId}&Type=2&CurrentLength=30'
session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename='Cookie')


def run(mycookie, SscId, SstId, CourseSdlId, TrainSdlId):
    headers['Cookie'] = mycookie
    print(headers)
    with open("data.txt", "r") as f:
        for line in f.readlines():
            meId = line.split('\001')[0]
            url_ch = 'http://xy.59iedu.com/Study/Learning/MediaLi?sscId=' + SscId + '&medId=' + meId
            print(url_ch)
            r = session.get(url_ch, headers=headers)
            # print(r.text)
            timingUrl_re = 'var timingUrl = "(.*?)"'
            timingUrl = re.compile(timingUrl_re).findall(r.text)[0]
            id_re = 'Id: "(.*?)"'
            Id = re.compile(id_re).findall(r.text)[0]
            url = timingUrl + timeUrl.format(
                Id=Id,
                SscId=SscId,
                SstId=SstId,
                CourseSdlId=CourseSdlId,
                TrainSdlId=TrainSdlId)
            print(url)

            ok = True
            while ok:
                rt = session.get(url)
                session.post(sessionurl,headers=headers)
                print(rt.text)
                id_re = '"Process":(.*?),'
                Id = re.compile(id_re).findall(rt.text)
                if Id:
                    print(Id)
                    if Id[0] == '100.0':
                        print("结束课程")
                        ok = False
                    else:
                        print("继续挂")
                time.sleep(1)
            print('----------------------------')


if __name__ == "__main__":
    FLAGS, unparsed = parser.parse_known_args()
    run(FLAGS.mycookie, FLAGS.SscId, FLAGS.SstId, FLAGS.CourseSdlId,
        FLAGS.TrainSdlId)
