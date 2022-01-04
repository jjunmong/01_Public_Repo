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

    outfile = codecs.open('jeonbukbank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|ETCADDR@@전북은행\n")


    for i in range(1,6):    # area code : 1 ~5
        page = 1
        while True:
            store_list = getStores(i, page)
            if store_list == None: break;

            count=0
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['etcaddr'])

                count += 1
                if count >= 5: break    # 5번째 값 이후의 값들은 중복된 결과들...

            page += 1

            if page == 19: break
            elif len(store_list) < 5: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(area_code, intPageNo):
    url = 'https://www.jbbank.co.kr'
    api = '/EBCIB_CMBRC_C_R001_01.jct'
    #api = '/EBCIB_CMBRC_C_R001_01.jct?jexSendIdx=1492671068453_2'
    data = {}
    #params = urllib.urlencode(data)
    #print(params)
    params = '_JSON_=%257B%2522PT_HEADER%2522%253A%257B%257D%252C%2522PAGEINDEX%2522%253A%25222%2522%252C%2522PAGECNT%2522%253A5%252C%2522BR_DIV%2522%253A%25221%2522%252C%2522BR_365_DIV%2522%253A%25222%2522%252C%2522AREA_DIV_S1%2522%253A%25221%2522%252C%2522BROF_NM%2522%253A%2522%2522%257D'
    params = '_JSON_=%257B%2522PT_HEADER%2522%253A%257B%257D%252C%2522PAGEINDEX%2522%253A%2522' + str(intPageNo)
    params += '%2522%252C%2522PAGECNT%2522%253A5%252C%2522BR_DIV%2522%253A%25221%2522%252C%2522BR_365_DIV%2522%253A%25222%2522%252C%2522AREA_DIV_S1%2522%253A%2522' + str(area_code)
    params += '%2522%252C%2522BROF_NM%2522%253A%2522%2522%257D'

    strtemp = urllib.unquote(params).decode('utf8')

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)
        req = urllib2.Request(url + api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(str(area_code) + ',' + str(intPageNo))    # for debugging
    print(response)     # for debugging
    response_json = json.loads(response)

    entity_list = response_json['GRID']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '전북은행'
        store_info['id'] = entity_list[i]['BROF_CD']
        store_info['subname'] = ''
        strtemp = entity_list[i]['BROF_NM']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            if not strtemp.endswith('지점') and strtemp != '본점': strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['INBN_ADDR']
        store_info['etcaddr'] = entity_list[i]['INBN_WHOL_ADDR']
        store_info['pn'] = entity_list[i]['INBN_TLNO'].replace(')', '-')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
