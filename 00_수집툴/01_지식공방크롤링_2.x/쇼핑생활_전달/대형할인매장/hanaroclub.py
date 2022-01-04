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

    outfile = codecs.open('hanaroclub_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|XCOORD|YCOORD\n")

    page = 1
    sentinel_pn = '999-999-9999'
    while True:
        storeList = getStores(page)
        if storeList == None: break;
        elif len(storeList) == 0: break

        # 끝에서 같은 내용이 계속 반복적으로 반환되어서...
        if sentinel_pn == storeList[0]['pn']: break
        elif storeList[0]['pn'] == '': pass
        else: sentinel_pn = storeList[0]['pn']

        for store in storeList:
            outfile.write(u'하나로클럽|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 9: break
        elif len(storeList) < 8: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://nonghyup.tritops.co.kr'
    api = '/dwr/call/plaincall/AspNonghyupNewDAO.getList.dwr'
    data = {
        'callCount': 1,
        'page': '/list_etc.jsp?menu=4&s_menu=1&type=tab',
        'httpSessionId': '',
        'scriptSessionId': '4195B9E2022F62905CEC2861BE1688FA567',
        'c0-scriptName': 'AspNonghyupNewDAO',
        'c0-methodName': 'getList',
        'c0-id': 0,
        #'c0-e1': 'string:3',
        'c0-e2': 'string:4',
        'c0-e3': 'string:1',
        'c0-e4': 'string:',
        'c0-e5': 'string:',
        'c0-e6': 'string:',
        'c0-e7': 'string:',
        'c0-e8': 'string:',
        'c0-param0': 'Object_Object:{pg:reference:c0-e1, menu:reference:c0-e2, s_menu:reference:c0-e3, region:reference:c0-e4, region_name:reference:c0-e5, oil_poll:reference:c0-e6, oil_name:reference:c0-e7, seq_no:reference:c0-e8}',
        #'batchId': 3,
    }
    data['c0-e1'] = 'string:' + str(intPageNo)
    data['batchId'] = intPageNo
    #params = json.dumps(data)
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive'
    }

    try:
        req = urllib2.Request(url + api, params, headers=hdr)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    storeList = []
    while True:

        idx = response.find('.tel="')
        if idx == -1: break

        storeInfo = {}
        response = response[idx+6:]
        idx = response.find('"')
        storeInfo['pn'] = response[:idx]

        idx = response.find('.name="')
        response = response[idx+7:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc'].lstrip().rstrip()
        if teststr2.endswith('(하나로클럽)'): teststr2 = teststr2[:-7].rstrip()
        if teststr2.endswith('하나로클럽'): teststr2 = teststr2[:-5].rstrip()
        storeInfo['subname'] = teststr2.replace(' ', '/')

        idx = response.find('address_new\']="')
        response = response[idx+15:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        storeInfo['newaddr'] = teststr2

        idx = response.find('map_x\']=')
        response = response[idx + 8:]
        idx = response.find(';')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        storeInfo['xcoord'] = teststr2[:3] + '.' + teststr2[3:]

        idx = response.find('address="')
        response = response[idx+9:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        storeInfo['addr'] = teststr2

        idx = response.find('map_y\']=')
        response = response[idx + 8:]
        idx = response.find(';')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        storeInfo['ycoord'] = teststr2[:2] + '.' + teststr2[2:]

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
