# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import random
import codecs
import urllib
import urllib2
import json
from lxml import html

area2 = {
    '충남': '041'
}

area = {
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

    outfile = codecs.open('kfc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|NEWADDR|ETCADDR|OT|FEAT|XCOORD|YCOORD@@KFC\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['etcaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전국 점포정보 모두 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


# v2.0 (2018년6월)
def getStores(areaname):
    url = 'https://www.kfckorea.com'
    api = '/kfc/interface/selectStoreList'
    data = {
        'device': 'WEB',
        'store_search': '',
        #'sido_search': 'A0181',
        'sido_search': '',
        'gugun_search': '',
        'show_search': 'Y',
        'store_show_type': '',
        'sales_code_search': '',
        'initYn': 'N',
        'rows': '999',
    }
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
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
    print(response)
    #tree = html.fromstring(response)

    response_json = json.loads(response)
    entity_list = response_json['rows']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'KFC'
        strtemp = entity_list[i]['store_name'].lstrip().rstrip()
        if not strtemp.endswith('점'): strtemp += '점'
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['store_code'].lstrip().rstrip()

        store_info['newaddr'] = entity_list[i]['store_new_address'].lstrip().rstrip()
        store_info['addr'] = entity_list[i]['store_old_address'].lstrip().rstrip()
        store_info['etcaddr'] = entity_list[i]['store_new_address_detail'].lstrip().rstrip()
        store_info['pn'] = entity_list[i]['store_tel_number'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['ot'] = entity_list[i]['store_sales_time'].lstrip().rstrip()
        store_info['feat'] = entity_list[i]['store_sales_code_nm'].lstrip().rstrip().replace(',', ';')

        store_info['xcoord'] = entity_list[i]['store_longitude']
        store_info['ycoord'] = entity_list[i]['store_latitude']

        store_list += [store_info]

    return store_list

# v1.0
'''
def getStores(areaname):
    url = 'http://www.kfckorea.com'
    api = '/store/store_search.asp'
    data = {
        'sales_chimac_yn_': '',
        'sales_delivery_yn_': '',
        'sales_24_yn_': '',
        'sales_wifi_yn_': '',
        'sales_order_group_yn_': '',
        'sales_park_yn_': '',
        'sales_subway_yn_': '',
        'sales_mart_in_yn_': '',
        'searchFlag': 0,
        'addr_div2': '',
        'keyword': ''
    }
    data['addr_div1'] = areaname

    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    receivedData = json.loads(response)  # json 포맷으로 결과값 반환

    if receivedData.get('store'): storeList = receivedData['store']
    else: storeList = []

    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
