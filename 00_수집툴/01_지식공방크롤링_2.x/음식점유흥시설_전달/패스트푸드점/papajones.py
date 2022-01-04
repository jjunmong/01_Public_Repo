# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
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

    outfile = codecs.open('papajones_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|XCOORD|YCOORD@@파파존스피자\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'파파존스피자|')
            outfile.write(u'%s|' % store['szname'])
            outfile.write(u'%s|' % store['szphone1'])

            store_addr = store['szaaddr']
            if store_addr != None:      # 불필요한 문자들 제거
                store_addr = store_addr.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            outfile.write(u'%s|' % store_addr)

            shop_feats = ''
            if store['szpark'] == 'Y':
                shop_feats += '주차'
            outfile.write(u'%s|' % shop_feats)      # 다른 속성 정보들도 해석해서 추가할 것!!!

            outfile.write(u'%s|' % store['szxasix'])
            outfile.write(u'%s\n' % store['szyasix'])

        page += 1

        if page == 2: break     # 한 페이지에 모든 정보 다 있음

        time.sleep(random.uniform(0.3, 0.9))
        time.sleep(delay_time)

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.pji.co.kr'
    api = '/get.do'
    data = {
        'ex': 'Store',
        'ac': 'getstores',
        'szdocd': '',
        'szsicd': '',
        'szname': '',
        'szstoreid': '',
    }
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    storeList = json.loads(response)
    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
