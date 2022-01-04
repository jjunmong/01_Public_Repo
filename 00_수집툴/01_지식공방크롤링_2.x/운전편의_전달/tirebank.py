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

    outfile = codecs.open('tirebank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|XCOORD|YCOORD\n")

    page = 1
    while True:
        storeList = getStores('')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'타이어뱅크|')
            outfile.write(u'%s|' % store['ST_NAME'].replace(' ', '/'))
            outfile.write(u'%s|' % store['ST_TEL'].replace(')', '-'))
            outfile.write(u'%s|' % store['ST_ADDRESS'])
            outfile.write(u'%s|' % store['ST_LNG'])
            outfile.write(u'%s\n' % store['ST_LAT'])

        break;

    outfile.close()

def getStores(type_info):
    url = 'http://www.tirebank.com'
    api = '/home/get_store_list'
    data = {
        'skey': 'ST_NAME',
        'sval': '',
     }
    params = urllib.urlencode(data)

    formdata = 'csrftestname=d201fef546be7057739339ee48535085&my_lat=&my_lng=&n=37.769591509648876&w=126.50695890234374&s=37.33409454777454&e=127.50122159765624'

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=sm7h8s2duqhbeq90qhdo1cp555; 2a0d2363701f23f8a75028924a3af643=MTI1LjEyOS4yNDIuMjI3; _gat=1; _ga=GA1.3.1065939222.1486961929'
    }

    try:
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)

        #req = urllib2.Request(url + api + '?' + params, formdata, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        ##req = urllib2.Request(url + api, params, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        #req.get_method = lambda: 'POST'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)
    response_json = json.loads(response)
    return response_json['data']

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
