# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: sheayun
'''

import sys
import codecs
import time
import random
import urllib
#import json
from lxml import html

area = {
    '01': 'test1',
}

area2 = {
    '01': 'seoul',
    '02': 'kwangju',
    '03': 'daegu',
    '04': 'daejeon',
    '05': 'busan',
    '06': 'ulsan',
    '07': 'incheon',
    '08': 'gyenggi',
    '09': 'gangwon',
    '10': 'kyungnam',
    '11': 'kyungbuk',
    '12': 'jeonnam',
    '13': 'jeonbuk',
    '14': 'chungnam',
    '15': 'chungbuk',
    '16': 'jeju',
    '17': 'sejong',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('lotteria_utf8_pp_sc.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ORG_SUBNAME|FEAT@@롯데리아\n")

    page=1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u"롯데리아|")
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 2001:
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(intPageNo):

    url = 'http://www.lotteria.com'
    api = '/Shop/Shop_Ajax.asp'

    data = {
        'PageSize': 10,
        'BlockSize': 10,
        'SearchArea1': '',
        'SearchArea2': '',
        'SearchType': 'TEXT',
        'SearchIsFreshChicken': 0,
        'SearchIs24H': 0,
        'SearchIsDT': 0,
        'SearchIsEvent': 0,
        'SearchIsGroupOrder': 0,
        'SearchIsHomeService': 0,
        'SearchIsWifi': 0,
        'SearchText': ''
    }
    data['Page'] = intPageNo

    params = urllib.urlencode(data)
    print(params)

    try:
        result = urllib.urlopen(url + api, params)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)  # for debugging
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    #tree = html.fromstring(response)

    tableSelector = '//table[@class="list"]'
    dataTable = tree.xpath(tableSelector)[0]

    nameSelector = '//td[@class="first num"]/a'
    names = dataTable.xpath(nameSelector)
    telSelector = '//td[@class="num"]'
    tels = dataTable.xpath(telSelector)
    infoSelector = '//td[@class="type-list"]'
    infoList = dataTable.xpath(infoSelector)

    storeList = []

    for i in range(len(names)):
        storeInfo = {}

        storeInfo['orgname'] = names[i].text or ''
        storeInfo['name'] = storeInfo['orgname']
        if not storeInfo['name'].endswith('점'): storeInfo['name'] += '점'
        storeInfo['pn'] = tels[i].text or ''

        features = infoList[i].xpath('.//img/@alt')

        idx = 0
        storeInfo['feat'] = ''
        for feat_item in features:
            if(idx != 0):
                storeInfo['feat'] += ';'

            storeInfo['feat'] += feat_item
            idx += 1

        storeList += [storeInfo]

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
