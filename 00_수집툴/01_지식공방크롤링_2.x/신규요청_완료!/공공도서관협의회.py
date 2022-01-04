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

    outfile = codecs.open('libraries_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|HOMEPAGE@@도서관\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['homepage'])

        page += 1

        if page == 2: break     # 한 페이지에 정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.kpla.kr'
    api = '/php_subpage.htm'
    data = {
        'php_sub': 'lib_info',
        'php_subpage': 'lib_info',
        'ex': 'htm',
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@class="new_tb01"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 5: continue  # 최소 5개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        store_info['homepage'] = ''

        temp_list = info_list[4].xpath('./a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            if strtemp != None:
                store_info['homepage'] = strtemp.lstrip().rstrip()

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
