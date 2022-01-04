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

    outfile = codecs.open('caffetiamo_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR@@카페띠아모\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            if store['addr'].find('오픈 예정') != -1: continue

            outfile.write(u'카페띠아모|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['addr'])

        page += 1

        if page == 499: break
        elif len(storeList) < 20: break

        delay_time = random.uniform(0.3, 1.1)
        time.sleep(delay_time)

    outfile.close()

def getStores(intPageNo):
    # 'http://www.ti-amo.co.kr/storeGuide/storeSearch.asp?page=3'
    url = 'http://www.ti-amo.co.kr'
    api = '/storeGuide/storeSearch.asp'
    data = {
    }
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    # print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        urls = url + api + '?' + params
        print(urls)     # for debugging

        req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)

    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@class="group_storeList"]/div'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        subname = entityList[i].xpath('.//p')[0].text
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['addr'] = '';
        strtemp = entityList[i].xpath('.//dl[@class="area_storeAddress"]/dd')[0].text
        if strtemp != None: storeInfo['addr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = '';
        strtemp = entityList[i].xpath('.//dl[@class="area_storeTel"]/dd')[0].text
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip()

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
