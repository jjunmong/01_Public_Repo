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

    outfile = codecs.open('ssangyong_motors_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'쌍용자동차|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 99: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.smotor.com'
    api = '/purchase/exhibition_center/ec_am_search.jsp'
    data = {
        'ec_addr_si': '',
        'ec_addr_gu': '',
        'am_addr_si': '',
        'am_addr_gu': '',
        'am_addr_cd': '',
        'cmd': '',
    }
    data['current_page'] = intPageNo
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
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@class="result"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        info_list = entityList[i].xpath('.//td')

        if len(info_list) < 4: continue  # 최소 필드 수 체크

        storeInfo = {}
        subname = "".join(info_list[1].itertext()).strip('\r\t\n').lstrip().rstrip()
        if not subname.endswith('지점'): subname += '지점'
        storeInfo['subname'] = subname.replace(' ', '/')

        storeInfo['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        storeInfo['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
