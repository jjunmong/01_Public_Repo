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

    outfile = codecs.open('medipharm_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|X|Y@@메디팜약국\n")

    page = 1
    retry_count = 0
    while True:
        store_list = getStores(page)
        if store_list == None:
            if retry_count >= 3: break
            else: retry_count += 1; continue

        retry_count = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 199: break       # 2018년7월 508개 약국 있음
        elif len(store_list) < 6: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'https://www.medipharm.co.kr/mediStore/mediStore_040700.asp?seq=&pageNo=1&schKind=2&schText=%B8%DE%B5%F0%C6%CA'
    url = 'https://www.medipharm.co.kr'
    api = '/mediStore/mediStore_040700.asp'
    data = {}
    params = 'seq=&pageNo=' + str(intPageNo) + '&schKind=2&schText=%BE%E0%B1%B9'
    #print(params)

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

    # 앞에 이상한 문자들이 포함되어 있어서 잘라냄 ㅠㅠ
    idx = response.find('<title>')
    if idx != -1: response = response[idx:]

    response = unicode(response, 'euc-kr')  # 'euc-kr' 인코딩값 반환
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)

    entity_list = tree.xpath('//table[@class="table table-style-1"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        pn_list = entity_list[i].xpath('.//span[@class="num ml_10"]')
        href_list = entity_list[i].xpath('.//a/@href')
        if len(info_list) < 2: continue  # 최소 2개 필드 있어야 함

        store_info = {}

        store_info['name'] = '메디팜'
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('메디팜'): strtemp = strtemp[3:].lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['addr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        if len(pn_list) > 0:
            strtemp = "".join(pn_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if len(href_list) > 0:
            strtemp = href_list[0]  # '"javascript:openPop('http://www.medipharm.co.kr/inc/map.asp?coord1=36.6708894&coord2=127.4825038&pname=메디팜가정약국', 'winMap', 950, 450, 'no');'
            idx1 = strtemp.find('coord1=')
            idx2 = strtemp.find('&pname=')
            if idx1 != -1 and idx2 != -1:
                strtemp = strtemp[idx1+7:idx2]
                idx = strtemp.find('&coord2=')
                if idx != -1:
                    store_info['ycoord'] = strtemp[:idx]
                    store_info['xcoord'] = strtemp[idx+8:]

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
