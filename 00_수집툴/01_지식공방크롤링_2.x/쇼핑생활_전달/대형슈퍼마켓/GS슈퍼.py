# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import random
import codecs
import urllib
import urllib2
import json
from lxml import html

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('gssuper_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write("GS수퍼마켓|")
            strSubName = store['shopName']
            outfile.write(u'%s|' % strSubName)
            strPhoneNum = ''
            if store['phone'] != None:
                strPhoneNum = store['phone'].replace(')', '-')
            outfile.write(u'%s|' % strPhoneNum)
            outfile.write(u'%s|' % store['address'])
            strOperationHourInfo = ''
            if store['timeSTH'] != None:
                strOperationHourInfo += store['timeSTH']
                strOperationHourInfo += ':'
                strOperationHourInfo += store['timeSTM']
                strOperationHourInfo += '~'
                strOperationHourInfo += store['timeEDH']
                strOperationHourInfo += ':'
                strOperationHourInfo += store['timeEDM']
            outfile.write(u'%s|' % strOperationHourInfo)
            strOffDateInfo = ''
            strtemp = store['closedDate1']
            if strtemp != '': strOffDateInfo += strtemp
            strtemp = store['closedDate2']
            if strtemp != '':
                if strOffDateInfo != '': strOffDateInfo += ';'
                strOffDateInfo += strtemp
            strtemp = store['closedDate3']
            if strtemp != '':
                if strOffDateInfo != '': strOffDateInfo += ';'
                strOffDateInfo += strtemp
            strtemp = store['closedDate4']
            if strtemp != '':
                if strOffDateInfo != '': strOffDateInfo += ';'
                strOffDateInfo += strtemp
            outfile.write(u'%s\n' % strOffDateInfo)

            # 점포유형, 주차장 정보 등도 있다. (나중에 필요할 때 추가로 추출할 것!!!)

        page += 1

        if page == 71:     # 2016년12월 기준 58 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://gssuper.gsretail.com'
    api = '/gssuper/ko/market-info/find-storelist'
    data = {
        'listCnt': '5',
        'searchShopName': '',
        'pagingCnt': '',
        'totlPageNum': '',
        'pagingNowIdx': '',
        'searchShopName': '',
        'searchSido': '',
        'searchGugun': '',
        'searchType': '',
        'stationFlag': '',
        'pageSize': 5
    }
    data['pageNum'] = intPageNo

    params = urllib.urlencode(data)
    print(params)       # for debugging
    urls = url + api + '?' + params
    print(urls)         # for debugging

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #'Accept-Charset': 'utf-8',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-kr,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    req = urllib2.Request(urls, headers=hdr)

    try:
        result = urllib2.urlopen(req)
        # result = urllib.urlopen(url + api, params)
        #result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #result_encoding = result.headers.getparam('charset')
    #response = result.read().decode(result_encoding)

    #print(response)
    #tree = html.fromstring(response)
    receivedData = json.loads(response)     # json 포맷으로 결과값 반환

    if receivedData.get('results'): storeList = receivedData['results']
    else: storeList = []

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
