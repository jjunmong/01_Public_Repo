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

    outfile = codecs.open('stock_meritz_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ORGNAME|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@메리츠종금증권\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전체 점포 정보 얻을 수 있음

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/2)
def getStores(intPageNo):
    url = 'https://home.imeritz.com'
    api = '/bsbr/getSearch.do'
    data = {
    }
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript,*/*;q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)
    response_json = json.loads(response)
    entity_list = response_json['bsbrinfoList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '메리츠종금증권'
        strtemp = entity_list[i]['bsbrName'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['bsbrTurnNo']

        store_info['newaddr'] = entity_list[i]['addr']
        store_info['pn'] = entity_list[i]['wholTelno'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['xcoord'] = entity_list[i]['gpsLonVal']
        store_info['ycoord'] = entity_list[i]['gpsLatVal']

        store_list += [store_info]

    return store_list

'''
# v1.0
def getStores(intPageNo):
    url = 'http://home.imeritz.com'
    api = '/bsbr/getSearch.do'
    data = {
        'search1': '%',
    }
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['bsbrinfoList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '메리츠종금증권'
        strtemp = entity_list[i]['bsbrName'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['bsbrTurnNo']

        store_info['newaddr'] = entity_list[i]['addr']
        store_info['pn'] = entity_list[i]['wholTelno'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['xcoord'] = entity_list[i]['gpsLonVal']
        store_info['ycoord'] = entity_list[i]['gpsLatVal']

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
