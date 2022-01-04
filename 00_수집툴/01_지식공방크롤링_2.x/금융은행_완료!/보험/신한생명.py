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

sido_list = {      # 테스트용 광역시도 목록
    '부산': '부산광역시',
}

sido_list2 = {
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

    outfile = codecs.open('insurance_shinhanlife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|ADDR|NEWADDR|XCOORD|YCOORD@@신한생명\n")

    # 고객플라자(창구)
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
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            if page == 99: break
            elif len(store_list) < 12: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    # 지점
    call_count = 1
    for sido_name in sorted(sido_list):

        page = 1
        sentinel_store_id = '999999'
        while True:
            store_list = getStores2(sido_name, sido_list[sido_name], page, call_count)
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
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            if page == 99: break
            elif len(store_list) < 12: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()


# 고객플라자
def getStores(sido_name, sido_fullname, intPageNo, call_count):
    url = 'http://shinhanlife.tritops.co.kr'
    api = '/dwr/call/plaincall/ShinhanLifeBranchDAO.getSearchList.dwr'

    data = {
        'callCount': '1',
        'page': '/main_branch.jsp?menu=5',
        'httpSessionId': '',
        'scriptSessionId': 'D7F37957DA4E1FCC7B239C2F6D0D61D5294',
        'c0-scriptName': 'ShinhanLifeBranchDAO',
        'c0-methodName': 'getSearchList',
        'c0-id': '0',
        'c0-e1': 'string:5',
        'c0-e2': 'string:1',
        'c0-e3': 'string:9',
        'c0-e4': 'string:',
        'c0-e6': 'string:',
        'c0-e7': 'string:',
        'c0-e8': 'string:',
        'c0-e9': 'string:',
        'c0-e10': 'string:1',
        'c0-e11': 'string:',
        'c0-e12': 'string:',
        'c0-e13': 'string:',
        'c0-e14': 'string:',
        'c0-e15': 'string:',
        'c0-param0': 'Object_Object:{menu:reference:c0-e1, upmu_gb:reference:c0-e2, search_gb:reference:c0-e3, search_text:reference:c0-e4, pg:reference:c0-e5, seq_no:reference:c0-e6, gb:reference:c0-e7, f_sido_name:reference:c0-e8, f_sigungu_name:reference:c0-e9, s_cond:reference:c0-e10, s_dong:reference:c0-e11, s_branch:reference:c0-e12, sido_name:reference:c0-e13, sigungu_name:reference:c0-e14, s_subway:reference:c0-e15}',
    }
    data['c0-e5'] = 'string:' + str(intPageNo)
    #data['c0-e4'] = sido_name
    #data['c0-e11'] = sido_name
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
    print(response)

    store_list = []
    while True:
        idx = response.find('.tel=')
        if idx == -1: break

        store_info = {}
        store_info['name'] = '신한생명'

        store_info['pn'] = ''
        response = response[idx+5:]
        if not response.startswith('null'): # 전화번호 정보 없는 항목도 있음 ㅠㅠ
            response = response[1:]  # 앞에 있는 '"'문자 떼어내기
            idx = response.find('"')
            store_info['pn'] = response[:idx].replace(')', '-')

        idx = response.find('seq_no\']=')
        response = response[idx+9:]
        idx = response.find(';')
        store_info['id'] = response[:idx]

        idx = response.find('address_detail\']="')
        response = response[idx+18:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        store_info['addr'] = teststr2

        idx = response.find('branch_name\']="')
        response = response[idx+15:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc'].lstrip().rstrip()
        if teststr2.endswith('센터'): pass
        store_info['subname'] = teststr2.replace(' ', '/')

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


        idx = response.find('branch_gb_txt\']="')
        response = response[idx+17:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc'].lstrip().rstrip()
        store_info['type'] = teststr2

        store_list += [store_info]

    return store_list


# 지점
def getStores2(sido_name, sido_fullname, intPageNo, call_count):
    url = 'http://shinhanlife.tritops.co.kr'
    api = '/dwr/call/plaincall/ShinhanLifeBranchDAO.getSearchList.dwr'

    data = {
        'callCount': '1',
        'page': '/main_branch.jsp?menu=0',
        'httpSessionId': '',
        'scriptSessionId': 'D7F37957DA4E1FCC7B239C2F6D0D61D5321',   # 촉탁병원 수집하려면 'D7F37957DA4E1FCC7B239C2F6D0D61D5359'로 지정 (촉탁병원은 결과값 포맷이 약간 다를 수도 있음, 확인 요망)
        'c0-scriptName': 'ShinhanLifeBranchDAO',
        'c0-methodName': 'getSearchList',
        'c0-id': '0',
        'c0-e1': 'string:0',    # menu 값 (촉탁병원 수집하려면 5로 지정)
        'c0-e2': 'string:1',
        'c0-e3': 'string:9',
        'c0-e4': 'string:',
        'c0-e6': 'string:',
        'c0-e7': 'string:',
        'c0-e8': 'string:',
        'c0-e9': 'string:',
        'c0-e10': 'string:1',
        'c0-e11': 'string:',
        'c0-e12': 'string:',
        'c0-e13': 'string:',
        'c0-e14': 'string:',
        'c0-e15': 'string:',
        'c0-param0': 'Object_Object:{menu:reference:c0-e1, upmu_gb:reference:c0-e2, search_gb:reference:c0-e3, search_text:reference:c0-e4, pg:reference:c0-e5, seq_no:reference:c0-e6, gb:reference:c0-e7, f_sido_name:reference:c0-e8, f_sigungu_name:reference:c0-e9, s_cond:reference:c0-e10, s_dong:reference:c0-e11, s_branch:reference:c0-e12, sido_name:reference:c0-e13, sigungu_name:reference:c0-e14, s_subway:reference:c0-e15}',
    }
    data['c0-e5'] = 'string:' + str(intPageNo)
    #data['c0-e4'] = sido_name
    #data['c0-e11'] = sido_name
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
    print(response)

    store_list = []
    while True:
        idx = response.find('.tel=')
        if idx == -1: break

        store_info = {}
        store_info['name'] = '신한생명'

        store_info['pn'] = ''
        response = response[idx+5:]
        if not response.startswith('null'): # 전화번호 정보 없는 항목도 있음 ㅠㅠ
            response = response[1:]  # 앞에 있는 '"'문자 떼어내기
            idx = response.find('"')
            store_info['pn'] = response[:idx].replace(')', '-')

        idx = response.find('seq_no\']=')
        response = response[idx+9:]
        idx = response.find(';')
        store_info['id'] = response[:idx]

        idx = response.find('address_detail\']="')
        response = response[idx+18:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc']
        store_info['addr'] = teststr2

        idx = response.find('branch_name\']="')
        response = response[idx+15:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc'].lstrip().rstrip()
        if teststr2.endswith('센터'): pass
        store_info['subname'] = teststr2.replace(' ', '/')

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


        idx = response.find('branch_gb_txt\']="')
        response = response[idx+17:]
        idx = response.find('"')
        strtemp = response[:idx]
        teststr = '{ "abc": "' + strtemp + '" }'
        test_json = json.loads(teststr)
        teststr2 = test_json['abc'].lstrip().rstrip()
        store_info['type'] = teststr2

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
