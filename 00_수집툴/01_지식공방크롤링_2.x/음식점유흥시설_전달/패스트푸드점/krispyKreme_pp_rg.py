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

    outfile = codecs.open('krispyKreme_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@크리스피크림\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;


        for store in storeList:
            outfile.write(u'크리스피크림|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['x'])
            outfile.write(u'%s\n' % store['y'])

        page += 1

        if page == 49: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.krispykreme.co.kr'
    api = '/store/store_search.asp'
    data = {
        'list_num': 10,
        'schWord': '',
        'schSido': '',
        'schGugun': '',
        'schService1': '',
        'schService2': '',
        'schService3': '',
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
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@class="tbl_wrap02 store_search_warp"]'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        name_list = entityList[i].xpath('.//p[@class="store_tit"]')

        if len(name_list) < 1: continue

        subname = name_list[0].text
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        infoList = entityList[i].xpath('.//tbody//tr//td')
        strtemp = infoList[0].text
        storeInfo['pn'] = strtemp

        storeInfo['ot'] = ''
        strtemp = infoList[1].text
        if strtemp != None:
            strtemp = strtemp.upper().replace('/', ';').replace('OPEN', '').replace('CLOSE', '').replace('.', '').replace(' ', '').lstrip().rstrip()
            storeInfo['ot'] = strtemp

        x_coord = entityList[i].xpath('.//input[@name="mapX"]/@value')[0].lstrip().rstrip()
        y_coord = entityList[i].xpath('.//input[@name="mapY"]/@value')[0].lstrip().rstrip()

        # x,y 좌표 거꾸로 들어가 있음 ㅠㅠ
        storeInfo['y'] = x_coord
        storeInfo['x'] = y_coord

        storeInfo['newaddr'] = ''

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
