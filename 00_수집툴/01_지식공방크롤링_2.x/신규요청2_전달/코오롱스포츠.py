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

    outfile = codecs.open('kolonsport_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|TYPE|XCOORD|YCOORD\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            #if store['type'] == '직영점' : continue
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2017/11)
def getStores(intPageNo):
    url = 'https://www.kolonsport.com'
    api = '/Store/Search'
    data = {
        'brand': 'KS',
        'region': '',
        'searchWord': '',
        'storeType': '',
    }
    data['currentPage'] = intPageNo
    params = urllib.urlencode(data)
    #print(params)

    try:
        urls = url + api + '?' + params
        print(urls)  # for debugging
        result = urllib.urlopen(urls)

        #urls = url + api
        #req = urllib2.Request(urls, params)
        #req.get_method = lambda: 'GET'     // 이렇게 호출하면 다른 결과값 반환, 2페이지도 1페이지와 동일한 결과값 반환???
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['resultList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '코오롱스포츠'
        store_info['subname'] = ''
        strtemp = entity_list[i]['displayName']
        if strtemp != None:
            strtemp = convert_full_to_half_string(strtemp)
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('FnC부문')
            if idx != -1: strtemp = strtemp[idx+5:].lstrip()
            idx = strtemp.find('FNC부문')
            if idx != -1: strtemp = strtemp[idx+5:].lstrip()
            idx = strtemp.find('FnC코오롱')
            if idx != -1: strtemp = strtemp[idx+6:].lstrip()

            if strtemp.startswith('코오롱스포츠'): strtemp = strtemp[6:].lstrip()
            elif strtemp.startswith('코오로스포츠'): strtemp = strtemp[6:].lstrip()
            elif strtemp.startswith('코오롱상사'): strtemp = strtemp[5:].lstrip()
            elif strtemp.startswith('(주)'): strtemp = strtemp[3:].lstrip()
            elif strtemp.startswith('주)'): strtemp = strtemp[2:].lstrip()
            strtemp = strtemp.replace('(주)', '').replace('주식회사', '').replace('코오롱스포츠', '').replace('코오롱 스포츠', '').replace('  ', ' ')

            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        store_info['pn'] = ''
        store_info['ot'] = ''

        if entity_list[i].get('address'): store_info['newaddr'] = convert_full_to_half_string(entity_list[i]['address'])
        if entity_list[i].get('phone'): store_info['pn'] = entity_list[i]['phone'].lstrip().rstrip().replace(' ', '')
        if entity_list[i].get('openTime') and entity_list[i].get('closeTime'):
            store_info['ot'] = entity_list[i]['openTime'].replace('2016-08-15', '').lstrip() + '-' + entity_list[i]['closeTime'].replace('9999-12-31', '').lstrip()

        store_info['type'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if entity_list[i].get('storeType'): store_info['type'] = entity_list[i]['storeType']
        if entity_list[i].get('longitude'): store_info['xcoord'] = entity_list[i]['longitude']
        if entity_list[i].get('latitude'): store_info['ycoord'] = entity_list[i]['latitude']

        store_list += [store_info]

    return store_list

"""
# v1.0
def getStores(intPageNo):
    url = 'http://www.kolonsport.com'
    api = '/api/cms/ft_store/storeList.json'
    data = {
        'site_id': 'kolonsport',
        'store_codes': 'kolonsport',
        'store_type': '',
        'address': '',
        'store_name': '',
        'page_size': 10,
    }
    data['page'] = intPageNo
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
    entity_list = response_json['items']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '코오롱스포츠'
        store_info['subname'] = ''
        strtemp = entity_list[i]['store_name']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('코오롱스포츠'): strtemp = strtemp[6:].lstrip()
            elif strtemp.startswith('코오로스포츠'): strtemp = strtemp[6:].lstrip()
            idx = strtemp.find('FnC부문')
            if idx != -1: strtemp = strtemp[idx+5:].lstrip()
            idx = strtemp.find('FNC부문')
            if idx != -1: strtemp = strtemp[idx+5:].lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = convert_full_to_half_string(entity_list[i]['address'])
        store_info['pn'] = entity_list[i]['phone'].lstrip().rstrip().replace(' ', '')
        store_info['ot'] = entity_list[i]['opening_time'] + '-' + entity_list[i]['closing_time']

        store_info['type'] = entity_list[i]['store_type']
        store_info['xcoord'] = entity_list[i]['map_y']
        store_info['ycoord'] = entity_list[i]['map_x']

        store_list += [store_info]

    return store_list
"""

def convert_full_to_half_char(ch):
    codeval = ord(ch)
    if 0xFF00 <= codeval <= 0xFF5E:
        ascii = codeval - 0xFF00 + 0x20;
        return unichr(ascii)
    else:
        return ch


def convert_full_to_half_string(line):
    output_list = [convert_full_to_half_char(x) for x in line]
    return ''.join(output_list)

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
