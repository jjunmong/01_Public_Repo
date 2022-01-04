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

brand_list = {
    u'신선설농탕': 1
}
brand_list2 = {
    u'신선설농탕': 1,
    u'시화담': 2,
    u'우소보소': 3,
    u'수련': 4,
    u'이노데코': 5
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('sinsun_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|OT|PARKING|SEAT@@신선설농탕\n")

    for brandname in brand_list:

        page = 1
        while True:
            storeList = getStores(brandname, brand_list[brandname], page)
            if len(storeList) == 0:
                break

            for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s|' % store['park'])
                outfile.write(u'%s\n' % store['seat'])

            page += 1

            if page == 10:     # 2016년 12월 기준 7 페이지까지 있음
                break

    outfile.close()

def getStores(brandname, brandNo, intPageNo):
    url = 'http://www.kood.co.kr'
    api = '/koodci/store/store_list.php'
    data = {
        'vSIDO': '',
        'vGUGUN': '',
        'frSEARCH': ''
    }
    data['vBrand'] = ''
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    #print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)  # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)

    storeList = []

    # 반환값에 오류가 있어 수정함
    idx = response.find('<body>')
    if idx == -1: return storeList
    response = response[idx:]
    response = '<?xml version="1.0" encoding="utf-8"?><html><head></head> ' + response
    # print(response)

    tree = html.fromstring(response)

    tableSelector = '//div[@class="brand_store_list"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/div[@class="area_02"]'
    entityList = dataTable.xpath(entitySelector)

    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//p')

        if infoList == None: continue;      # for safety
        elif len(infoList) < 5: continue    # 2개 필드 있음

        name = '신선설농탕';    subname = ''
        strtemp = entityList[i].xpath('.//h5/a')[0].text

        if strtemp == None: continue
        idx = strtemp.find(']')
        if idx != -1:
            subname = strtemp[idx+1:].lstrip().rstrip().replace(' ','/')
            strtemp = strtemp[:idx].lstrip().rstrip()
            if strtemp.startswith('['):
                name = strtemp[1:].lstrip()

        if subname == '본사': continue
        elif subname == '레스토랑': subname = ''

        storeInfo['name'] = name.replace('·', '').replace(' ', '')      # '시·화·담'은 '시화담'으로...
        storeInfo['subname'] = subname.replace(' ', '/')


        storeInfo['addr'] = ''
        strtemp = "".join(infoList[0].itertext())
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            storeInfo['addr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = "".join(infoList[1].itertext())
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            storeInfo['pn'] = strtemp.rstrip().lstrip()

        storeInfo['ot'] = ''
        strtemp = "".join(infoList[2].itertext())
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('영업시간'): strtemp = strtemp[4:].lstrip()
            if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
            strtemp = strtemp.replace(' ', '').replace('24시간영업', '24시간')
            storeInfo['ot'] = strtemp.rstrip().lstrip()

        storeInfo['park'] = ''
        strtemp = "".join(infoList[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '')
            strtemp = strtemp.replace('주차여부', '').replace(':', '').replace('이상', '').replace('가능', '').lstrip().rstrip()
            if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
            storeInfo['park'] = strtemp.rstrip().lstrip()

        storeInfo['seat'] = ''
        strtemp = "".join(infoList[4].itertext())
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('좌석수'): strtemp = strtemp[3:].lstrip()
            if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
            storeInfo['seat'] = strtemp.rstrip().lstrip()

        storeList += [storeInfo]

    time.sleep(random.uniform(0.3, 0.9))
    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
