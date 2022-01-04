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

    outfile = codecs.open('public_healthcare_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE1|TYPE2|TELNUM|NEWADDR|SINCE|URL|ID|XCOORD|YCOORD@@보건소\n")

    page = 1
    retry_count = 0
    while True:
        store_list = getStores(75, page)    # 보건의료원
        if store_list == None:
            if retry_count > 2: break
            else: retry_count += 1;     continue

        retry_count  = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type1'])
            outfile.write(u'%s|' % store['type2'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s|' % store['url'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    page = 1
    retry_count = 0
    while True:
        store_list = getStores(71, page)    # 보건소
        if store_list == None:
            if retry_count > 2: break
            else: retry_count += 1;     continue

        retry_count  = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type1'])
            outfile.write(u'%s|' % store['type2'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s|' % store['url'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 199: break
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    page = 1
    retry_count = 0
    while True:
        store_list = getStores(72, page)    # 보건지소
        if store_list == None:
            if retry_count > 2: break
            else: retry_count += 1;     continue

        retry_count  = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type1'])
            outfile.write(u'%s|' % store['type2'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s|' % store['url'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 799: break
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    page = 1
    retry_count = 0
    while True:
        store_list = getStores(73, page)    # 보건진료소
        if store_list == None:
            if retry_count > 2: break
            else: retry_count += 1;     continue

        retry_count  = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type1'])
            outfile.write(u'%s|' % store['type2'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s|' % store['url'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 799: break
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(type_code, page_no):
    # 'http://www.g-health.kr/portal/health/pubHealthSearch/get_list.do'
    url = 'http://www.g-health.kr'
    api = '/portal/health/pubHealthSearch/get_list.do'
    data = {
        'c_view': '',
        'ykiho_enc': '',
        #'cl_cd': '',
        'dgsbjt_cd': '',
        'rows': '5',
        'x_pos': '126.99243210837594',
        'y_pos': '37.571284694433965',
        'bbsId': 'U00198',
        'menuNo': '200452',
        'sido_cd': '',
        'sggu_cd': '',
        'cl_cd1': '',
        'yadm_nm': '',
        'cl_cd2': '',
    }
    data['cl_cd'] = type_code
    data['cpage'] = page_no
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #'Content-Length': '30',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ccsession=201804261638350004407840781366; ccguid=201804261638350004407840781366; JSESSIONID=Qf5qhhBbTCTX2QK2SlhqCjHxH3wBY9GftTv7sXcnJhyPQxgQ0mDV!486546763!456521807; WMONID=VG_GYKbh5Pq; __utma=154953518.171085328.1524728318.1524728318.1524728318.1; __utmc=154953518; __utmz=154953518.1524728318.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; wcs_bt=407305de1ac038:1524728436; __utmb=154953518.2.10.1524728318',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url + api, 'rcode1=서울&rcode2=강남구', headers=hdr)
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
    entity_list = json.loads(response)

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = entity_list[i]['yadm_nm'].replace(' ', '/')
        store_info['subname'] = ''

        store_info['id'] = entity_list[i]['ykiho_enc']

        store_info['newaddr'] = entity_list[i]['addr']
        store_info['pn'] = entity_list[i]['telno'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['url'] = entity_list[i]['hosp_url']
        store_info['since'] = entity_list[i]['estb_dd']


        store_info['type1'] = entity_list[i]['cl_cd_nm']
        store_info['type2'] = entity_list[i]['org_ty_cd_nm']

        store_info['xcoord'] = entity_list[i]['x_pos']
        store_info['ycoord'] = entity_list[i]['y_pos']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
