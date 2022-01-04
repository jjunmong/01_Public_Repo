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

sido_list2 = {      # 테스트용 광역시도 목록
    '부산': '부산광역시',
}

sido_list = {
    '서울': '서울특별시',
    '광주': '광주광역시',
    '대구': '대구광역시',
    '대전': '대전광역시',
    '부산': '부산광역시',
    '울산': '울산광역시',
    '인천': '인천광역시',
    '경기': '경기도',
    '강원': '강원도',
    '경남': '경상남도',
    '경북': '경상북도',
    '전남': '전라남도',
    '전북': '전라북도',
    '충남': '충청남도',
    '충북': '충청북도',
    '제주': '제주특별자치도',
    '세종': '세종특별자치시'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('insurance_hanwha_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@한화손해보험\n")

    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores(page)
        page += 1

        if store_list == None: break;
        elif len(store_list) > 0:
            if store_list[0]['id'] ==  sentinel_store_id: break
            else: sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            #outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        if page == 999: break
        elif len(store_list) < 4: break
        #elif len(store_list) < 1: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.hwgeneralins.com'
    api = '/totalsearch/addr.do'
    data = {
        'collection': 'home_addr',
        'query': '',
        'avilTask': '',
        'avilVisit': '',
        'listCount': '4',
    }
    data['startCount'] = (intPageNo-1)*4
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    print(params)
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        req = urllib2.Request(url+api, params, headers=hdr)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    response_json = json.loads(response)
    result_list = response_json['SearchQueryResult']['Collection']
    if len(result_list) < 1: return None

    entity_list = result_list[0]['DocumentSet']['Document']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '한화손해보험'
        strtemp = entity_list[i]['Field']['ORGNM'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['Field']['ORGCD']
        store_info['type'] = entity_list[i]['Field']['HMPAG_XC_ORG_CSFNM']

        store_info['newaddr'] = entity_list[i]['Field']['ADDR']
        store_info['pn'] = entity_list[i]['Field']['TLNO']

        store_info['xcoord'] = entity_list[i]['Field']['CODN_X_VL']
        store_info['ycoord'] = entity_list[i]['Field']['CODN_Y_VL']

        store_list += [store_info]

    return store_list


def convert_full_to_half_char(ch):
    codeval = ord(ch)
    if 0xFF00 <= codeval <= 0xFF5E:
        ascii = codeval - 0xFF00 + 0x20;
        return unichr(ascii)
    else:
        return ch


def convert_full_to_half_string(line):
    output_list = [convert_full_to_half_char(x) for x in line]
    return ''.join(output_list)


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
