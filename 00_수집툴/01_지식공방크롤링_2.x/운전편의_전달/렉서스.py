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

    outfile = codecs.open('lexus_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|WEBSITE|XCOORD|YCOORD@@렉서스\n")

    page = 1
    while True:
        store_list = getStores(page, '전시장')
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전체 점포 정보 모두 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo, postfix):
    url = 'http://lexus.co.kr'
    api = '/data/json/getData_find_dealers.php?dealer=official&page_id=find_dealers'
    try:
        urls = url + api
        print(urls)
        req = urllib2.Request(urls, '')
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    # print(response)
    location_list = json.loads(response)['find_dealers']['locations']
    if location_list == None: return None

    store_list = []
    for i in range(len(location_list)):
        entity_list = location_list[i]['branches']
        for j in range(len(entity_list)):
            store_info = {}
            store_info['name'] = '렉서스'

            strtemp = entity_list[j]['text'].replace('렉서스', '').lstrip().rstrip()
            if not strtemp.endswith(postfix): strtemp += postfix
            store_info['subname'] = strtemp.replace(' ', '/')

            store_info['newaddr'] = entity_list[j]['addr']
            store_info['pn'] = entity_list[j]['tel'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

            store_info['website'] = entity_list[j]['link_dealer']

            store_info['xcoord'] = entity_list[j]['map']['longitude']
            store_info['ycoord'] = entity_list[j]['map']['latitude']

            store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
