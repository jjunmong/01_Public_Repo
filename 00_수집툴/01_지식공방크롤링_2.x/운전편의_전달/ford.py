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

    outfile = codecs.open('ford_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|SUBNAME2|ORGNAME|ID|TELNUM|ADDR|NEWADDR|WEBSITE|XCOORD|YCOORD\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['subname2'])
            outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전체 전시장&서비스센터 정보 모두 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):

    try:
        # 아래와 같이 호출하면 다 얻을 수 있음
        # '(37.566535,126.97796919999996,500)' <= 서울 반경 500km(마일?) 이내 전시장/서비스센터 검색 조건
        urls = 'http://spatial.virtualearth.net/REST/v1/data/1652026ff3b247cd9d1f4cc12b9a080b/FordEuropeDealers_Transition/Dealer?spatialFilter=nearby(37.566535,126.97796919999996,500)&$select=*,__Distance&'
        urls += '$filter=CountryCode%20Eq%20%27KOR%27%20And%20Language%20Eq%20%27ko%27%20And%20Brand%20Eq%20%27Ford%27&$top=100&$format=json&key=Al1EdZ_aW5T6XNlr-BJxCw1l4KaA0tmXFI_eTl1RITyYptWUS0qit_MprtcG7w2F&Jsonp=processDealerResults'
        print(urls)
        result = urllib.urlopen(urls)
        #req = urllib2.Request(urls, None)
        #req = urllib2.Request(urls, params, headers=hdr)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = response.lstrip().rstrip()
    if response.startswith('processDealerResults('): response = response[21:]
    if response.endswith(')'): response = response[:-1]
    #print(response)
    response_json = json.loads(response)

    entity_list = response_json['d']['results']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'Ford'
        subname = entity_list[i]['DealerName'].lstrip().rstrip()
        store_info['orgname'] = subname
        store_info['id'] = entity_list[i]['DealerID']
        store_info['subname'] = '';     store_info['subname2'] = ''
        if subname.endswith(')'):
            subname = subname[:-1]
            idx = subname.rfind('(')
            store_info['subname2'] = subname[idx+1:]
            subname = subname[:idx].rstrip()
        store_info['subname'] = subname.replace(' ', '/')

        store_info['addr'] = '';     store_info['newaddr'] = ''
        store_info['newaddr'] = entity_list[i]['AddressLine1']
        strtemp = entity_list[i]['AddressLine2']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            if strtemp.startswith('(구주소)'): strtemp = strtemp[5:].lstrip()
            store_info['addr'] = strtemp

        store_info['pn'] = entity_list[i]['PrimaryPhone']
        store_info['website'] = ''
        strtemp = entity_list[i]['PrimaryURL']
        if strtemp != None:
            store_info['website'] = strtemp

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['Longitude']
        store_info['ycoord'] = entity_list[i]['Latitude']

        # 휴무일 정보도 있음 (필요할 때 추출할 것!!!)

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
