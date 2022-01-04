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

sido_list2 = {      # 테스트용 시도 목록
    '제주': '제주도'
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
    '제주': '제주도',
    '세종': '세종특별시'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('nhbank_2_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|XCOORD|YCOORD\n")

    count = 0
    for sido_name in sorted(sido_list):
        page = 1
        sentinel_pn = '999-999-9999'
        while True:
            count += 1
            storeList = getStores(sido_name, sido_list[sido_name], page, count)
            if storeList == None: break;
            elif len(storeList) == 0: break

            # 끝에서 같은 내용이 계속 반복적으로 반환되어서...
            if sentinel_pn == storeList[0]['pn']: break
            elif storeList[0]['pn'] == '': pass
            else: sentinel_pn = storeList[0]['pn']

            for store in storeList:
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 99: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_shortname, sido_fullname, intPageNo, count):
    url = 'http://nonghyup.tritops.co.kr'
    api = '/dwr/call/plaincall/AspNonghyupNewDAO.getList.dwr'
    data = {
        'callCount': 1,
        'page': '/list_branch.jsp',
        'httpSessionId': '',
        'scriptSessionId': '952E2D24F6AB7E3A77F4FCE504EE43CC612',
        'c0-scriptName': 'AspNonghyupNewDAO',
        'c0-methodName': 'getList',
        'c0-id': 0,
        'c0-e1': 'string:2', # 1 = 농협은행 , 2 = 농협은행 + 농*축협 , 3 = 농*축협, 4 = 하나로마트 , 5 = 하나로 클럽
        'c0-e4': 'string:',
        'c0-e5': 'string:3',
        'c0-e6': 'string:',
        #'c0-e7': 'string:5',
        'c0-e8': 'string:0',
        'c0-e9': 'string:',
        'c0-e10': 'string:',
        'c0-e11': 'string:',
        'c0-e12': 'string:',
        'c0-e13': 'string:',
        'c0-e14': 'string:',
        'c0-e15': 'string:',
        'c0-e16': 'string:1',
        'c0-e17': 'string:',
        'c0-e18': 'string:1',
        'c0-e19': 'string:',
        'c0-e20': 'string:',
        'c0-e21': 'string:',
        'c0-e22': 'string:',
        'c0-param0': 'Object_Object:{menu:reference:c0-e1, sido:reference:c0-e2, full_sido:reference:c0-e3, sigungu:reference:c0-e4, search_type:reference:c0-e5, map_type:reference:c0-e6, pg:reference:c0-e7, scroll_top:reference:c0-e8, list_tab:reference:c0-e9, seq_no:reference:c0-e10, s_menu:reference:c0-e11, region:reference:c0-e12, region_name:reference:c0-e13, oil_poll:reference:c0-e14, oil_name:reference:c0-e15, nh_type:reference:c0-e16, atm_type:reference:c0-e17, search_cond:reference:c0-e18, search_word:reference:c0-e19, search_sido:reference:c0-e20, search_sigungu:reference:c0-e21, search_addr:reference:c0-e22}',
        #'batchId': 3,
    }
    data['c0-e2'] = 'string:' + sido_shortname
    data['c0-e3'] = 'string:' + sido_fullname
    data['c0-e7'] = 'string:' + str(intPageNo)
    data['batchId'] = count
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
    print(response)

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
        if teststr2.endswith('<출>'): teststr2 = teststr2[:-3].rstrip() + '출장소'
        elif teststr2.endswith('(출)'): teststr2 = teststr2[:-3].rstrip() + '출장소'
        storeInfo['subname'] = teststr2.replace(' ','').replace('농협','농협|')

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
