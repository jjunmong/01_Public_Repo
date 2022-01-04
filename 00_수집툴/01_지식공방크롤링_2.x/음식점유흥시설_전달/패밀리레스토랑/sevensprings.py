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

    outfile = codecs.open('sevensprings_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@세븐스프링스\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 2: break     # 한번 호출로 전국 점포정보 얻을 수 있음
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v3.0 (2018/9)
def getStores(intPageNo):
    # 'https://www.sevensprings.co.kr/Store/Store'
    url = 'https://www.sevensprings.co.kr'
    api = '/Store/Store'
    data = {}
    params = urllib.urlencode(data)
    # print(params)

    try:
        #result = urllib.urlopen(url + api, params)
        #urls = url + api + '?' + params
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//table[@class="center"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 5개 필드 있어야 함

        store_info = {}

        store_info['name'] = '세븐스프링스'
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('['):     # '[강원도]  삼척점'에서 '[강원도]' 제거
                idx = strtemp.find(']')
                if idx != -1:
                    strtemp = strtemp[idx+1:].lstrip()

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        # 상세정보 페이지에 메뉴 정보, 요금 정보 등 있음

        store_list += [store_info]

    return store_list


# v1.0
'''
def getStores(intPageNo):
    url = 'http://www.sevensprings.co.kr'
    api = '/store/store_list.asp'
    data = {
        'Area': '',
    }
    data['p'] = intPageNo
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
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)


    entitySelector = '//table[@class="tableList store"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 최소 4개 필드 있어야 함

        storeInfo = {}
        storeInfo['name'] = '세븐스프링스'
        subname = "".join(infoList[0].itertext()).strip('\r\t\n')
        idx = subname.find('(카페')
        if idx != -1:
            storeInfo['name'] = '카페세븐스프링스'
            subname = subname[:idx].rstrip()
            if subname.startswith('카페'):
                subname = subname[2:].lstrip()

        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['newaddr'] = ''
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        storeInfo['pn'] = '';
        strtemp = "".join(infoList[3].itertext()).strip('\r\t\n')
        if strtemp != None:
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')
            if storeInfo['pn'] == '--': storeInfo['pn'] = ''

        # 상세 정보 페이지에 영업시간 정보 등 속성 정보들 있음 (필요할 때 추출할 것!)

        storeList += [storeInfo]

    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
