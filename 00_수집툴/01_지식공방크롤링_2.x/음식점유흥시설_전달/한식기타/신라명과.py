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

    outfile = codecs.open('shillabakery_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|OT|FEAT\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'신라명과|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 11:     # 2016년12월 기준 9 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.shillabakery.com'
    api = '/www/store/store.html'
    data = {
        'brand': 1      # 1 신라명과, 2 링바볼 (매장 1개만 있음)
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
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    tableSelector = '//table[@class="board-list mgtop10"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (len(infoList) < 7): continue    # 5개 필드 있음

        strSubName = infoList[1].xpath('.//a')[0].text.lstrip().rstrip()
        if not strSubName.endswith('점'): strSubName += '점'
        storeInfo['subname'] = strSubName.replace(' ', '/')

        storeInfo['addr'] = infoList[2].xpath('.//a')[0].text
        storeInfo['pn'] = infoList[3].xpath('.//a')[0].text
        storeInfo['ot'] = infoList[4].xpath('.//a')[0].text

        storeInfo['feat'] = ''
        featList = infoList[5].xpath('.//img/@src')
        if featList != None:
            for feat_item in featList:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'

                if feat_item.find("_t.gif") != -1: storeInfo['feat'] += 'SKT멤버쉽'
                elif feat_item.find("_o.gif") != -1: storeInfo['feat'] += 'KT멤버쉽'

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
