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
#import json
from lxml import html

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('emart_everyday_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'이마트에브리데이|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 15:     # 2016년12월 기준 11 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.emarteveryday.co.kr'
    api = '/branch/branchList.jsp'
    data = {
        'region': '',
        'searchWord': ''
    }
    data['currentPage'] = intPageNo

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
    tree = html.fromstring(response)

    tableSelector = '//div[@id="content"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (len(infoList) < 5): continue    # 5개 필드 있음

        strSubName = infoList[1].xpath('.//a')[0].text.lstrip().rstrip()
        if not strSubName.endswith('점'): strSubName += '점'
        storeInfo['subname'] = strSubName.replace(' ', '/')

        storeInfo['newaddr'] = ''
        strtemp = infoList[2].xpath('.//a')[0].text
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            storeInfo['newaddr'] = strtemp

        storeInfo['pn'] = infoList[4].text.replace(' ', '')

        # 상세정보 페이지에 영업시간, 좌표정보 등 있음 (필요할 때 추출할 것!!)

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
