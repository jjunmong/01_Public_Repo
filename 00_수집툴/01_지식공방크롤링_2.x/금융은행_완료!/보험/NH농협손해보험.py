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

    outfile = codecs.open('insurance_nhfire_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR@@NH농협손해보험\n")

    # 지역총국 (지역총국만 전달하는 Form Data의 값이 다름)
    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores2(page, '/location/retrieveCustomerCenterLocationList.nhfire', '지역총국')
        page += 1

        if store_list == None: break;
        elif len(store_list) > 0:
            if store_list[0]['id'] ==  sentinel_store_id: break
            elif store_list[0]['id'] != '': sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    # NHC지점
    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores(page, '/location/retrieveNhcLocationList.nhfire', 'NHC지점')
        page += 1

        if store_list == None: break;
        elif len(store_list) > 0:
            if store_list[0]['id'] ==  sentinel_store_id: break
            elif store_list[0]['id'] != '': sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    # TM센터
    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores(page, '/location/retrieveTMLocationList.nhfire', 'TM센터')
        page += 1

        if store_list == None: break;
        elif len(store_list) > 0:
            if store_list[0]['id'] ==  sentinel_store_id: break
            elif store_list[0]['id'] != '': sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))


    # 교차/GA지점
    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores(page, '/location/retrieveIALocationList.nhfire', '교차/GA지점')
        page += 1

        if store_list == None: break;
        elif len(store_list) > 0:
            if store_list[0]['id'] ==  sentinel_store_id: break
            elif store_list[0]['id'] != '': sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    # 농축협
    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores(page, '/location/retrieveNhBrcList.nhfire', '농축협')
        page += 1

        if store_list == None: break;
        elif len(store_list) > 0:
            if store_list[0]['id'] ==  sentinel_store_id: break
            elif store_list[0]['id'] != '': sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo, api, store_type):
    url = 'https://www.nhfire.co.kr'
    data = {
        'locSearchType': '',
        'locSearchWord': '',
        'devonOrderBy': '',
    }
    data['devonTargetRow'] = (intPageNo-1)*10 + 1

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
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//div[@class="ProTable"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = 'NH농협손해보험'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if store_type == '농축협':
                idx = strtemp.find('농협')
                if idx != -1:
                    store_info['name'] = strtemp[:idx+2]
                    store_info['subname'] = strtemp[idx+2:].lstrip().replace(' ', '/')
                else:
                    idx = strtemp.find('협 ')
                    if idx != -1:
                        store_info['name'] = strtemp[:idx+1]
                        store_info['subname'] = strtemp[idx+1:].lstrip().replace(' ', '/')
                    else: store_info['name'] = strtemp.replace(' ', '/')
            else: store_info['subname'] = strtemp.replace(' ', '/')

        store_info['type'] = store_type

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('('):     # 우편번호 정보 제거
                idx = strtemp.find(')')
                strtemp = strtemp[idx+1:].lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = info_list[4].xpath('.//a/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('LocationInfo(')
            if idx != -1:
                strtemp = strtemp[idx+13:]
                idx = strtemp.find(');')
                store_info['id'] = strtemp[:idx].lstrip().rstrip()[1:-1]

        store_list += [store_info]

    return store_list

# 지역총국 데이터 크롤링
def getStores2(intPageNo, api, store_type):
    url = 'https://www.nhfire.co.kr'
    data = {
        'addrNo': '',
        'dtlBsnClsfCd': '',
        'checkSearch': '',
        'flag': '',
        'sidoCdList': '',
        'ccwCdList': '',
        'locSearchWord': '',
        'devonOrderBy': '',
    }
    data['devonTargetRow'] = (intPageNo-1)*10 + 1


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
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//div[@class="ProTable mt50"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = 'NH농협손해보험'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if store_type == '농축협':
                idx = strtemp.find('농협')
                if idx != -1:
                    store_info['name'] = strtemp[:idx+2]
                    store_info['subname'] = strtemp[idx+2:].lstrip().replace(' ', '/')
                else:
                    idx = strtemp.find('협 ')
                    if idx != -1:
                        store_info['name'] = strtemp[:idx+1]
                        store_info['subname'] = strtemp[idx+1:].lstrip().replace(' ', '/')
                    else: store_info['name'] = strtemp.replace(' ', '/')
            else: store_info['subname'] = strtemp.replace(' ', '/')

        store_info['type'] = store_type

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('('):     # 우편번호 정보 제거
                idx = strtemp.find(')')
                strtemp = strtemp[idx+1:].lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = info_list[5].xpath('.//a/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('LocationInfo(')
            if idx != -1:
                strtemp = strtemp[idx+13:]
                idx = strtemp.find(');')
                store_info['id'] = strtemp[:idx].lstrip().rstrip()[1:-1]

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
