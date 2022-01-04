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

    outfile = codecs.open('sorrento_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@쏘렌토\n")

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

        if page == 99: break
        elif len(storeList) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.sorrento.co.kr'
    api = '/bbs/board.php'
    data = {
        'bo_table': 'store',
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
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)    # for debugging
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)


    entitySelector = '//div[@class="basic_tbl"]//ul'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        infoList = entityList[i].xpath('.//li')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 3): continue  # 최소 4개 필드 있어야 함

        storeInfo = {}
        storeInfo['name'] = '쏘렌토'
        subname = "".join(infoList[0].itertext()).strip('\r\t\n')
        if subname.endswith('피자쏘렌토'):
            subname = subname[:-5].rstrip()
            storeInfo['name'] = '피자쏘렌토'

        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')
        if storeInfo['subname'].endswith('점') == False:
            storeInfo['subname'] += '점'

        storeInfo['newaddr'] = ''
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        storeInfo['pn'] = '';
        strtemp = "".join(infoList[1].itertext()).strip('\r\t\n')
        if strtemp != None:
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')
            if storeInfo['pn'] == '--': storeInfo['pn'] = ''

        # 상세 정보 란에 영업시간 정보 있음 (필요할 때 추출할 것!)

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
