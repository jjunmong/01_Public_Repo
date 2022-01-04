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

    outfile = codecs.open('momstouch_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@맘스터치\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'맘스터치|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 201:     # 2016년12월 기준 ?? 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.momstouch.co.kr'
    api = '/sub/store/store_01_list.html'
    data = {
        'area': '',
        'ss': ''
    }
    data['pg'] = intPageNo
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

    tableSelector = '//table[@class="store_List"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        if i == 0: continue     # 첫번째 엔티티에는 내용 없음

        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 5개 필드 있음

        strSubName = "".join(infoList[1].itertext()).strip('\r\t\n')
        storeInfo['subname'] = strSubName.rstrip().lstrip().replace(' ', '/')

        storeInfo['newaddr'] = '';
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = infoList[3].text
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip()

        # infoList[4]에 상세정보 페이지 열기 위한 store id 있으나 상세정보 페이지에 별 내용 없음

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
