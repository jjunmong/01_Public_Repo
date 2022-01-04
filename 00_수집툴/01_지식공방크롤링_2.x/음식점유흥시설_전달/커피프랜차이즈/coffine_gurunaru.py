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

    outfile = codecs.open('coffine_gurunaru_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|PN|NEWADDR|FEAT\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'커핀그루나루|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 999: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.coffine.co.kr'
    api = '/front/store/find_store_list.php'
    data = {

        'area1': '',
        'area2': '',
        'sv1': '',
        'sv2': '',
        'sv3': '',
        'sv4': '',
        'sk': '',
    }
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//table[@class="table_style1 mb35"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        subname = entityList[i].xpath('.//th')[0].text
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 4개 필드 있음

        storeInfo['newaddr'] = '';
        strtemp = "".join(infoList[0].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = '';
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip()

        storeInfo['feat'] = ''
        featList = infoList[1].xpath('.//img/@src')
        for j in range(len(featList)):
            if storeInfo['feat'] != '': storeInfo['feat'] += ';'

            feat_item = featList[j]
            if feat_item.endswith('ico1.png'): storeInfo['feat'] += '주차가능'
            elif feat_item.endswith('ico2.png'): storeInfo['feat'] += '비즈니스룸'
            elif feat_item.endswith('ico3.png'): storeInfo['feat'] += '충전가능'
            elif feat_item.endswith('ico4.png'): storeInfo['feat'] += '와이파이'
            elif feat_item.endswith('ico5.png'): storeInfo['feat'] += '발렛파킹'


        # 상세정보 페이지에 영업시간 정보 추가로 있음 (필요할 때 추출할 것)

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
