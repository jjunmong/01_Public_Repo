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

    outfile = codecs.open('catholic_church_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|AREA|SUBNAME|TELNUM|NEWADDR|FATHER|SINCE@@성당\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['area'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['father'])
            outfile.write(u'%s\n' % store['since'])

        page += 1

        if page == 299: break   # 2018년5월 1740곳 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://directory.cbck.or.kr/OnlineAddress/SearchList.aspx'
    url = 'http://directory.cbck.or.kr'
    api = '/OnlineAddress/SearchList.aspx'
    data = {
        'cgubn': 'g',
        'gyogu': 'all',
        'gubn': '4',
        'tbxSearch': '',
        #'scnt': '1740',
        'scnt': '',
        'paged': '10',
        'sort': '0',
        'gubn2': 'all',
        'char': 'all',
    }
    data['start'] = (intPageNo-1)*10 + 1
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
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)     # 인코딩 정보가 반환값에 없어서...

    entity_list = tree.xpath('//div[@id="Category_SearchList"]//table')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 1: continue  # 최소 1개 필드 있어야 함

        name_list = info_list[0].xpath('.//a')
        if len(name_list) < 1: continue

        store_info = {}

        store_info['name'] = '천주교'
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if not strtemp.endswith('성당'): strtemp += '성당'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['since'] = ''
        store_info['area'] = ''
        store_info['father'] = ''
        store_info['newaddr'] = ''
        store_info['pn'] = ''

        for j in range(len(info_list)):
            strtemp = "".join(info_list[j].itertext())
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if strtemp.startswith('설립일'):
                strtemp = strtemp[3:].lstrip()
                if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                store_info['since'] = strtemp
            elif strtemp.startswith('[대'):
                idx = strtemp.find(']')
                if idx != -1: strtemp = strtemp[idx + 1:].lstrip()

                if strtemp[0] >= '0' and strtemp[0] <= '9':  # 우편번호 정보 제거
                    idx = strtemp.find(' ')
                    if idx != -1: strtemp = strtemp[idx + 1:].lstrip()

                store_info['newaddr'] = strtemp.replace(' - ', '-')

            elif strtemp.find('교구/'):
                idx = strtemp.find('/')
                store_info['area'] = strtemp[:idx].rstrip()
                strtemp = strtemp[idx+1:].lstrip()
                idx = strtemp.rfind('/')
                if idx != -1:
                    store_info['father'] = strtemp[:idx].rstrip()
                    strtemp = strtemp[idx + 1:].lstrip()
                    if strtemp.startswith('('): strtemp = strtemp[1:].lstrip()
                    store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')
                else:
                    store_info['father'] = strtemp

        # 상세정보 페이지도 있음 (필요할 때 추출할 것)

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
