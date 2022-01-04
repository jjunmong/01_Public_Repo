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

    outfile = codecs.open('k2_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|XCOORD|YCOORD@@K2\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'K2|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(storeList) < 6: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(intPageNo):
    url = 'https://www.k2.co.kr'
    api = '/k2/ko/customercenter/ajaxStoreInfo'

    data = {
        'address1': '',
        'address2': '',
        'searchWord': '',
        'storeType': 'ALL',
        'specialZone1': '',
        'specialZone2': '',
        'specialZone3': '',
        'showMode': '',
        'rec': '10',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)  # POST 방식일 땐 이렇게 호출해야 함!!!
        req = urllib2.Request(url + api, params)        # header값 맞추기 어려운 경우에는, 그냥 header 정보 없이 호출할 것! (특별한 경우를 빼고는 이렇게 호출해도 됨)
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

    entity_list = response_json['resultObj']['shopInfoList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'K2'
        strtemp = entity_list[i]['displayName']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp

        store_info['newaddr'] = ''
        strtemp = entity_list[i]['streetName']
        if strtemp != None:
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = entity_list[i]['phone1']
        if strtemp != None:
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['longitude']
        store_info['ycoord'] = entity_list[i]['latitude']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
