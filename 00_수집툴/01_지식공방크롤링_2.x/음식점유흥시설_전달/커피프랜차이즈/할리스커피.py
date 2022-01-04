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

    outfile = codecs.open('hollys_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@할리스커피\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write("할리스커피|")
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 71:     # 2018년6월 기준 56 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.hollys.co.kr'
    api = '/store/korea/korStore.do'
    data = {
        'sido': '',
        'gugun': '',
        'store': ''
    }
    data['pageNo'] = intPageNo

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

    tableSelector = '//div[@class="tableType01"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (len(infoList) < 6): continue

        strtemp = infoList[1].xpath('.//a')[0].text
        storeInfo['subname'] = strtemp.replace(' ', '/')
        strtemp = infoList[3].xpath('.//a')[0].text
        storeInfo['newaddr'] = strtemp
        storeInfo['pn'] = ''
        strtemp = infoList[5].text
        if strtemp != None:
            storeInfo['pn'] = strtemp.lstrip().rstrip().replace(' ', '').replace(')', '-')

        featList = infoList[4].xpath('.//img/@alt')

        storeInfo['feat'] = ''
        if featList != None:
            for feat_item in featList:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'

                storeInfo['feat'] += feat_item

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
