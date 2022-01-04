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

    outfile = codecs.open('cafedroptop_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|FEAT@@드롭탑\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'카페드롭탑|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 31:       # 2016년 12월 기준 22 페이지까지 있음
            break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://cafedroptop.com'
    api = '/n/kr/src/store.php'
    data = {
        'c': '030100',
        's': 'store/store'
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

    tableSelector = '//table[@class="bbs_table_type1"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody//tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        if i == 0: continue  # 첫번째 엔티티에는 내용 없음

        storeInfo = {}

        infoList = entityList[i].xpath('.//td')
        if (infoList == None): continue;    # for safety
        elif (len(infoList) < 5): continue  # 5개 필드 있음

        storeInfo['subname'] = ''
        strtemp = "".join(infoList[0].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['subname'] = strtemp.rstrip().lstrip().replace(' ', '/')

        storeInfo['feat'] = ''
        strtemp = "".join(infoList[1].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['feat'] = strtemp.rstrip().lstrip()

        storeInfo['addr'] = ''
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['addr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = "".join(infoList[4].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip().replace(')', '-')

        featList = infoList[3].xpath('.//img/@alt')
        for j in range(len(featList)):
            if storeInfo['feat'] != '': storeInfo['feat'] += ';'
            storeInfo['feat'] += featList[j]

        # 상세정보 페이지에는 별다른 내용이 없음 (영업시간 정보 있음)

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
