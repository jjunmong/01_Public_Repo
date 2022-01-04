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

    outfile = codecs.open('alpha_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FAXNUM\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'알파문구|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['fn'])

        page += 1

        if page == 51:     # 2016년12월 기준 36 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.alpha.co.kr'
    api = '/customer/chain/chainSearchList.do'
    data = {
        'searchWord': ''
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
    tree = html.fromstring(response)

    tableSelector = '//table[@class="table-col table-b bbs-list"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (len(infoList) < 6): continue    # 6개 필드 있음

        strSubName = infoList[1].text
        storeInfo['subname'] = strSubName.replace(' ', '/')

        storeInfo['newaddr'] = infoList[2].text
        storeInfo['pn'] = infoList[3].text
        storeInfo['fn'] = infoList[4].text

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
