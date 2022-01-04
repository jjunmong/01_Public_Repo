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

    outfile = codecs.open('insurance_kb_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@KB손해보험\n")

    call_count = 1
    for sido_name in sorted(sido_list):

        page = 1
        sentinel_store_id = '999999'
        while True:
            store_list = getStores(sido_name, sido_list[sido_name], page, call_count)
            page += 1;      call_count += 1

            if store_list == None: break;
            elif len(store_list) > 0:
                if store_list[0]['id'] ==  sentinel_store_id: break
                else: sentinel_store_id = store_list[0]['id']

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            if page == 999: break
            elif len(store_list) < 4: break
            #elif len(store_list) < 1: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, sido_fullname, intPageNo, call_count):
    url = 'http://kbi.tritops.co.kr'
    api = '/dwr/call/plaincall/AspLigNewDAO.getBranchList.dwr'

    data = {
        'callCount': '1',
        'page': '/search_type_work.jsp?upmu_idx=0',
        'httpSessionId': '',
        'scriptSessionId': 'EFC0CC9FA498E7EF3488B68A34E75F51702',
        'c0-scriptName': 'AspLigNewDAO',
        'c0-methodName': 'getBranchList',
        'c0-id': '0',
        'c0-e2': 'string:work',
        'c0-e3': 'string:0',    # 지점 유형
        'c0-e6': 'string:',
        'c0-e7': 'string:',
        'c0-e8': 'string:',
        'c0-param0': 'Object_Object:{pg:reference:c0-e1, search_type:reference:c0-e2, upmu_idx:reference:c0-e3, simple_sido:reference:c0-e4, sido_name:reference:c0-e5, sigungu_name:reference:c0-e6, branch_code:reference:c0-e7, search_word:reference:c0-e8}',
        'batchId': '3',
    }
    data['c0-e1'] = 'string:' + str(intPageNo)
    data['c0-e4'] = sido_name
    data['c0-e5'] = sido_fullname
    data['c0-e8'] = '지역명/도로명/지점명'

    #data['c0-e4'] = urllib.urlencode(sido_name)
    #data['c0-e5'] = urllib.urlencode(sido_fullname)
    #data['c0-e8'] = urllib.urlencode('지역명/도로명/지점명')
    data['batchId'] = call_count
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
        idx = response.find('.tel=')
        if idx == -1: break

        store_info = {}
        store_info['name'] = 'KB손해보험'

        store_info['pn'] = ''
        response = response[idx+5:]
        if not response.startswith('null'): # 전화번호 정보 없는 항목도 있음 ㅠㅠ
            response = response[1:]  # 앞에 있는 '"'문자 떼어내기
            idx = response.find('"')
            store_info['pn'] = response[:idx].replace(')', '-')

        idx = response.find('branch_code\']="')
        response = response[idx+15:]
        idx = response.find('"')
        store_info['id'] = response[:idx]

        idx = response.find('branch_name\']="')
        response = response[idx+15:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc'].lstrip().rstrip()
        if teststr2.endswith('센터'): pass
        store_info['subname'] = teststr2.replace(' ', '/')

        idx = response.find('group_name\']="')
        response = response[idx+14:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc'].lstrip().rstrip()

        if teststr2 == '우수정비업체': break  # 정비업체 정보는 수집하지 않음
        elif teststr2 == '매직카서비스점':
            store_info['name'] = '매직카'
            store_info['subname'] = store_info['subname'].replace('매직카', '').lstrip().rstrip()
            if store_info['subname'].startswith('/'): store_info['subname'] = store_info['subname'][1:]

        store_info['type'] = teststr2

        idx = response.find('address_new\']="')
        response = response[idx+15:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        store_info['newaddr'] = teststr2

        idx = response.find('business_hour\']=')
        response = response[idx+16:]
        store_info['ot'] = ''
        if not response.startswith('null'): # bussiness hour 정보 없는 항목도 있음 ㅠㅠ
            response = response[1:]     # 앞에 있는 '"'문자 떼어내기
            idx = response.find('"')
            strtemp = response[:idx]
            teststr = '{ "abc": "' + strtemp + '" }'
            test_json = json.loads(teststr)
            teststr2 = test_json['abc']
            store_info['ot'] = teststr2

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
