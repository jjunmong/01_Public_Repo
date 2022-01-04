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
#import json
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

    outfile = codecs.open('suhyupbank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR@@수협은행\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 99: break
        elif len(store_list) < 12: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://suhyup.tritops.co.kr'
    api = '/list.jsp'
    data = {
        'sido': '',
        'sigungu': '',
        'gubun': '1',
        'search_gb': '',
        'search_type': 'left_addr',
        'seq_no': '',
        'type': 'bank',
        'search_word': '',
        'search_addr': '',
    }
    data['pg'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    try:
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="boardWrap"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        name_list = entity_list[i].xpath('.//th')
        info_list = entity_list[i].xpath('.//td')
        if len(name_list) < 1 or len(info_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}

        store_info['name'] = '수협은행'

        store_info['subname'] = ''
        temp_list = info_list[0].xpath('./@title')
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')
        if len(temp_list) > 0:      # subname이 '제2국제여객선터미...' 이렇게 추출되는 경우가 있어서 추출방법 변경
            store_info['subname'] = temp_list[0].lstrip().rstrip().replace(' ', '/')

        store_info['newaddr'] = '';     store_info['addr'] = ''
        addr_list = info_list[2].xpath('.//span/@title')
        if len(addr_list) > 0:
            store_info['addr'] = addr_list[0]
        if len(addr_list) > 1:
            store_info['newaddr'] = addr_list[1]

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace(')', '-')

        store_list += [store_info]

        # info_list[2]에 ID 정보 있음 (필요할 때 추출할 것!!)

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
