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

    outfile = codecs.open('tomntoms_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FLOOR|TYPE|FEAT@@탐앤탐스\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write("탐앤탐스|")
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['floor'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 149:     # 2016년12월 기준 445개 매장 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.tomntoms.com'
    api = '/store/storeList_frame.php'
    data = {
        'sidoCode': '',
        'sltGlobal': 'KR',
        'sltSIDO': '',
        'sltGUGUN': '',
        'hidGUGUN': '',
        'sName': ''
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

    tableSelector = '//div[@class="localList"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        storeInfo['type'] = ''
        temp_list = entityList[i].xpath('.//td[@class="type"]/img/@title')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            storeInfo['type'] = strtemp

        temp_list = entityList[i].xpath('.//th//dt/a')
        if len(temp_list) < 1: continue
        strtemp = temp_list[0].text
        storeInfo['subname'] = strtemp.replace(' ', '/')

        storeInfo['newaddr'] = '';        storeInfo['floor'] = ''
        temp_list = entityList[i].xpath('.//th//dd[@class="addr"]')
        if len(temp_list) < 1: continue
        strtemp = temp_list[0].text
        strtemp = strtemp.strip('\n\t\r').rstrip()
        strtemp = strtemp.replace('\t', ' ')   # '\t'문자가 strip을 해도 없어지지 않아서...
        idx = strtemp.rfind('[')
        if idx != -1:
            storeInfo['floor'] = strtemp[idx+1:].lstrip().rstrip()
            if storeInfo['floor'].endswith(']'): storeInfo['floor'] = storeInfo['floor'][:-1].rstrip()
            strtemp = strtemp[:idx].rstrip()
        storeInfo['newaddr'] = strtemp

        storeInfo['pn'] = ''
        temp_list = entityList[i].xpath('.//th//dd[@class="tel"]')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            idx = strtemp.find("T.")
            if idx != -1: strtemp = strtemp[idx+2:]
            storeInfo['pn'] = strtemp.lstrip()

        featList = entityList[i].xpath('.//td[@class="service"]//img/@src')

        storeInfo['feat'] = ''
        if featList != None:
            for feat_item in featList:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'

                if feat_item.find("_a.gif") != -1: storeInfo['feat'] += 'A클래스'
                elif feat_item.find("_b.gif") != -1: storeInfo['feat'] += 'B클래스'
                elif feat_item.find("_c.gif") != -1: storeInfo['feat'] += 'C클래스'
                elif feat_item.find("op.gif") != -1: storeInfo['feat'] += '24시간'
                elif feat_item.find("mt.gif") != -1: storeInfo['feat'] += '마이탐사용'
                elif feat_item.find("wf.gif") != -1: storeInfo['feat'] += '와이파이존'
                elif feat_item.find("bs.gif") != -1: storeInfo['feat'] += '비지니스룸'
                elif feat_item.find("te.gif") != -1: storeInfo['feat'] += '테라스'
                elif feat_item.find("pk.gif") != -1: storeInfo['feat'] += '주차가능'
                elif feat_item.find("bp.gif") != -1: storeInfo['feat'] += '발레파킹'
                elif feat_item.find("sm.gif") != -1: storeInfo['feat'] += '흡연실설치'
                elif feat_item.find("bcpay.gif") != -1: storeInfo['feat'] += 'BCPAY'

        # 가맹점, 직영점 구분도 있는데 추출하지 않았음
        # 상세보기 링크에 영업시간 정보 있음 (나중에 추가할 것)

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
