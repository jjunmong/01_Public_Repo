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

    outfile = codecs.open('koreaeximbank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@수출입은행\n")

    # 본부 정보 얻기
    store_list = getStores('본점', 'https://www.koreaexim.go.kr/site/homepage/menu/viewMenu?menuid=001005006003001001', 0)
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    time.sleep(random.uniform(0.3, 0.9))

    store_list = getStores('부산국제금융센터', 'https://www.koreaexim.go.kr/site/homepage/menu/viewMenu?menuid=001005006003002001', 0)
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    time.sleep(random.uniform(0.3, 0.9))

    # 지점 정보 얻기
    store_list = getStores('지점', 'https://www.koreaexim.go.kr/site/homepage/menu/viewMenu?menuid=001005006003003001', 0)
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    time.sleep(random.uniform(0.3, 0.9))

    store_list = getStores('인재개발원', 'https://www.koreaexim.go.kr/site/homepage/menu/viewMenu?menuid=001005006003005', 0)
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    time.sleep(random.uniform(0.3, 0.9))

    store_list = getStores('수출중소기업지원센터', 'https://www.koreaexim.go.kr/site/homepage/menu/viewMenu?menuid=001005006003006001', 0)
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    outfile.close()


def getStores(store_type, urls, subapi_flag):
    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        print(urls)     # for debugging
        #req = urllib2.Request(url + api, None, headers=hdr)
        req = urllib2.Request(urls, None)
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

    store_list = []
    temp_list = tree.xpath('//ul[@class="tab-map"]//a')
    if len(temp_list) > 0 and subapi_flag == 0:
        for j in range(len(temp_list)):
            subname = temp_list[j].text
            if not subname.endswith(store_type): subname += store_type
            suburls = 'https://www.koreaexim.go.kr' + temp_list[j].xpath('./@href')[0]
            time.sleep(random.uniform(0.3, 0.9))
            store_list += getStores(subname, suburls, 1)

        return store_list

    entity_list = tree.xpath('//div[@class="write_type_h1 mt2"]//tbody')

    for i in range(len(entity_list)):
        tag_list = entity_list[i].xpath('.//th')
        value_list = entity_list[i].xpath('.//td')
        if len(tag_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '한국수출입은행'

        store_info['subname'] = ''
        if store_type != '':
            store_info['subname'] = store_type

        store_info['newaddr'] = '';     store_info['pn'] = ''

        for j in range(len(tag_list)):
            tag = "".join(tag_list[j].itertext())
            value = "".join(value_list[j].itertext())
            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').lstrip().rstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

            if tag == '주소':
                if value.startswith('('):   # 우편번호 정보 제거
                    idx = value.find(')')
                    value = value[idx+1:].lstrip()
                store_info['newaddr'] = value
            elif tag == '전화번호': store_info['pn'] = value

        store_info['xcoord'] = '';        store_info['ycoord'] = ''
        temp_list = tree.xpath('//div[@class="map_area mt2"]//iframe/@src')
        if len(temp_list) > 0:
            strtemp = temp_list[0]  # '/site/inc/map/mapload?query=한국수출입은행&amp;menuid=001005006003001002&amp;wsize=898&amp;hsize=453&amp;coordx=126.9234185&amp;coordy=37.5286245'
            idx = strtemp.rfind('coordy=')
            if idx != -1:
                store_info['ycoord'] = strtemp[idx+7:]
                strtemp = strtemp[:idx]
                idx = strtemp.rfind('coordx=')
                store_info['xcoord'] = strtemp[idx+7:].replace('&amp;', '')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
