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

    outfile = codecs.open('jaguar_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|SUBNAME2\n")

    page = 1
    for page in range(1,2,1):       # 한번 호출로 전체 지점 정보 다 얻어 옴
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['subname2'])

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://local.jaguarkorea.co.kr'
    api = '/dealer/w/dealer.asp'

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
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@class="dealer"]//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue

        store_info = {}

        store_info['name'] = '재규어'
        store_info['subname'] = '';        store_info['subname2'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('|')
            if idx != -1:
                store_info['subname2'] = strtemp[idx+1:].lstrip().replace(' ', '/')
                strtemp = strtemp[:idx].rstrip()
                if not strtemp.endswith('전시장'): strtemp += '전시장'
                store_info['subname'] = strtemp.replace(' ', '/')
            else: store_info['subname'] = strtemp.replace(' ', '/')

        store_info['addr'] = '';        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('(')
            if idx != -1:
                store_info['newaddr'] = strtemp[:idx].rstrip()
                store_info['addr'] = strtemp[idx+1:-1].lstrip().rstrip()
            else: store_info['newaddr'] = strtemp

        store_info['pn'] = '';
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace(' ', '').replace('.', '-').replace(')', '-')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
