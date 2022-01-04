# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
import urllib2
import random
import json
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

    outfile = codecs.open('jjaktae_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@짝태&노가리\n")

    while True:
        storeList = getStores('')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'짝태&노가리|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        break     # 한 페이지에 모든 정보 다 있음

    outfile.close()

def getStores(type_info):
    url = 'http://jjaktae.kr'
    api = '/%EC%A7%80%EC%A0%90%EC%95%88%EB%82%B4/'
    data = {
     }
    params = urllib.urlencode(data)

    try:
        # result = urllib.urlopen(url + api, params)
        result = urllib.urlopen(url + api)
    except:
        print('Error calling the API');
        return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entityList = tree.xpath('//table[@class="wpgmza_table responsive"]//tbody//tr')

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 4개 필드 있어야 함

        subname = "".join(infoList[0].itertext()).strip('\r\t\n')
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/').replace('-', '/')

        storeInfo['newaddr'] = '';
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = '';
        strtemp = "".join(infoList[3].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-').replace(' ', '')

        storeList += [storeInfo]

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
