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

    outfile = codecs.open('vips_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|FEAT@@VIPS\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 11:     # 2016년12월 기준 9 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.ivips.co.kr:7002'
    api = '/store/storeStoreInfoQ.asp'
    data = {
        #'option1': '',
        #'option2': ''
    }
    data['pageseq'] = intPageNo

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

    tableSelector = '//table[@class="tbl-list02"]'
    dataTable = tree.xpath(tableSelector)[1]        # 첫번째 테이블은 매장 형태 소개

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (len(infoList) < 5): continue    # 5개 필드 있음

        strSubName = infoList[0].xpath('.//a')[0].text
        storeInfo['subname'] = strSubName.replace(' ', '/')

        storeInfo['pn'] = infoList[1].text

        storeInfo['addr'] = ''
        storeInfo['newaddr'] = ''
        #strAddrInfo = infoList[2].xpath('.//a')[0].text.strip('\r\t\n').lstrip()
        strAddrInfo = "".join(infoList[2].xpath('.//a')[0].itertext()).strip('\r\t\n').lstrip()
        if strAddrInfo.startswith("도로명주소:"):
            strAddrInfo = strAddrInfo[6:].lstrip()
        idx = strAddrInfo.find('지번주소:')
        if idx != -1:
            storeInfo['newaddr'] = strAddrInfo[0:idx-1].rstrip()
            storeInfo['addr'] = strAddrInfo[idx+5:].lstrip()
        else: storeInfo['newaddr'] = strAddrInfo

        name_list = infoList[3].xpath('.//span')
        if len(name_list) > 0:
            strName = name_list[0].text
            storeInfo['name'] = strName.replace(' ', '/')
        else:   # 이름 필드에 정보가 없는 경우도 있음
            storeInfo['name'] = '빕스/월드푸드마켓'

        storeInfo['feat'] = ''
        featList = infoList[4].xpath('.//img/@alt')
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
