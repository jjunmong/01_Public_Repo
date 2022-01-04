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

    outfile = codecs.open('kyobobooks_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|OFFDAY@@교보문고\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'교보문고|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['offday'])

        page += 1
        if page == 2: break     # 한 페이지에 모든 점포정보 다 있음

    outfile.close()

# v2.0
def getStores(intPageNo):
    url = 'http://www.kyobobook.co.kr'
    api = '/storen/info/StorePosition.jsp'
    data = {
        'SITE': '',
    }

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
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    suburl_info = tree.xpath('//div[@class="store_list wide"]//ul//li//a')

    store_list = []
    for i in range(len(suburl_info)):
        suburl = suburl_info[i].xpath('./@href')[0]
        strtemp = "".join(suburl_info[i].itertext())
        if strtemp == None: continue

        store_info = {}
        store_info['name'] = '교보문고'
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        store_info['subname'] = strtemp.rstrip().lstrip().replace(' ', '/')

        try:
            print(suburl)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        # print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="box_content"]//span')

        store_info['pn'] = ''
        store_info['newaddr'] = ''
        store_info['ot'] = ''
        store_info['offday'] = ''

        for j in range(len(subinfo_list)):
            strtemp = "".join(subinfo_list[j].itertext())
            if strtemp == None: continue
            idx = strtemp.find(':')
            if idx == -1: continue

            key = strtemp[:idx].lstrip().rstrip()
            value = strtemp[idx+1:].lstrip().rstrip()

            if key == '전화번호': store_info['pn'] = value.replace(' ', '').replace('.', '-').replace(')', '-')
            elif key == '영업시간': store_info['ot'] = value
            elif key == '정기휴일': store_info['offday'] = value
            elif key == '주소': store_info['newaddr'] = value

        store_list += [store_info]

    return store_list


# v1.0
'''
def getStores(intPageNo):
    url = 'http://www.kyobobook.co.kr'
    api = '/storen/info/StorePosition.jsp'
    data = {
        'SITE': '',
    }

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
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entityList = tree.xpath('//div[@class="branch_loc_box"]')

    storeList = []
    for i in range(len(entityList)):
        name_list = entityList[i].xpath('.//h2[@class="bul_green"]')
        info_list = entityList[i].xpath('.//div[@class="info"]/ul//li')

        if len(name_list) < 1: continue;  # for safety
        elif len(info_list) < 2: continue  # 최소 2개 필드 있어야

        storeInfo = {}
        subname = "".join(name_list[0].itertext()).strip('\r\t\n')
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['addr'] = '';      storeInfo['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext()).strip('\r\t\n')
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('(구)')
            if idx != -1:
                storeInfo['newaddr'] = strtemp[:idx].rstrip()
                storeInfo['addr'] = strtemp[idx+3:].lstrip()
            else: storeInfo['newaddr'] = strtemp

        storeInfo['pn'] = '';
        strtemp = "".join(info_list[1].itertext()).strip('\r\t\n')
        if strtemp != None:
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')
            if storeInfo['pn'] == '--': storeInfo['pn'] = ''

        storeList += [storeInfo]

    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
