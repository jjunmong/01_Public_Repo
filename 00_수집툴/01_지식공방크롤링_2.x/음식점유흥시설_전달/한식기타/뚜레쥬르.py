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

    outfile = codecs.open('tlj_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|ID|XCOORD|YCOORD@@뚜레쥬르\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write("뚜레쥬르|")
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 301:     # 2016년12월 기준 139까지 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.tlj.co.kr:7008'
    api = '/store/search.asp'
    data = {
        #'Area': ''
    }
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    #print(params)

    try:
        #result = urllib.urlopen(url + api, params)

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

    tableSelector = '//div[@class="str_rst"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        strtemp = entityList[i].xpath('.//th/span/a')[0].text
        idx = strtemp.find("뚜레쥬르")
        if(idx != -1): strtemp = strtemp[idx+4:]
        strtemp = strtemp.lstrip().rstrip()
        if not strtemp.endswith('점'): strtemp += '점'
        storeInfo['subname'] = strtemp.replace(' ', '/')

        storeInfo['addr'] = ''
        storeInfo['newaddr'] = ''
        addrList = entityList[i].xpath('.//td//a/span')
        addrinfo_length = len(addrList)
        if(addrinfo_length > 0): storeInfo['newaddr'] = addrList[0].text.strip('\n\t\r')
        if(addrinfo_length > 1): storeInfo['addr'] = addrList[1].text.strip('\n\t\r')

        storeInfo['pn'] = entityList[i].xpath('.//p[@class="tel"]')[0].text

        storeInfo['id'] = entityList[i].xpath('./@id')[0]
        storeInfo['xcoord'] = entityList[i].xpath('./@data-lat')[0]
        storeInfo['ycoord'] = entityList[i].xpath('./@data-lng')[0]

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
