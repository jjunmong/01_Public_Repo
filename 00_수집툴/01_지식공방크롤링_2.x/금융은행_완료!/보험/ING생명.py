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

    outfile = codecs.open('insurance_inglife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@ING생명\n")

    # 고객센터 정보 얻기
    page = 1
    while True:
        store_list = getStores(page, 'TO')
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 9: break
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    # 고객창구 정보 얻기
    page = 1
    while True:
        store_list = getStores(page, '')
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 9:
            break
        elif len(store_list) < 5:
            break

        time.sleep(random.uniform(0.3, 0.9))

    # 지점 정보 얻기
    page = 1
    while True:
        store_list = getStores(page, 'BO')
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 49: break
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(intPageNo, store_type):
    url = 'https://www.orangelife.co.kr'
    api = '/cs/fb/TCWCSBFIQ010.ajax'
    data = {
        'TRADE_ID': 'TCWCSBFIQ010',
        'SCREEN_ID': 'SCWCSFB010M',
        'noLogging': 'false',
        '_useLogId': '-1',
        'nocache': '',
        #'tabType': 'BO',
        'searchType': '01',
        'searchContent': '',
    }
    data['pageNo'] = intPageNo
    data['tabType'] = store_type

    scp_json_data = {'devonTargetRow': '1', 'devonRowSize': 5}
    scp_json_data['devonTargetRow'] = str((intPageNo-1)*5 + 1)
    data['_SCP_JSON_DATA'] = scp_json_data

    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    #response_json = json.load(response)
    response_dict = ast.literal_eval(response)      # json처럼 보이지만 정확하게는 dict 구조체를 반환
    entity_list = response_dict['result']['rows']
    if entity_list == None: return None

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '오렌지라이프'
        store_info['id'] = entity_list[i]['salsOrgCd']
        store_info['type'] = ''
        if entity_list[i].has_key('salsOrgTypCd'):
            store_info['type'] = entity_list[i]['salsOrgTypCd']

        strtemp = entity_list[i]['salsOrgNm'].lstrip().rstrip()
        if strtemp == '': break     # 아무 내용도 없이 5개씩 결과값을 채워 보내는 경우가 있어서...
        store_info['orgname'] = strtemp

        if store_info['type'] == 'BO':
            if not strtemp.endswith('지점'): strtemp += '지점'
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['bsaddr'] + ' ' + entity_list[i]['dtaddr']
        store_info['pn'] = entity_list[i]['telno'].replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['xcoord'] = entity_list[i]['coordYVlu']
        store_info['ycoord'] = entity_list[i]['coordXVlu']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
