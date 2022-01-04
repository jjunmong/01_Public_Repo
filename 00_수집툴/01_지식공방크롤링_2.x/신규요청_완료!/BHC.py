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

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('bhc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@BHC치킨\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 201:         # 2016년 12월 기준 135까지 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.bhc.co.kr'
    api = '/location/search_sub.asp'
    data = {
        'search_sido': '',
        'search_sido_text': '',
        'search_gugun': '',
        'search_text': '',
        'search_service': '',
        'search_type': ''
    }
    data['cPage'] = intPageNo
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
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    tableSelector = '//table[@class="register01"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody//tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 3): continue  # 3개 필드 있음

        storeInfo['name'] = 'BHC치킨';    storeInfo['feat'] = ''
        storetype_info = infoList[0].xpath('.//img/@src')[0]
        if storetype_info.find("BHC_Bear") != -1:
            storeInfo['name'] = 'BHC치킨앤비어'
            storeInfo['feat'] = '맥주판매'


        featList = infoList[1].xpath('.//p')
        if len(featList) < 2: continue

        strSubName = "".join(featList[0].itertext()).strip('\r\t\n')

        nameList = infoList[1].xpath('.//div')      # 이름이 이렇게 표기된 경우도 있음
        if len(nameList) == 1:
            strSubName = nameList[0].text.rstrip().lstrip()

        if strSubName.startswith('bhc'): strSubName = strSubName[3:].lstrip()
        elif strSubName.startswith('BHC'): strSubName = strSubName[3:].lstrip()

        storeInfo['subname'] = strSubName.rstrip().lstrip().replace(' ', '/')

        strOtherInfo = "".join(featList[1].itertext()).strip('\r\t\n')
        idx = strOtherInfo.find('전화번호')
        store_addr = strOtherInfo[:idx]
        store_pn = strOtherInfo[idx+4:]

        idx = store_addr.find(':')
        store_addr = store_addr[idx+1:]
        storeInfo['newaddr'] = store_addr.replace('\n', '').replace('\r', '').replace('\t', '').replace('.1층', ' 1층').replace('.2층', ' 2층').rstrip().lstrip()

        idx = store_pn.find(':')
        store_pn = store_pn[idx+1:]
        storeInfo['pn'] = store_pn.rstrip().lstrip().replace('\n', '').replace('\r', '').replace('\t', '')

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
