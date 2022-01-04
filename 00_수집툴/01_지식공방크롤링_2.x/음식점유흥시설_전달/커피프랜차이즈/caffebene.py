# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: sheayun
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

    outfile = codecs.open('caffebene_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|FEAT@@카페베네\n")

    page = 1
    while True:
        storeList = getStores(page)

        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'카페베네|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 501:         # 2016년 12월 기준 135까지 있음
            break

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.caffebene.co.kr'
    api = '/Content/Gnb/Store/Map.aspx'
    data = {
        'code': 'T5M2I2',
        'SearchValue': '',
        'gugun': '',
        'StoreName': '',
        'room': 'N',
        'wifi': 'N',
        'all': 'N',
        'pc': 'N',
        'book': 'N',
        'store': 'N'
    }
    data['Page'] = intPageNo

    params = urllib.urlencode(data)
    #print(params)

    try:
        #result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)
        result = urllib.urlopen(urls)
        #result = urllib.urlopen('http://www.caffebene.co.kr/Content/Gnb/Store/Map.aspx?&SearchValue=&gugun=&StoreName=&room=N&wifi=N&all=N&pc=N&book=N&store=N&Page=9&code=T5M2I2')
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    tree = html.fromstring(response)

    tableSelector = '//div[@class="listWrap type05"]'
    dataTable = tree.xpath(tableSelector)[0]


    nameSelector = './/strong[@class="storeName"]'
    telSelector = './/span[@class="tel"]'
    addrSelector = './/address[@class="addr"]'
    opentimeSelector = './/span[@class="cell_inner"]'
    names = dataTable.xpath(nameSelector)
    tels = dataTable.xpath(telSelector)
    addrs = dataTable.xpath(addrSelector)
    opentimes = dataTable.xpath(opentimeSelector)

    featSelector = './/div[@class="cell_service"]'
    featInfoList = dataTable.xpath(featSelector)

    storeList = []

    for i in range(len(names)):
        storeInfo = {}

        # 초기에 짠 코드여서 로직 다소 어설픔
        # 상세정보 페이지에 좌석수, 주차여부 등의 정보 있음 (필요할 때 추가로 추출할 것!!!)

        storeInfo['feat'] = ''

        storeInfo['subname'] = names[i].text or ''
        if storeInfo['subname'].startswith('직영'):
            storeInfo['subname'] = storeInfo['subname'][2:].lstrip()
            storeInfo['feat'] += '직영매장'

        if storeInfo['subname'].endswith('(휴점)'):
            storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-4].rstrip()
            if storeInfo['feat'] != '': storeInfo['feat'] += ';'
            storeInfo['feat'] += '휴점'

        storeInfo['subname'] = storeInfo['subname'].replace(' ', '/')

        storeInfo['pn'] = tels[i].text or ''
        if storeInfo['pn'] != None:
            if storeInfo['pn'].startswith('T'): storeInfo['pn'] = storeInfo['pn'][1:].lstrip()
        storeInfo['newaddr'] = addrs[i].text or ''
        storeInfo['ot'] = opentimes[i].text or ''
        if storeInfo['ot'] != None:
            storeInfo['ot'] = storeInfo['ot'].replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

        feature_list = featInfoList[i].xpath('.//img')

        for j in range(len(feature_list)):
            feature = feature_list[j]
            feature_name = feature.xpath('./@alt')[0]
            feature_flag = feature.xpath('./@style')
            if feature_name.find('세미나실') != -1 and len(feature_flag) == 0:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '세미나실'
            if feature_name.find('WIFI') != -1 and len(feature_flag) == 0:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += 'WIFI'
            if feature_name.find('24시간') != -1 and len(feature_flag) == 0:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '24시간'
            if feature_name.find('북카페') != -1 and len(feature_flag) == 0:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '북카페'
            if feature_name.find('PC사용가능') != -1 and len(feature_flag) == 0:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += 'PC사용가능'
            if feature_name.find('베이글') != -1 and len(feature_flag) == 0:
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '베이글인매장'

        storeList += [storeInfo]

    delay_time = random.uniform(0.3, 1.1)
    time.sleep(delay_time)
    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
