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

    outfile = codecs.open('megamart_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OT|OFFDAY|XCOORD|YCOORD@@메가마트\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['offday'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/9)
def getStores(intPageNo):
    url = 'http://home.megamart.com'
    api = '/boardApi/query'
    data = {
        'method': 'store.selectStore',
        'applyCamelCase': 'true',
    }
    params = urllib.urlencode(data)
    # print(params)

    # Cookie값 없으면 호출 실패
    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        #'Cache-Control': 'max-age=0',
        #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #'Cookie': 'WMONID=My5Yu9p9Itm; JSESSIONID=k9vzvGGghu9Y21BHIsEgGBH16CU9AMjLRDazw225QQVx32Dz0D4lNO1NekG8sOIA.sen-pacwas2_servlet_hkwwas',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    try:
        req = urllib2.Request(url+api, params)
        #req = urllib2.Request(url+api, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);
        return None

    response = result.read()
    entity_list = json.loads(response)

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '메가마트'
        store_info['subname'] = entity_list[i]['storeName']
        store_info['id'] = entity_list[i]['storeCode']

        store_info['newaddr'] = entity_list[i]['address']
        store_info['ot'] = entity_list[i]['businessTime'].replace(' ', '')
        store_info['offday'] = entity_list[i]['holiday'].replace(' ', '')
        store_info['xcoord'] = entity_list[i]['lon']
        store_info['ycoord'] = entity_list[i]['lat']
        store_info['pn'] = entity_list[i]['telNumber'].replace(' ', '')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
