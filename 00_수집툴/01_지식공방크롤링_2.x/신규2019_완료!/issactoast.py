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

    outfile = codecs.open('issactoast_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TEL|NEWADDR|FEAT\n")

    for sido_name in sido_list:

        page = 1
        while True:
            storeList = getStores('', page)
            if storeList == None: break;

            for store in storeList:
                outfile.write(u'이삭토스트|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['feat'])

            page += 1

            if page == 149: break
            elif len(storeList) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        break   # 2017년12월에 사이트 개편되어 sido_name 지정하지 않고 전국 지점 목록을 읽을 수 있음

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'http://www.isaac-toast.co.kr'
    api = '/bbs/board.php'
    data = {
        'bo_table': 'branches',
        'sfl': 'wr_subject',

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
        print('Error calling the API')
        return None

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@class="tbl_head01 tbl_wrap"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 최소 4개 필드 있어야 함

        subname = "".join(infoList[1].itertext()).strip('\r\t\n')
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['newaddr'] = ''
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None:
            idx = strtemp.find(']')
            if idx != -1: strtemp = strtemp[idx+1:].lstrip()
            storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = "".join(infoList[3].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-')

        storeInfo['feat'] = ''
        #strtemp = "".join(infoList[3].itertext()).strip('\r\t\n')
        #if strtemp != None:
        #    strtemp = strtemp.lstrip().rstrip()
        #    if strtemp == '○': storeInfo['feat'] = '단체주문가능'

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
