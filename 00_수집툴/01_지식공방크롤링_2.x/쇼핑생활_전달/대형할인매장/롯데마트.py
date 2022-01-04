# -*- coding: utf-8 -*-

'''
Created on 13 Dec 2016

@author: jskyun
'''

import sys
import time
import random
import codecs
import urllib
#import json
from lxml import html

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('lottemart_toysrus_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|OFFDATE|SUBSTORE@@롯데마트\n")

    # 롯데마트
    page = 1
    while True:
        storeList = getStores('BC0701', page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'롯데마트|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['offdate'])
            outfile.write(u'%s\n' % store['substore'])

        page += 1

        if page == 31:     # 2016년12월 기준 24 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    # VIC마켓
    page = 1
    while True:
        storeList = getStores('BC0704', page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'VIC마켓|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['offdate'])
            outfile.write(u'%s\n' % store['substore'])

        page += 1

        if page == 5:     # 2016년12월 기준 1 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    # 토이저러스
    page = 1
    while True:
        storeList = getStores('BC0702', page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'토이저러스|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['offdate'])
            outfile.write(u'\n')

        page += 1

        if page == 11:     # 2016년12월 기준 7 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    # 롯데문화센터
    page = 1
    while True:
        storeList = getStores('BC0705', page)
        if storeList == None: break
        elif len(storeList) == 0: break

        for store in storeList:
            outfile.write(u'롯데문화센터|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['offdate'])
            outfile.write(u'\n')

        page += 1

        if page == 31:     # 2016년12월 기준 11 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(strBrandCode, intPageNo):
    url = 'http://company.lottemart.com'
    api = '/bc/branchSearch/branchSearch.do'
    data = {
        'schStrCd': '',
        'schRegnCd': '',
        'schStrNm': ''
    }
    data['currentPageNo'] = intPageNo
    data['schBrnchTypeCd'] = strBrandCode

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

    tableSelector = '//ul[@class="office_list"]'
    dataTableList = tree.xpath(tableSelector)
    if len(dataTableList) < 1: return None

    dataTable = dataTableList[0]    # 첫번째 테이블은 매장 형태 소개

    nameSelector = './/div[@class="article1"]'
    nameList = dataTable.xpath(nameSelector)

    infoSelector = './/div[@class="article2"]'
    infoList = dataTable.xpath(infoSelector)

    # article3에 어마어마하게 많은 정보 있음 (마트 내 점포 정보 모두 등등)
    featSelector = './/div[@class="article3"]'
    featList = dataTable.xpath(featSelector)

    storeList = []

    for i in range(len(nameList)):
        storeInfo = {}

        strSubName = nameList[i].xpath('.//h3')[0].text
        storeInfo['subname'] = strSubName.replace(' ', '/')

        additionalInfo = infoList[i].xpath('.//p')[0]
        strPhoneNum = additionalInfo.text
        if strPhoneNum.startswith("T."): strPhoneNum = strPhoneNum[2:].lstrip()
        storeInfo['pn'] = strPhoneNum

        storeInfo['ot'] = ''
        storeInfo['offdate'] = ''
        strDateTimeInfo = "".join(additionalInfo.itertext()).strip('\r\t\n').rstrip()
        idx = strDateTimeInfo.find('휴점일 :')
        if idx != -1:
            storeInfo['offdate'] = strDateTimeInfo[idx+5:].lstrip()
            strDateTimeInfo = strDateTimeInfo[0:idx-1].rstrip()
        idx = strDateTimeInfo.find('운영시간 :')
        if idx != -1:
            storeInfo['ot'] = strDateTimeInfo[idx+6:].lstrip()

        offDateInfo = infoList[i].xpath('.//ul')[0]     # 휴점일 정보 위에서 추출되지 않아 다른 방법으로 추출
        strOffDate = "".join(offDateInfo.itertext()).strip('\r\t\n').rstrip()
        idx = strOffDate.find('휴점일 :')
        if idx != -1:
            storeInfo['offdate'] = strOffDate[idx+5:].lstrip()

        addrInfoList = infoList[i].xpath('.//li')
        strNewAddr = "".join(addrInfoList[0].itertext())
        if strNewAddr.startswith("신"): strNewAddr = strNewAddr[1:].lstrip()
        storeInfo['newaddr'] = strNewAddr
        strOldAddr = "".join(addrInfoList[1].itertext())
        if strOldAddr.startswith("구"): strOldAddr = strOldAddr[1:].lstrip()
        storeInfo['addr'] = strOldAddr

        storeInfo['substore'] = ''
        substoreInfoList = featList[i].xpath('.//li//span/span')
        for j in range(len(substoreInfoList)):
            substoreInfoItem = "".join(substoreInfoList[j].itertext()).strip('\r\t\n').replace(' ', '')
            substoreInfoItem = substoreInfoItem.replace('\r', '')
            substoreInfoItem = substoreInfoItem.replace('\t', '')
            substoreInfoItem = substoreInfoItem.replace('\n', '')
            if storeInfo['substore'] != '': storeInfo['substore'] += ';'
            storeInfo['substore'] += substoreInfoItem

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
