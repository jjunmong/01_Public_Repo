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

    outfile = codecs.open('redtable_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ID|NEWADDR|TYPE|TYPE2|ORGNAME|SOURCE2@@레드테이블\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['type2'])
            outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s\n' % u'레드테이블')

        page += 1

        if page == 500: break
        elif len(store_list) < 12: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://redtable.kr/api2.php?cmd=getRestaurantAward&index=24&limit=12&city=seoul
    url = 'http://redtable.kr'
    api = '/api2.php'
    data = {
        'cmd': 'getRestaurantAward',
        'limit': '12',
        'city': 'seoul',
    }
    data['index'] = (intPageNo-1)*12
    params = urllib.urlencode(data)
    #print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
        urls = url + api + '?' + params
        print(urls)
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    entity_list = json.loads(response)

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = ''
        strtemp = entity_list[i]['attributes']['name'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['subname'] = strtemp
        store_info['name'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['attributes']['address']
        store_info['pn'] = ''
        store_info['id'] = entity_list[i]['attributes']['id']
        store_info['type'] = entity_list[i]['attributes']['cat01']
        store_info['type2'] = entity_list[i]['attributes']['cat02']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
