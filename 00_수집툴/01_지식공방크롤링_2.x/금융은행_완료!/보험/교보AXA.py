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
import ast
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

    outfile = codecs.open('kyoboaxa_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ADDR@@AXA손해보험\n")

    # 지점 정보
    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['addr'])

        page += 1

        if page == 2: break     # 한번 호출로 전국 점포정보 모두 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    # 본사 정보
    store_list = getStores2()
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['addr'])

    outfile.close()


def getStores(intPageNo):
    # 'https://www.axa.co.kr/AsianPlatformInternet/html/axacms/shcl/auto/find/index.html'
    url = 'https://www.axa.co.kr'
    api = '/AsianPlatformInternet/html/axacms/shcl/auto/find/index.html'
    data = {}
    #params = urllib.urlencode(data)
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

        #result = urllib.urlopen(url+api+'?'+params)
        result = urllib.urlopen(url + api)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200 and code != 304:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    entity_list = tree.xpath('//tbody[@id="lBody"]//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = 'AXA손해보험'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        store_info['addr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find('(구주소')
            if idx != -1:
                store_info['newaddr'] = strtemp[:idx].rstrip()
                strtemp = strtemp[idx+4:].lstrip()
                if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                if strtemp.endswith(')'): strtemp = strtemp[:-1].rstrip()
                store_info['addr'] = strtemp
            else:
                store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_list += [store_info]

    return store_list

# 본사 정보 수집
def getStores2():
    try:
        result = urllib.urlopen('https://www.axa.co.kr/AsianPlatformInternet/html/axacms/common/intro/intro/contact/index.html')
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    info_list = tree.xpath('//div[@class="cont_right"]//dl//dd')

    if len(info_list) < 2: return None

    store_list = []
    store_info = {}
    store_info['name'] = 'AXA손해보험'
    store_info['subname'] = '본사'

    store_info['addr'] = ''
    store_info['newaddr'] = ''
    strtemp = "".join(info_list[0].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        if strtemp[0] >= '0' and strtemp[0] <= '9': # 우편번호 삭제
            idx = strtemp.find(' ')
            if idx != -1: strtemp = strtemp[idx+1:].lstrip()
        store_info['newaddr'] = strtemp

    store_info['pn'] = ''
    strtemp = "".join(info_list[1].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        strtemp = strtemp.replace('대표전화', '').replace(':', '').rstrip().lstrip()
        store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

    store_list += [store_info]
    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
