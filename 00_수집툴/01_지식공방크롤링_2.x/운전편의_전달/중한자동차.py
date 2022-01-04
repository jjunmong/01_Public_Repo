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

    outfile = codecs.open('zhmotors_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|X|Y@@중한자동차\n")

    page = 1
    while True:
        store_list = getStores2(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'신원CK모터스|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['x'])
            outfile.write(u'%s\n' % store['y'])

        page += 1

        if page == 299: break
        elif len(store_list) < 3: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2/0 (2019/1)
def getStores2(intPageNo):
    # 'http://www.zhmotors.com/home/sub.php?menukey=72&page=3&scode=00000000'
    url = 'http://www.zhmotors.com'
    api = '/home/sub.php'
    data = {
        'menukey': '72',
        'scode': '00000000',
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="agent_list"]//div[@class="agent_list_wrap"]')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//h3')
        addr_list = entity_list[i].xpath('.//p')
        pn_list = entity_list[i].xpath('.//address')
        info_list = entity_list[i].xpath('.//ul[@class="cf"]//li//a/@onclick')

        if len(name_list) < 1: continue

        store_info = {}

        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('총 대리점', '총대리점').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        if len(addr_list) > 0:
            strtemp = "".join(addr_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if strtemp.startswith('['):     # '[17311] 경기도 이천시 백사면 이여로 260' <= 여기서 우편번호 '[17311]' 제거
                    idx = strtemp.find(']')
                    if idx != -1: strtemp = strtemp[idx+1:].lstrip()
                store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        if len(pn_list) > 0:
            strtemp = "".join(pn_list[0].itertext())
            if strtemp != None:
                store_info['pn'] = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('.', '-').replace(')', '-').rstrip().lstrip()

        store_info['x'] = ''
        store_info['y'] = ''
        if len(info_list) >= 2:
            strtemp = info_list[1]
            idx = strtemp.find('gomap(')
            if idx != -1:
                coord_list = strtemp[idx+6:].lstrip().split(',')
                if len(coord_list) >= 2:
                    store_info['x'] = coord_list[0].replace('\'', '').lstrip().rstrip()
                    store_info['y'] = coord_list[1].replace('\'', '').lstrip().rstrip()

        store_list += [store_info]

    return store_list

# v1.0
def getStores(intPageNo):
    url = 'http://www.zhmotors.com'
    api = '/shop_contents/myboard_list.htm'
    data = {
        'myboard_code': 'network',
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="store_list"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 3: continue  # 최소 3개 필드 있어야 함

        store_info = {}

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').replace('총 대리점', '총대리점')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None: store_info['pn'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').replace('.', '-').replace(')', '-')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
