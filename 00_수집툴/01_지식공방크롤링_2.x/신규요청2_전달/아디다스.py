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

    outfile = codecs.open('adidas_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|TYPE\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['type'])

        page += 1

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://shop.adidas.co.kr'
    api = '/PF110101.action'
    data = {
        'command': 'LIST_2',
        'gubn': 'first',
        'paramGubn': 'undefined',
        'STORE_NM_PRE': '',
        'SIDO_NM': '전체',
        'GUN_NM': '전체',
        'BRAND': 1,
        'STORE_ID': '',
        'STORE_DIVI': '',
        'STORE_DIVI_NM': '',
        'STORE_DIVI_SUB': '',
        'STORE_DIVI_SUB_NM': '',
        'PAGE_LEN': '',
        'CLUB_YN': '',
        'STORE_DIVI_SUB_NM': 'N',
        'STORE_NM': '',
    }
    data['PAGE_CUR'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    try:
        urls = url + api
        #print(urls)
        req = urllib2.Request(urls, params)
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
    entity_list = response_json['storeList2']['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '아디다스'
        store_info['subname'] = ''
        strtemp = entity_list[i]['STORE_NM']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['DORO_ADDR'] + ' ' + entity_list[i]['DORO_DTL_ADDR']
        store_info['addr'] = entity_list[i]['ADDR'] + ' ' + entity_list[i]['DTL_ADDR']
        store_info['pn'] = entity_list[i]['TEL_NO'].lstrip().rstrip().replace(' ', '')

        store_info['type'] = entity_list[i]['STORE_DIVI_NM']

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
