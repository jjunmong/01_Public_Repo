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

sido_list = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list2 = {
    '서울': '02',
    '광주': '062',
    '대구': '053',
    '대전': '042',
    '부산': '051',
    '울산': '052',
    '인천': '032',
    '경기': '031',
    '강원': '033',
    '경남': '055',
    '경북': '054',
    '전남': '061',
    '전북': '063',
    '충남': '041',
    '충북': '043',
    '제주': '064',
    '세종': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('ssangyong_motors_svc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR@@쌍용자동차정비사업소\n")

    outfile2 = codecs.open('ssangyong_motors_svc_plaza_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|ADDR@@쌍용자동차서비스프라자\n")

    outfile3 = codecs.open('ssangyong_motors_svc_other_utf8.txt', 'w', 'utf-8')
    outfile3.write("##NAME|SUBNAME|TELNUM|ADDR@@쌍용자동차지정전문공장\n")


    page = 1
    while True:
        storeList = getStores('/kr/service/network/org', '1', page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'쌍용자동차|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['addr'])

        page += 1

        if page == 99: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.4, 1.2))

    page = 1
    while True:
        storeList = getStores('/kr/service/network/center', '1', page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'쌍용자동차|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['addr'])

        page += 1

        if page == 99: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.4, 1.2))

    page = 1
    while True:
        storeList = getStores('/kr/service/network/fac', '1', page)
        if storeList == None: break;

        for store in storeList:
            outfile3.write(u'쌍용자동차지정공장|')
            outfile3.write(u'%s|' % store['subname'])
            outfile3.write(u'%s|' % store['pn'])
            outfile3.write(u'%s\n' % store['addr'])

        page += 1

        if page == 99:
            break
        elif len(storeList) < 10:
            break

        time.sleep(random.uniform(0.4, 1.2))

    page = 1
    while True:
        storeList = getStores('/kr/service/network/se_pl', '1', page)
        if storeList == None: break;

        for store in storeList:
            outfile2.write(u'쌍용자동차서비스프라자|')
            outfile2.write(u'%s|' % store['subname'])
            outfile2.write(u'%s|' % store['pn'])
            outfile2.write(u'%s\n' % store['addr'])

        page += 1

        if page == 99:
            break
        elif len(storeList) < 10:
            break

        time.sleep(random.uniform(0.4, 1.2))

    outfile.close()
    outfile2.close()
    outfile3.close()


def getStores(api_name, type_info, intPageNo):
    url = 'http://www.smotor.com'
    api = api_name
    params = '/index,' + str(type_info) + ',list,' + str(intPageNo) + '.html'
    if intPageNo == 1: params = '/index.html'
    #print(params)

    try:
        urls = url + api + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@id="boardListA"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        info_list = entityList[i].xpath('.//td')

        if len(info_list) < 5: continue  # 최소 필드 수 체크

        storeInfo = {}
        subname = "".join(info_list[1].itertext()).strip('\r\t\n').lstrip().rstrip().replace('(주)', '')
        if subname.startswith('쌍용자동차'): subname = subname[5:].lstrip()
        if subname.endswith('서비스프라자'): subname = subname[:-6].rstrip()
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['addr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            storeInfo['addr'] = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
