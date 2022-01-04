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

sido_list2 = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list = {
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
    #'세종': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('blackyak_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|FEAT|XCOORD|YCOORD@@블랙야크\n")

    for sido_name in sorted(sido_list):
        storeList = getStores(sido_name, 'b')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'블랙야크|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|FEAT|XCOORD|YCOORD@@블랙야크키즈\n")

    for sido_name in sorted(sido_list):
        storeList = getStores(sido_name, 'y')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'블랙야크키즈|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(sido_name, store_type):
    url = 'http://member.blackyak.com'
    api = '/store/store_20170301/ajax_storelist.asp'
    data = {
        'isZoom' : '4',
        #'isbk': 'b',
        'keyword': '',
        'lat': '',
        'lon': '',
        'geotype': 'N',
        'format': 'json',
        #'_': '',
    }
    data['isbk'] = store_type
    data['region'] = sido_name
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        urls = url + api + '?' + params
        print(urls)
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = response.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
    #print(response)
    entity_list = json.loads(response)

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '블랙야크'
        store_info['subname'] = ''
        strtemp = entity_list[i]['info1'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['feat'] = ''
        idx = strtemp.find('<span>')
        if idx != -1: strtemp = strtemp[:idx].rstrip()

        if strtemp.startswith('['):     # '[키즈]AK평택'와 같은 지점명 처리
            idx = strtemp.find(']')
            if idx != -1:
                store_info['feat'] = strtemp[1:idx].lstrip().rstrip()
                strtemp = strtemp[idx+1:].lstrip()
        if strtemp.endswith(']'):
            idx = strtemp.rfind('[')
            if idx != -1:
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += strtemp[idx+1:-1].lstrip().rstrip()
                strtemp = strtemp[:idx].rstrip()

        if not strtemp.endswith('점'): strtemp += '점'
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['addr'] = ''
        if entity_list[i].get('info3'): store_info['addr'] = entity_list[i]['info3']

        store_info['pn'] = ''
        if entity_list[i].get('info2'):
            store_info['pn'] = entity_list[i]['info2'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')
        store_info['xcoord'] = ''
        if entity_list[i].get('lng'): store_info['xcoord'] = entity_list[i]['lng']
        store_info['ycoord'] = ''
        if entity_list[i].get('lat'): store_info['ycoord'] = entity_list[i]['lat']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
