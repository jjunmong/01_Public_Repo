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

    outfile = codecs.open('mantruck_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@만트럭\n")

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

        if page == 2: break     # 한번 호출로 전국 지점 정보 모두 얻을 수 있음
        elif len(store_list) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://mantruck.co.kr'
    api = '/dealer/'
    data = {}
    params = urllib.urlencode(data)
    # print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Encoding': 'deflate, br',   # gzip 포함되어 있으면 압축 포맷으로 반환
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        urls = url + api
        print(urls)
        #req = urllib2.Request(urls, params)
        req = urllib2.Request(urls, params, headers=hdr)        # header 없이 호출하면 403 에러 반환
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

    name_list = tree.xpath('//div[@class="vc_toggle_title"]')
    entity_list = tree.xpath('//div[@class="vc_toggle_content"]')

    store_list = []
    for i in range(len(name_list)):

        info_list = entity_list[i].xpath('.//li')
        if len(info_list) < 4: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = '만트럭'
        store_info['subname'] = ''
        strtemp = "".join(name_list[i].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('주소:', '').rstrip().lstrip()
            idx = strtemp.find('/')
            if idx != -1: store_info['newaddr'] = strtemp[:idx].rstrip()
            else: store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('지점연락처:', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_list += [store_info]

    # 출고사무소 정보 추가
    name_list = tree.xpath('//div[@class="vc_cta3-content"]//h2')
    info_list = tree.xpath('//div[@class="vc_cta3-content"]//ul//li//p')

    if len(name_list) > 0 and len(info_list) > 2:
        store_info = {}

        store_info['name'] = '만트럭'
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('주소:', '').rstrip().lstrip()
            idx = strtemp.find('/')
            if idx != -1: store_info['newaddr'] = strtemp[:idx].rstrip()
            else: store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('문의:', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace('.', '-').replace('|', ';')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
