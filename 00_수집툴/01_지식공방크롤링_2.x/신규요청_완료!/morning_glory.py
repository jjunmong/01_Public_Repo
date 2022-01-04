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

    outfile = codecs.open('morning_glory_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR@@모닝글로리\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'모닝글로리|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 999: break
        elif len(storeList) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://morning.mgstore.co.kr'
    api = '/_cafe24/locationshop/_LocalChain.asp'
    data = {
        'Loc': '',
        'locate_gu01': '',
        'locate_gu02': '',
        'locate_gu03': '',
        'txtSchWord': '',
        'c_block': 1,
    }
    data['cpage'] = intPageNo

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
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)    # for debugging
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//table[@class="bbsViewA mgt30"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        if i == 0: continue     # 첫번째 줄은 컬럼 정보 수록

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 6): continue  # 최소 6개 필드 있어야 함

        storeInfo = {}
        subname = "".join(infoList[1].itertext()).strip('\r\t\n')
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['addr'] = '';      storeInfo['newaddr'] = ''
        strtemp = "".join(infoList[5].itertext()).strip('\r\t\n')
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('(지번)')
            storeInfo['addr'] = strtemp[idx+4:].lstrip()
            strtemp = strtemp[:idx].rstrip()
            if strtemp.startswith('(도로)'): strtemp = strtemp[4:].lstrip()
            storeInfo['newaddr'] = strtemp

        storeInfo['pn'] = '';
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None:
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-').replace(' ', '')
            if storeInfo['pn'] == '--': storeInfo['pn'] = ''

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
