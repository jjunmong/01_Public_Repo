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
import ast
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

    outfile = codecs.open('chrysler_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|TYPE|ETCNAME|WEBSITE|XCOORD|YCOORD@@크라이슬러\n")

    page = 1
    while True:
        store_list = getStores2(page)
        if store_list == None: break;

        prev_pn = '999-999-9999'
        for store in store_list:
            if store['pn'] == prev_pn: continue     # 같은 지점이 중복 추출되어 전화번호 체크로 같은 것 삭제
            prev_pn = store['pn']

            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['etcname'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전체 점포 정보 모두 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

# v2.0 (2019/2)
def getStores2(intPageNo):
    # 'https://www.jeep.co.kr/content/dam/cross-regional/apac/jeep/ko_kr/find-a-dealer/jeep-korea-dealers181231.js'
    url = 'https://www.jeep.co.kr/'
    api = '/content/dam/cross-regional/apac/jeep/ko_kr/find-a-dealer/jeep-korea-dealers181231.js'

    try:
        urls = url + api
        print(urls)
        req = urllib2.Request(urls, '')
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = response.replace('\r', '').replace('\t', '').replace('\n', '')
    response_dict = ast.literal_eval(response)

    # 전시장 추출
    entity_list = response_dict['sales']
    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'JEEP'
        store_info['subname'] = ''
        store_info['etcname'] = ''

        strtemp = entity_list[i]['dealerName'].lstrip().rstrip()
        if strtemp != None:
            strtemp = strtemp.upper().replace('JEEP', '').lstrip().rstrip()
            idx = strtemp.find('전시장')
            if idx != -1:
                store_info['subname'] = strtemp[:idx+9].rstrip()   # utf8 인코딩이 아니어서 한글1글자당 +3
                store_info['etcname'] = strtemp[idx+9:].lstrip()   # utf8 인코딩이 아니어서 한글1글자당 +3

        store_info['pn'] = ''
        if entity_list[i].get('phoneNumber'):
            store_info['pn'] = entity_list[i]['phoneNumber'].replace('(', '').replace(')', '-').lstrip().rstrip()
        store_info['newaddr'] = ''
        if entity_list[i].get('dealerAddress1'):
            store_info['newaddr'] = entity_list[i]['dealerAddress1']

        store_info['website'] = ''
        if entity_list[i].get('website'):
            store_info['website'] = entity_list[i]['website']

        store_info['type'] = ''
        if entity_list[i].get('department'):
            store_info['type'] = entity_list[i]['department']

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if entity_list[i].get('dealerShowroomLongitude'):
            store_info['xcoord'] = entity_list[i]['dealerShowroomLongitude']
        if entity_list[i].get('dealerShowroomLatitude'):
            store_info['ycoord'] = entity_list[i]['dealerShowroomLatitude']

        store_list += [store_info]

    # 서비스센터 추출
    entity_list = response_dict['services']
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'JEEP'
        store_info['subname'] = ''
        store_info['etcname'] = ''

        strtemp = entity_list[i]['dealerName'].lstrip().rstrip()
        if strtemp != None:
            #strtemp = strtemp.upper().replace('JEEP', '').replace(' 수성구', '/수성구').replace(' 서비스센터', '/서비스센터').lstrip().rstrip()
            strtemp = strtemp.upper().replace('JEEP', '').lstrip().rstrip()
            idx = strtemp.find('서비스센터')
            if idx != -1:
                store_info['subname'] = strtemp[:idx+15].rstrip()   # utf8 인코딩이 아니어서 한글1글자당 +3
                store_info['etcname'] = strtemp[idx+15:].lstrip()   # utf8 인코딩이 아니어서 한글1글자당 +3

        store_info['pn'] = ''
        if entity_list[i].get('phoneNumber'):
            store_info['pn'] = entity_list[i]['phoneNumber'].replace('(', '').replace(')', '-').lstrip().rstrip()
        store_info['newaddr'] = ''
        if entity_list[i].get('dealerAddress1'):
            store_info['newaddr'] = entity_list[i]['dealerAddress1']

        store_info['website'] = ''
        if entity_list[i].get('website'):
            store_info['website'] = entity_list[i]['website']

        store_info['type'] = ''
        if entity_list[i].get('department'):
            store_info['type'] = entity_list[i]['department']

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if entity_list[i].get('dealerShowroomLongitude'):
            store_info['xcoord'] = entity_list[i]['dealerShowroomLongitude']
        if entity_list[i].get('dealerShowroomLatitude'):
            store_info['ycoord'] = entity_list[i]['dealerShowroomLatitude']

        store_list += [store_info]

    return store_list


# v1.0
def getStores(intPageNo):
    url = 'http://www.chrysler.co.kr'
    api = '/fca/find-dealer/'

    try:
        urls = url + api
        print(urls)
        req = urllib2.Request(urls, '')
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    idx = response.find('var dealerList =')
    if idx == -1: return None
    response = response[idx+16:].lstrip()
    idx = response.find('};')
    if idx == -1: return None
    response = response[:idx+1]

    response = response.replace('http://', '').replace('https://', '')

    result = ''
    while True:     # 커멘트 부분 제거 ( /* */ 부분)
        idx = response.find('/*')
        if idx == -1:
            result += response;     break

        result += response[:idx].rstrip()
        response = response[idx+2:]
        idx = response.find('*/')
        response = response[idx+2:]

    response = result;  result = ''
    #print(response)

    while True:     # 커멘트 부분 제거 ( // ... 부분)
        idx = response.find('//')
        if idx == -1:
            result += response;     break

        result += response[:idx].rstrip()
        response = response[idx+2:]
        idx = response.find('"')
        response = response[idx:]

    response = result;
    #response = response.replace('//Gwangju', '').replace('//Busan', '').replace('//Daejeon', '').replace('//Pohang', '').replace('//Gangwon', '').replace('//Gyeongbuk', '')

    #print(response)
    response_dict = ast.literal_eval(response)

    store_list = []
    for key, subdict in response_dict.iteritems():
        dealer_data = subdict['dealer_data']
        for subkey, dealerdict in dealer_data.iteritems():
            store_info = {}
            store_info['name'] = '크라이슬러'
            store_info['subname'] = dealerdict['name'].replace(' ', '/')
            store_info['newaddr'] = ''
            strtemp = dealerdict['address'].lstrip().rstrip()
            if strtemp.startswith('('):
                idx = strtemp.find(')')
                if idx != -1: strtemp = strtemp[idx+1:].lstrip()
            store_info['newaddr'] = strtemp
            store_info['pn'] = dealerdict['phone'].replace(' ', '').replace('.', '-').replace(')', '-')
            store_info['website'] = dealerdict['url']
            store_info['xcoord'] = dealerdict['lng']
            store_info['ycoord'] = dealerdict['lat']

            store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
