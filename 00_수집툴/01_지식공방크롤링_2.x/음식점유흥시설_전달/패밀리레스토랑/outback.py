# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import random
import codecs
import urllib
import urllib2
import json
from lxml import html


sido_list2 = {      # 테스트용 시도 목록
    '서울': '11',
}

sido_list = {
    '서울': '11',
    '광주': '29',
    '대구': '27',
    '대전': '30',
    '부산': '26',
    '울산': '31',
    '인천': '28',
    '경기': '41',
    '강원': '42',
    '경남': '48',
    '경북': '47',
    '전남': '46',
    '전북': '45',
    '충남': '44',
    '충북': '43',
    '제주': '50',
    '세종': '36'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('outback_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|ADDR|ETCADDR|FEAT|XCOORD|YCOORD@@아웃백스테이크하우스\n")

    for sidoname in sorted(sido_list):

        page = 1
        while True:
            store_list = getStores(sido_list[sidoname], '')
            if store_list == None: break;
            elif len(store_list) < 1: break

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['etcaddr'])
                outfile.write(u'%s|' % store['feat'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1
            if page == 2: break     # 한번 호출로 광역시도내 정보 다 읽어옴

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/10)
def getStores(sidocode, guguncode):
    url = 'https://www.outback.co.kr'
    api = '/store/storeJsonList.do'
    data = {
        'sggCd': '',
        'searchKeyword': '',
    }
    data['sdCd'] = sidocode
    params = urllib.urlencode(data)
    print(sidocode)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-kr,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        #'Content-Length': 70,
        'Content-Type': 'application/json;charset=UTF-8',
        #'Cookie': 'JSESSIONID=DBBE75A09FB6C761409B66573B6CA849; _ga=GA1.3.572484436.1481311150; wcs_bt=s_2f6be2a35c45:1482483708'
        #'Host': 'www.outback.co.kr',
        #'Origin': 'ttp://www.outback.co.kr',
        #'Referer': 'http://www.outback.co.kr/Store/FindStore.aspx',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)

        #req = urllib2.Request(url + api, params, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        #req.get_method = lambda: 'POST'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['resultData']['storeList']
    print(len(entity_list))

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '아웃백스테이크하우스'
        store_info['subname'] = entity_list[i]['stNm']

        store_info['id'] = entity_list[i]['stIdx']

        store_info['pn'] = ''
        if entity_list[i].get('phone1'):
            store_info['pn'] = entity_list[i]['phone1']
        if entity_list[i].get('phone2'):
            store_info['pn'] += '-' + entity_list[i]['phone2']
        if entity_list[i].get('phone3'):
            store_info['pn'] += '-' + entity_list[i]['phone3']
        if store_info['pn'].startswith('-'): store_info['pn'] = store_info['pn'][-1:]

        store_info['newaddr'] = ''
        if entity_list[i].get('addrN'):
            store_info['newaddr'] = entity_list[i]['addrN']

        store_info['addr'] = ''
        if entity_list[i].get('addrO'):
            store_info['addr'] = entity_list[i]['addrO']

        store_info['etcaddr'] = ''
        if entity_list[i].get('addrDetail'):
            store_info['etcaddr'] = entity_list[i]['addrDetail']

        store_info['feat'] = ''
        if entity_list[i].get('parkingFlag'):
            if entity_list[i]['parkingFlag'] == 'Y':
                store_info['feat'] = '주차가능'

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if entity_list[i].get('lng'):
            store_info['xcoord'] = entity_list[i]['lng']
        if entity_list[i].get('lat'):
            store_info['ycoord'] = entity_list[i]['lat']

        store_list += [store_info]

    return store_list


'''
# v1.0
def getStores(sidoname, gugunname):
    url = 'http://www.outback.co.kr'
    api = '/store/page_store_web_service.aspx/GetStoreSearch'
    data = {
        'baby': '',
        'runch': '',
        'meeting': '',
        'city': '',         # 1 을 넣고 호출하면 서울시 결과값 반환, ''을 넣고 호출하면 전국 결과값 반환
        'gugun': '',
        'keyword': '',
    }
    #data['si'] = sidoname
    #data['gu'] = gugunname
    #params = urllib.urlencode(data)
    params = json.dumps(data)
    print(sidoname + ' ' + gugunname)  # for debugging

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-kr,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        #'Content-Length': 70,
        'Content-Type': 'application/json;charset=UTF-8',
        #'Cookie': 'JSESSIONID=DBBE75A09FB6C761409B66573B6CA849; _ga=GA1.3.572484436.1481311150; wcs_bt=s_2f6be2a35c45:1482483708'
        #'Host': 'www.outback.co.kr',
        #'Origin': 'ttp://www.outback.co.kr',
        #'Referer': 'http://www.outback.co.kr/Store/FindStore.aspx',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }

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
    #print(response)
    response_json = json.loads(response)

    table_json = json.loads(response_json['d'])
    store_list = table_json['Table']

    time.sleep(random.uniform(0.3, 0.9))

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
