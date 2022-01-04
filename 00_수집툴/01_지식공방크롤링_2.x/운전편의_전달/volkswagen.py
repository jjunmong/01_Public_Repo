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

    outfile = codecs.open('volkswagen_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|SUBNAME2@@폭스바겐\n")

    outfile2 = codecs.open('volkswagen_svc_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|SUBNAME2@@폭스바겐서비스센터\n")


    while True:
        storeList = getStores('S')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'폭스바겐|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['subname2'])

        break     # 한 페이지에 모든 정보 다 있음

    time.sleep(random.uniform(0.5, 2.5))

    while True:
        storeList = getStores('C')
        if storeList == None: break;

        for store in storeList:
            outfile2.write(u'폭스바겐서비스센터|')
            outfile2.write(u'%s|' % store['subname'])
            outfile2.write(u'%s|' % store['pn'])
            outfile2.write(u'%s|' % store['newaddr'])
            outfile2.write(u'%s|' % store['ot'])
            outfile2.write(u'%s\n' % store['subname2'])

        break     # 한 페이지에 모든 정보 다 있음

    outfile.close()
    outfile2.close()


def getStores(type_info):
    url = 'https://www.vwkr.co.kr'
    api = '/2016cms/api/network_list.jsp'
    data = {
        'sido': '',
        'gugun': '',
     }
    data['ntype'] = type_info
    params = urllib.urlencode(data)
    print(params)

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=sm7h8s2duqhbeq90qhdo1cp555; 2a0d2363701f23f8a75028924a3af643=MTI1LjEyOS4yNDIuMjI3; _gat=1; _ga=GA1.3.1065939222.1486961929'
    }
    try:
        req = urllib2.Request(url + api, params, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entityList = tree.xpath('//li[@class="mp"]')

    storeList = []
    for i in range(len(entityList)):
        subname_list = entityList[i].xpath('.//a//p')
        subname2_list = entityList[i].xpath('.//a//em')
        info_list = entityList[i].xpath('.//div[@class="area_info"]//li//p')

        if len(subname_list) < 1: continue
        if len(info_list) < 2: continue  # 최소 2개 필드 있어야 함
        storeInfo = {}

        subname = subname_list[0].text
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')
        storeInfo['subname2'] = ''
        if len(subname2_list) > 0:
            storeInfo['subname2'] = subname2_list[0].text.lstrip().rstrip().replace(' ', '/')

        storeInfo['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = "".join(info_list[1].itertext()).strip('\r\t\n')
        if strtemp != None:
            if strtemp.startswith('T'): strtemp = strtemp[1:].lstrip()
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-').replace(' ', '')

        storeInfo['ot'] = ''
        if len(info_list) >= 3:
            strtemp = "".join(info_list[2].itertext()).strip('\r\t\n')
            if strtemp != None:
                storeInfo['ot'] = strtemp.rstrip().lstrip().replace(' ', '').replace('<br>/', ';')

        storeList += [storeInfo]

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
