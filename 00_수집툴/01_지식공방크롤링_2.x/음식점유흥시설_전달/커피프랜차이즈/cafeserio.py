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

    outfile = codecs.open('cafeserio_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['addr'])

        page += 1

        if page == 99: break
        elif len(storeList) < 3: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.serio.co.kr'
    api = '/store/ourstore.html'
    data = {
        'table_code': '',
        'tblname': '',
        'gubun': '',
        'SearchId': '',
        'strSearch': '',
        'levels': '',
        'Sdate': '',
        'Edate': '',
        'cidx': '',
        'year': '',
        'month': '',
        'catename': '',
        'catename2': '',
        'sido': '',
        'gugun': '',
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
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)    # for debugging
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entityList = tree.xpath('//table[@width="740"]//tr')

    storeList = []
    for i in range(len(entityList)):
        infoList = entityList[i].xpath('./td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) != 5): continue  # 5개 있는 것이 점포 정보

        strtemp = "".join(infoList[2].itertext())
        if strtemp == None: continue
        strtemp = strtemp.lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
        if strtemp == '': continue

        storeInfo = {}
        storeInfo['name'] = '카페쎄리오'
        storeInfo['subname'] = '';  storeInfo['addr'] = '';  storeInfo['pn'] = ''

        idx = strtemp.find('주소 :')
        if idx == -1: continue
        subname = strtemp[:idx].rstrip();       strtemp = strtemp[idx+4:].lstrip()
        if subname.startswith('매장명 :'): subname = subname[5:].lstrip()
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        idx = strtemp.find('전화번호 :')
        if idx == -1: continue
        storeInfo['addr'] = strtemp[:idx].rstrip()
        storeInfo['pn'] = strtemp[idx+6:].lstrip().rstrip().lstrip().replace('.', '-').replace(')', '-')

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
