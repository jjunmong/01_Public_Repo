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

    outfile = codecs.open('tudari_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR@@투다리\n")

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
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 101:     # 2016년12월 기준 84 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://tudari.co.kr'
    api = '/매장찾기/page/'
#    data = {
#        #'store': ''
#    }
#    data['page'] = intPageNo

#    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + str(intPageNo)
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)    # for debugging
    tree = html.fromstring(response)

    tableSelector = '//div[@class="map_list_wrap"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (len(infoList) < 5): continue

        strName = infoList[1].xpath('.//a')[0].text
        storeInfo['name'] = strName
        strSubName = infoList[2].xpath('.//a')[0].text
        storeInfo['subname'] = strSubName

        storeInfo['addr'] = ''
        storeInfo['newaddr'] = ''
        strAddrInfo = "".join(infoList[3].itertext()).strip('\r\t\n')

        idx = strAddrInfo.find('/')
        if idx != -1:
            storeInfo['addr'] = strAddrInfo[0:idx-1].rstrip()
            storeInfo['newaddr'] = strAddrInfo[idx+1:].lstrip()
        else:
            storeInfo['addr'] = strAddrInfo.rstrip()

        # 잘못 태그가 부여된 경우가 많아서 아래 코드는 사용하지 않음
        #addrInfoList = infoList[3].xpath('.//span[@class="address"]')
        #if len(addrInfoList) >= 1: storeInfo['addr'] = addrInfoList[0].text
        #if len(addrInfoList) >= 2:
        #    strNewAddr = addrInfoList[1].text.lstrip()
        #    if strNewAddr.startswith("/"): strNewAddr = strNewAddr[1:]
        #    strNewAddr = strNewAddr.lstrip()
        #    storeInfo['newaddr'] = strNewAddr

        storeInfo['pn'] = infoList[4].text

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
