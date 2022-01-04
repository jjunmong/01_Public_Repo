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

    outfile = codecs.open('bccard_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@비씨카드\n")

    page = 1
    while True:
        store_list = getStores(page)    # 본사 정보
        if store_list == None:
            break

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        store_list = getStores2(page)   # 센터 정보
        if store_list == None:
            break

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 2: break   # 한번 호출로 모든 정보 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):   # 본사 크롤링
    # 'https://www.bccard.com/card/html/company/kr/company/location/head/location.jsp'
    url = 'https://www.bccard.com'
    api = '/card/html/company/kr/company/location/head/location.jsp'
    data = {}
    #params = urllib.urlencode(data)
    #print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #'Content-Length': '30',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'Cookie': 'session_cookie=db340ce2fcdeabf9fda2b50c14d35a3ced533934ae2ef2df2ba70f5719e62fba768bca163cdc6f186b42ca30473008ea83d3c21215bac42720189bb3c6d890e0c9c2461b3afd3b0590afbac66f34624887df20bb8e50e7bcbbc8356a6002a3e5; JSESSIONID=B4M8dBc7PW15pk9J3rfkkl4EJhdfuKAql12KGmvFvr1OqOfGMxRnQMOown5SlS6z.etwas2_servlet_engine1; XTVID=A180501152249739329; _ga=GA1.3.1159740144.1525155770; _gid=GA1.3.393662324.1525155770; _gat_gtag_UA_111271396_1=1; xloc=2560X1440; UID=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)

        #urls = url + api + '?' + params
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)

    entity_list = tree.xpath('//dl[@class="locationJuso_text"]')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//dt')
        info_list = entity_list[i].xpath('.//dd')
        if len(name_list) < 1 or len(info_list) < 1: continue

        store_info = {}

        store_info['name'] = '비씨카드'
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('비씨카드'): strtemp = strtemp[4:].lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['pn'] = '' ;    store_info['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('주소 :'): strtemp = strtemp[4:].lstrip()
            idx = strtemp.find('전화 :')
            if idx != -1:
                store_info['newaddr'] = strtemp[:idx].rstrip()
                strtemp = strtemp[idx+4:].lstrip()
                idx = strtemp.find('위치')
                if idx != -1:
                    store_info['pn'] = strtemp[:idx].rstrip()

        store_list += [store_info]

    return store_list

def getStores2(intPageNo):      # 센터 크롤링
    # 'https://www.bccard.com/card/html/company/kr/company/location/center/center6/center06.jsp'
    url = 'https://www.bccard.com'
    api = '/card/html/company/kr/company/location/center/center6/center06.jsp'
    data = {}
    #params = urllib.urlencode(data)
    #print(params)

    try:
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)

    subapi_list = tree.xpath('//div[@class="tab01"]//li//a/@href')

    store_list = []
    for i in range(len(subapi_list)):
        suburl = url + subapi_list[i]
        print(suburl)  # for debugging

        try:
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        subtree = html.fromstring(subresponse)

        name_list = subtree.xpath('//li[@class="mapJuso"]//dt')
        info_list = subtree.xpath('//li[@class="mapJuso"]//dd')

        if len(name_list) < 1 or len(info_list) < 1: continue

        store_info = {}

        store_info['name'] = '비씨카드'
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('비씨카드'): strtemp = strtemp[4:].lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['pn'] = '';
        store_info['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('주소 :'): strtemp = strtemp[4:].lstrip()
            store_info['newaddr'] = strtemp.replace('㈜', '(주)')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
