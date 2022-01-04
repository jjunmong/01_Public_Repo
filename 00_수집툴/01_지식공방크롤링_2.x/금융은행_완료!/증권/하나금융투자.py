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
    '부산': '051',
}

sido_list = {
    '서울특별시': '02',
    '광주광역시': '062',
    '대구광역시': '053',
    '대전광역시': '042',
    '부산광역시': '051',
    '울산광역시': '052',
    '인천광역시': '032',
    '경기도': '031',
    '강원도': '033',
    '경상남도': '055',
    '경상북도': '054',
    '전라남도': '061',
    '전라북도': '063',
    '충청남도': '041',
    '충청북도': '043',
    '제주도': '064',
    '세종시': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('hana_investock_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@하나금융투자\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 2: break     # 한 페이지에서 광역시도내 지점정보 모두 반환
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'http://openhanafn.tritops.co.kr'
    api = '/dwr/call/plaincall/OpenHanabankDAO.getDtList.dwr'

    data = {
        'callCount': '1',
        'page': '/content_dt.jsp',
        'httpSessionId': '',
        'scriptSessionId': '9A328AA8FF2EA14C3DD6B7D77E4E2D81575',
        'c0-scriptName': 'OpenHanabankDAO',
        'c0-methodName': 'getDtList',
        'c0-id': '0',
        'c0-e1': 'string:page',
        'c0-e2': 'string:1',
        'c0-e3': 'string:1',
        'c0-e4': 'string:105',
        'c0-e5': 'string:',
        'c0-e6': 'string:',
        'c0-e7': 'string:1',
        'c0-e8': 'string:',
        'c0-param0': 'Object_Object:{page_type:reference:c0-e1, menu:reference:c0-e2, biz_type:reference:c0-e3, seq_no:reference:c0-e4, admin_no:reference:c0-e5, daetoo_no:reference:c0-e6, search_type:reference:c0-e7, scroll_height:reference:c0-e8, search_word:reference:c0-e9}',
        'batchId': '5',
    }
    data['c0-e9'] = sido_name
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
        urls = url + api
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    store_list = []
    while True:
        idx = response.find('.tel="')
        if idx == -1: break

        store_info = {}
        store_info['name'] = '하나금융투자'

        response = response[idx+6:]
        idx = response.find('"')
        store_info['pn'] = response[:idx].replace(')', '-')

        idx = response.find('daetoo_no\']="')
        response = response[idx+13:]
        idx = response.find('"')
        store_info['id'] = response[:idx]

        idx = response.find('address_new\']="')
        response = response[idx+15:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        store_info['newaddr'] = teststr2

        idx = response.find('map_x\']=')
        response = response[idx + 8:]
        idx = response.find(';')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        store_info['xcoord'] = teststr2[:3] + '.' + teststr2[3:]

        idx = response.find('.address="')
        response = response[idx+10:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        store_info['newaddr'] += ' (' + teststr2 + ')'

        idx = response.find('map_y\']=')
        response = response[idx + 8:]
        idx = response.find(';')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        store_info['ycoord'] = teststr2[:2] + '.' + teststr2[2:]

        idx = response.find('.name="')
        response = response[idx + 7:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc'].lstrip().rstrip()
        if teststr2.endswith('센터'): pass
        elif teststr2.endswith('영업소'): pass
        elif not teststr2.endswith('지점'): teststr2 += '지점'
        store_info['subname'] = teststr2.replace(' ', '/')

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
