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

    outfile = codecs.open('pascucci_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|FEAT@@파스쿠찌\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'파스쿠찌|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 101:
            break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.caffe-pascucci.co.kr'
    api = '/store/storeList.asp'
    data = {
        #'sido': ''
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

    tableSelector = '//table[@class="table storeTable"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        strtemp = entityList[i].xpath('.//td[@class="storeName"]/strong')[0].text
        storeInfo['subname'] = strtemp.replace(' ', '/')
        storeInfo['newaddr'] = entityList[i].xpath('.//td[@class="subject"]//p[@class="addr"]')[0].text
        storeInfo['ot'] = entityList[i].xpath('.//td[@class="subject"]//p[@class="openInfo"]')[0].text
        strtemp = entityList[i].xpath('.//span[@class="tel"]')[0].text
        storeInfo['pn'] = strtemp.replace('.', '-')

        featList = entityList[i].xpath('.//td[@class="additionalInfo"]//img/@alt')

        storeInfo['feat'] = ''
        for j in range(len(featList)):
            if(j != 0): storeInfo['feat'] += ';'
            storeInfo['feat'] += featList[j]

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
