# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
import urllib2
import random
import json
from lxml import html

sido_list = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list2 = {
    '서울': '02',
    '광주': '062',
    '대구': '053',
    '대전': '042',
    '부산': '051',
    '울산': '052',
    '인천': '032',
    '경기': '031',
    '강원': '033',
    '경남': '055',
    '경북': '054',
    '전남': '061',
    '전북': '063',
    '충남': '041',
    '충북': '043',
    '제주': '064',
    '세종': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('lgbestshop_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|PARKING|XCOORD|YCOORD\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'LG전자베스트샵|')
            outfile.write(u'%s|' % store['agName'])
            outfile.write(u'%s|' % store['agTel'])

            shop_addr = ''
            if store['agAddr1'] != None:
                shop_addr = store['agAddr1']
                if store['agAddr2'] != None:
                    shop_addr += ' '
                    shop_addr += store['agAddr2']
            outfile.write(u'%s|' % shop_addr)

            shop_newaddr = ''
            if store['agNAddr1'] != None:
                shop_newaddr = store['agNAddr1']
                if store['agNAddr2'] != None:
                    shop_newaddr += ' '
                    shop_newaddr += store['agNAddr2']
            outfile.write(u'%s|' % shop_newaddr)

            shop_ot = '평일'
            if store['agWeekday'] != None:
                shop_ot += store['agWeekday']
            shop_ot += ';주말'
            if store['agSaturday'] != None:
                shop_ot += store['agSaturday']
            outfile.write(u'%s|' % shop_ot)

            strtemp = store['agGuide']
            if strtemp != None:     # line feed 문자가 포함되어 있는 경우가 있어서...
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            outfile.write(u'%s|' % strtemp)

            outfile.write(u'%s|' % store['agGpsY'])
            outfile.write(u'%s\n' % store['agGpsX'])

        page += 1

        if page == 2: break     # 한 페이지에 모든 정보 다 있음

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.lge.co.kr'
    api = '/lgekor/bestshop/retrieveBestshopMobileList.do'
    data = {
     }
    data['page'] = intPageNo

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }

    params = 'currentLatitude=37.49456669588779&currentLongitude=127.06176171703245&si=&gu='

    try:
        req = urllib2.Request(url + api, params, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'euc-kr')
    print(response)
    storeList = json.loads(response)
    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
