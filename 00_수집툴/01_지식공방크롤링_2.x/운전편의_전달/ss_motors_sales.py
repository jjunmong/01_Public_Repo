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

sido_list2 = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list = {
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

    outfile = codecs.open('ss_motors_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR\n")

    for sido_name in sido_list:

        storeList = getStores(sido_name)
        if storeList == None: continue
        elif len(storeList) == 0: continue

        for store in storeList:
            outfile.write(u'르노삼성자동차|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['newaddr'])

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(strSidoName):
    url = 'http://www.renaultsamsungm.com'
    api = '/2016/customer/search/getSalesList.jsp'
    data = {
        'gu': '',
        'search_type': 'addr'
    }
    data['zip_sido'] = strSidoName
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entityList = tree.xpath('//table[@class="bbsList"]//tbody//tr')

    storeList = []
    for i in range(len(entityList)):
        subname_list = entityList[i].xpath('.//th')
        info_list = entityList[i].xpath('.//td')

        if len(subname_list) < 1 or len(info_list) < 1: continue

        storeInfo = {}

        storeInfo['subname'] = '';      storeInfo['pn'] = ''
        subname = subname_list[0].text.lstrip().rstrip()
        storeInfo['subname'] = subname.replace(' ', '/')

        strtemp = "".join(subname_list[0].itertext()).strip('\r\t\n')
        idx = strtemp.find(subname)
        if idx != -1:
            storeInfo['pn'] = strtemp[idx+len(subname):].lstrip().rstrip().replace('.', '-').replace(')', '-')

        storeInfo['addr'] = '';      storeInfo['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext()).lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
        idx = strtemp.find('지번')
        if idx != -1:
            storeInfo['addr'] = strtemp[idx+2:].lstrip()
            strtemp = strtemp[:idx].rstrip()
        if strtemp.startswith('도로명'): strtemp = strtemp[3:].lstrip()
        storeInfo['newaddr'] = strtemp

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
