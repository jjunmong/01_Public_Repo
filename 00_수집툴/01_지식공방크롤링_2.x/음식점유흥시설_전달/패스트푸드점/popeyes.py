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
import json
from lxml import html

sido_list2 = {      # 테스트용 시도 목록
    '부산': '051'
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

    outfile = codecs.open('popeyes_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|XCOORD|YCOORD@@파파이스치킨\n")

    for sido_name in sido_list:

        storeList = getStores(sido_name)
        if storeList == None: break;
        elif len(storeList) == 0: break

        for store in storeList:
            strtemp = store['addr']
            if strtemp.find('없습니다') != -1: continue     # '검색된 매장이 없습니다'인 경우...

            outfile.write(u'파파이스치킨|')
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['tel'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['Naddr'])
            outfile.write(u'%s|' % store['mapy'])     # x, y 거꾸로 입력되어 있음
            outfile.write(u'%s\n' % store['mapx'])

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(strSidoName):
    url = 'http://www.popeyes.co.kr'
    api = '/store/exec_getFindCustomer.asp'
    data = {
        'gugun': '',
        'isDelivery': '',
    }
    data['sido'] = strSidoName

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
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)        # for debugging

    receivedData = json.loads(response)  # json 포맷으로 결과값 반환

    storeList = receivedData
    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
