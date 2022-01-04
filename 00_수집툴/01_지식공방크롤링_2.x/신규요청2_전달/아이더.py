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

    outfile = codecs.open('eider_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|XCOORD|YCOORD@@아이더\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'아이더|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(storeList) < 6: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.eider.co.kr'
    api = '/eider/ko/customercenter/ajaxStoreInfo'

    data = {
        'address1' : '',
        'address2': '',
        'searchWord': '',
        'storeType': 'ALL',
        'specialZone1': '',
        'specialZone2': '',
        'specialZone3': '',
        'showMode': '',
        'rec': '6',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        urls = url + api
        #req = urllib2.Request(urls, params, headers=hdr)
        req = urllib2.Request(urls, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['resultObj']['shopInfoList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '아이더'
        store_info['subname'] = ''
        strtemp = entity_list[i]['displayName'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        if entity_list[i].get('streetName'): store_info['newaddr'] = entity_list[i]['streetName']

        store_info['pn'] = ''
        if entity_list[i].get('phone1'):
            store_info['pn'] = entity_list[i]['phone1'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')
        store_info['xcoord'] = ''
        if entity_list[i].get('longitude'): store_info['xcoord'] = entity_list[i]['longitude']
        store_info['ycoord'] = ''
        if entity_list[i].get('latitude'): store_info['ycoord'] = entity_list[i]['latitude']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
