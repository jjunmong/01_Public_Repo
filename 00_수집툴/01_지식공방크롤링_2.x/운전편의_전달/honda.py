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

    outfile = codecs.open('honda_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|SUBNAME2|ID|TELNUM|NEWADDR@@HONDA\n")

    for i in range(1,7):    # 1~6을 호출해야 함
        store_list = getStores(i)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['subname2'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(area_code):
    url = 'https://www.hondakorea.co.kr'
    api = '/automobile/sales/retrieveDealerList.json'
    data = {
        #'areaCode': '1',        # 1 ~ 6
    }
    data['areaCode'] = str(area_code)
    params = json.dumps(data)
    print(params)

    hdr = {
        'Accept': 'application/json',     # 'text/html,application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        urls = url + api
        print(urls)
        #req = urllib2.Request(urls, params)
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)
    response_json = json.loads(response)

    entity_list = response_json['data']['dealerList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'HONDA'
        store_info['id'] = entity_list[i]['dealerId']
        store_info['subname'] = ''
        store_info['subname2'] = ''
        subname1 = entity_list[i]['dealerAbNm'].lstrip().rstrip()
        subname2 = entity_list[i]['dealerNm'].lstrip().rstrip()
        idx = subname2.find(subname1)
        if idx != -1:
            subname2 = subname2[:idx].rstrip()
        store_info['subname'] = subname1.replace(' ', '/')
        store_info['subname2'] = subname2.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = entity_list[i]['addr']
        if strtemp != None:
            store_info['newaddr'] = strtemp.lstrip().rstrip()

        store_info['pn'] = ''

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
