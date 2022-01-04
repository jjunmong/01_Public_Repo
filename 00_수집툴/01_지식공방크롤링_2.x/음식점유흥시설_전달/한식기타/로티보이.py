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

    outfile = codecs.open('rotiboy_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|FEAT@@로티보이\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'로티보이|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 99: break
        elif len(storeList) < 16: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/6)
def getStores(intPageNo):
    # 'http://rotiboykr.dahanw.gethompy.com/gnuboard4/bbs/board.php'
    url = 'http://rotiboykr.dahanw.gethompy.com'
    api = '/gnuboard4/bbs/board.php'
    data = {
        'bo_table': 'sub0301',
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
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)    # for debugging
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    #tree = html.fromstring('<head><meta charset="utf-8"/></head>' + response)

    entity_list = tree.xpath('//table[@id="board_list"]//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        subname = "".join(info_list[1].itertext()).replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        store_info['subname'] = subname.replace(' ', '/')

        store_info['addr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-')

        store_info['feat'] = ''

        store_list += [store_info]

    return store_list

# v1.0
'''
def getStores(intPageNo):
    url = 'http://www.rotiboy.kr'
    api = '/front/store/store_list.php'
    data = {
        'idx': '',
        'dSido': '',
        'dGugun': '',
        'dSearchStr': '',
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
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)    # for debugging
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    #tree = html.fromstring('<head><meta charset="utf-8"/></head>' + response)

    entity_list = tree.xpath('//div[@class="boardList"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        subname = "".join(info_list[1].itertext()).strip('\r\t\n')
        store_info['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        store_info['addr'] = ''
        strtemp = "".join(info_list[2].itertext()).strip('\r\t\n')
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext()).strip('\r\t\n')
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-')

        store_info['feat'] = ''
        feat_list = info_list[4].xpath('.//img/@alt')
        for j in range(len(feat_list)):
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_list[j].replace('온라인주문 가능', '온라인주문').replace('배달가능', '배달').replace('와이파이존', '와이파이')

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
