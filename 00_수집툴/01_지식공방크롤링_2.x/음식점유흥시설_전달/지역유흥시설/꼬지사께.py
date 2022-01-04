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

    outfile = codecs.open('kkojisakke_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@꼬지사께\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.kkojisakke.com'
    api = '/new/board/index.php'
    data = {
        'board': 'map_01',
        'sca': 'all',
        'type': 'list',
        'select': '',
        'search': '',
        'now_date': '',
    }
    data['page'] = intPageNo
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
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)
    #tree = html.fromstring('<head><meta charset="utf-8"/></head>' + response)

    entity_list = tree.xpath('//div[@class="store_text f_right"]')

    store_list = []
    for i in range(len(entity_list)):
        subname_list = entity_list[i].xpath('.//p')
        info_list = entity_list[i].xpath('.//dd')

        if len(subname_list) < 1 or len(info_list) < 2: continue  # 필수 필드 숫자 체크

        store_info = {}
        store_info['name'] = '꼬지사께'

        store_info['subname'] = '';     store_info['feat'] = ''
        strtemp = "".join(subname_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None: store_info['newaddr'] = strtemp.rstrip().lstrip()

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None: store_info['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
