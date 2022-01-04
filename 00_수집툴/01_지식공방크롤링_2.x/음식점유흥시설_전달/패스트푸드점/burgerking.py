# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import codecs
import time
import random
import urllib
import json
from lxml import html

area = {
    '서울특별시': '02',
    '광주광역시': '062',
    '대구광역시': '053',
    '대전광역시': '042',
    '부산광역시': '051',
    '울산광역시': '052',
    '인천광역시': '032',
    '경기도': '031',
    '강원도': '033',
    '경상남도': '055',
    '경상북도': '054',
    '전라남도': '061',
    '전라북도': '063',
    '충청남도': '041',
    '충청북도': '043',
    '제주특별자치도': '064',
    '세종특별자치시': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')


#    test = '[{"StoreSQ":225,"StoreNM":"경대병원SK점","PhoneNumber":"053-253-0332","NewAddr":"대구광역시 중구","NewAddr2":"달구벌대로 2194 ","AllHour":"Y","Delivery":"Y","Morning":"Y","DriveThrough":"Y","OpenTime":"","CloseWeekday":"","ClosePeakSeason":"","CloseCleaning":"","PointX":35.86282,"PointY":128.6031},{"StoreSQ":33,"StoreNM":"대구만촌점","PhoneNumber":"053-741-0208","NewAddr":"대구광역시 수성구 달구벌대로","NewAddr2":"2622 (만촌동)","AllHour":"Y","Delivery":"Y","Morning":"Y","DriveThrough":"Y","OpenTime":"","CloseWeekday":"","ClosePeakSeason":"","CloseCleaning":"매월 셋째주 월요일 02:00~06:00","PointX":35.8571243,"PointY":128.648773},{"StoreSQ":34,"StoreNM":"대구문화점","PhoneNumber":"053-254-0323","NewAddr":"대구광역시 중구 동성로 ","NewAddr2":"2길 95 더락빌딩1, 2F (동성로2가)","AllHour":"Y","Delivery":"Y","Morning":"Y","DriveThrough":"N","OpenTime":"","CloseWeekday":"","ClosePeakSeason":"","CloseCleaning":"Cleaning Day(Close): 매월 둘째주 수요일 02:00~08:00","PointX":35.87016,"PointY":128.5967},{"StoreSQ":35,"StoreNM":"대구범어점","PhoneNumber":"053-764-0331","NewAddr":"대구광역시 수성구 동대구로 ","NewAddr2":"251 (범어동)","AllHour":"N","Delivery":"Y","Morning":"N","DriveThrough":"Y","OpenTime":"10:00","CloseWeekday":"24:00","ClosePeakSeason":"","CloseCleaning":"","PointX":35.8529167,"PointY":128.6247},{"StoreSQ":36,"StoreNM":"대구상인SK점","PhoneNumber":"053-632-0889","NewAddr":"대구광역시 달서구 월배로","NewAddr2":"200 지상1~2층","AllHour":"Y","Delivery":"Y","Morning":"Y","DriveThrough":"Y","OpenTime":"","CloseWeekday":"","ClosePeakSeason":"","CloseCleaning":"Cleaning Day(Close): 매월 둘째주 일요일 02:00~07:00","PointX":35.81802,"PointY":128.535446},{"StoreSQ":273,"StoreNM":"대구성서이마트점","PhoneNumber":"053-583-1332","NewAddr":"대구광역시 달서구 이곡동로","NewAddr2":"24 이마트 성서점 내","AllHour":"N","Delivery":"N","Morning":"N","DriveThrough":"N","OpenTime":"10:00","CloseWeekday":"23:30","ClosePeakSeason":"","CloseCleaning":"","PointX":35.8536377,"PointY":128.5102},{"StoreSQ":217,"StoreNM":"대구시지점","PhoneNumber":"053-791-0331 ","NewAddr":"대구광역시 수성구 신매로 19길 ","NewAddr2":"46 ","AllHour":"N","Delivery":"Y","Morning":"N","DriveThrough":"N","OpenTime":"10:00","CloseWeekday":"23:00 ","ClosePeakSeason":" , ~  24:00 (금요일, 토요일)","CloseCleaning":"","PointX":35.8395042,"PointY":128.707275},{"StoreSQ":233,"StoreNM":"대구율하점","PhoneNumber":"053-959-1126","NewAddr":"대구시 동구 율하동 ","NewAddr2":"1225번지","AllHour":"N","Delivery":"Y","Morning":"N","DriveThrough":"N","OpenTime":"오전10시","CloseWeekday":"오후10시","ClosePeakSeason":"","CloseCleaning":"","PointX":35.8663864,"PointY":128.6961},{"StoreSQ":173,"StoreNM":"대구죽전네거리","PhoneNumber":"053-526-5959","NewAddr":"대구광역시 달서구 달구벌대로","NewAddr2":"1536(현대오일뱅크 주유소內)","AllHour":"N","Delivery":"N","Morning":"N","DriveThrough":"Y","OpenTime":"9:00","CloseWeekday":"23:00","ClosePeakSeason":"","CloseCleaning":"","PointX":35.84952,"PointY":128.535187},{"StoreSQ":61,"StoreNM":"반야월이마트점","PhoneNumber":"053-965-0334","NewAddr":"대구광역시 동구 안심로 ","NewAddr2":"389-2 이마트반야월점內1층 (신서동)","AllHour":"N","Delivery":"N","Morning":"N","DriveThrough":"N","OpenTime":"10:00","CloseWeekday":"22:00","ClosePeakSeason":"","CloseCleaning":"","PointX":35.8708763,"PointY":128.727463},{"StoreSQ":249,"StoreNM":"삼성라이온즈파크점","PhoneNumber":"070-7462-9972","NewAddr":"대구광역시 수성구","NewAddr2":"야구전설로 1 ","AllHour":"N","Delivery":"N","Morning":"N","DriveThrough":"N","OpenTime":"","CloseWeekday":"","ClosePeakSeason":"비경기일 : 11:00~18:00시 (2시간 무료주차가능) / 경기일 : 11:00~ 경기종료까지 / 매주 월요일 휴점","CloseCleaning":"","PointX":35.8410873,"PointY":128.681259}]'
#    testresponse = json.loads(test)
#    for testitem in testresponse:
#        store_nm = testitem["StoreNM"]
#        store_pn = testitem["PhoneNumber"]
#        store_na = testitem["NewAddr"]

    outfile = codecs.open('bk_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|OT@@버거킹\n")

    for areainfo in area:

        while True:
            storeList = getStores(area[areainfo])
            if len(storeList) == 0:
                break

            for store in storeList:
                # outfile.write(u'#%d\n' % n)
                outfile.write(u"버거킹|")
                outfile.write(u'%s|' % store['STOR_NM'])
                outfile.write(u'%s|' % store['TEL_NO'])
                outfile.write(u'%s ' % store['ADDR_1'])
                outfile.write(u'%s|' % store['ADDR_2'])

            break;

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(area_code):
    url = 'http://www.burgerking.co.kr'
    api = '/api/store/searchmap/empty/'
    data = {}
    data['areacd'] = area_code

    params = urllib.urlencode(data)
    print(params)

    try:
        #result = urllib.urlopen(url + api, params)

        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    print(response)
    storeList = json.loads(response)

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()