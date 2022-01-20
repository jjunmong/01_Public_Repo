import bs4
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

def getStoreInfo(intPageNo):
    url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    querystring = {"serviceKey":"fdBIIF1vASwjtUTGKzimsdOegcu7mQMFdyIba/JeymvRkGmib9WbfhD9X/hh3ruQLQWvqtD5l9p4KEihyi1Hrw=="}
    querystring['pageNo'] = intPageNo
    querystring['numOfRows']= '1000'
    try:
        response = requests.request("GET", url, params=querystring).text
    except requests.exceptions.ConnectionError:
        print(intPageNo, "해당 코드의 페이지 호출을 실패하여 실패 리스트로 반환합니다.")
        outfile = codecs.open('건강심사평가원_병원_수집실패.txt', 'a')
        fail_url = str(intPageNo) + '\n'
        outfile.write(fail_url)
        outfile.close()
    soup = bs4.BeautifulSoup(response,"lxml")
    list = soup.find_all('item')
    data = []
    for info in range(len(list)):
        try:
            yadmnm = list[info].find('yadmnm').text
        except AttributeError:
            yadmnm = ''
        try:
            addr = list[info].find('addr').text
        except AttributeError:
            addr =''
        try:
            clcd = list[info].find('clcd').text
        except AttributeError:
            clcd = ''
        try:
            drtotcnt = list[info].find('drtotcnt').text
        except AttributeError:
            drtotcnt =''
        try:
            estbdd = list[info].find('estbdd').text
        except AttributeError:
            estbdd = ''
        try:
            gdrcnt = list[info].find('gdrcnt').text
        except AttributeError:
            gdrcnt = ''
        try:
            intncnt = list[info].find('intncnt').text
        except AttributeError:
            intncnt = ''
        try:
            postno = list[info].find('postno').text
        except AttributeError:
            postno = ''
        try:
            resdntnct = list[info].find('resdntnct').text
        except AttributeError:
            resdntnct = ''
        try:
            sdrcnt = list[info].find('sdrcnt').text
        except AttributeError:
            sdrcnt = ''
        try:
            sggucd = list[info].find('sggucd').text
        except AttributeError :
            sggucd = ''
        try :
            sggucdnm = list[info].find('sggucdnm').text
        except AttributeError:
            sggucdnm = ''
        try:
            sidocd = list[info].find('sidocd').text
        except AttributeError:
            sidocd =''
        try:
            sidocdnm = list[info].find('sidocdnm').text
        except AttributeError:
            sidocdnm = ''
        try:
            telno = list[info].find('telno').text
        except AttributeError:
            telno = ''
        try:
            hospurl = list[info].find('hospurl').text
        except AttributeError:
            hospurl = ''
        try:
            xpos = list[info].find('xpos').text
        except AttributeError:
            xpos = ''
        try:
            ypos = list[info].find('ypos').text
        except AttributeError:
            ypos =''
        try :
            ykiho = list[info].find('ykiho').text
        except AttributeError:
            ykiho : ''
        data.append({"yadNm":yadmnm,"addr":addr,"clcd":clcd,"drTotCnt":drtotcnt,"estbdd":estbdd,"gdrCnt":gdrcnt,"intnCnt":intncnt,"postNo":postno,"resdntNct":resdntnct
                     ,"sdrCnt":sdrcnt,"sgguCd":sggucd,"sgguCdNm":sggucdnm,"sidoCd":sidocd,"sidoCdNm":sidocdnm,"telno":telno,"hospurl":hospurl,"XPos":xpos,"YPos":ypos,"ykiho":ykiho})
    results = [dict(t) for t in {tuple(d.items()) for d in data}]
    return results
print(getStoreInfo(1))
