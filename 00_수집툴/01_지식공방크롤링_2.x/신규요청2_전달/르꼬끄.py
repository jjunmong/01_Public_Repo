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

    outfile = codecs.open('lecoq_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|TYPE|NEWADDR|XCOORD|YCOORD@@르꼬끄스포르티브\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'르꼬끄스포르티브|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/3)
def getStores(intPageNo):
    url = 'http://www.lecoqsportif.co.kr'
    api = '/shopListByRegion.do'

    data = {
        'brandCd': '',
        'sido': '',
        'sigungu': '',
        'shopType': '',
        'shopNm': '',
        'listSize': '10',
        'searchType': 'region',
    }
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)  # POST 방식일 땐 이렇게 호출해야 함!!!
        req = urllib2.Request(url + api, params)        # header값 맞추기 어려운 경우에는, 그냥 header 정보 없이 호출할 것! (특별한 경우를 빼고는 이렇게 호출해도 됨)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)

    entity_list = response_json['shopList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '르꼬끄스포르티브'
        strtemp = entity_list[i]['SHOP_NM'].lstrip().rstrip()
        strtemp = strtemp.replace('르꼬끄', '').replace('스포르티브', '').rstrip().lstrip()
        if not strtemp.endswith('점'): strtemp += '점'
        store_info['subname'] = strtemp.replace(' ', '/')
        store_info['type'] = entity_list[i]['SHOP_TYPE']

        store_info['newaddr'] = ''
        strtemp = entity_list[i]['SHOP_ADDR']
        if strtemp != None:
            store_info['newaddr'] = strtemp

            if entity_list[i].get('SHOP_ADDR_DTL'):
                store_info['newaddr'] += ' ' + entity_list[i]['SHOP_ADDR_DTL']

        store_info['pn'] = ''
        strtemp = entity_list[i]['TEL_NO']
        if strtemp != None:
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['id'] = entity_list[i]['SHOP_CD']

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['HARDNESS']
        store_info['ycoord'] = entity_list[i]['LATITUDE']

        store_list += [store_info]

    return store_list


'''
# v1.0
def getStores(intPageNo):
    url = 'http://www.lecoqsportif.co.kr'
    api = '/service/shop.php'

    data = {}
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    #print(params)

    try:
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    entity_list = tree.xpath('//table[@class="tbl-find"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '르꼬끄스포르티브'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith('(상설)'): strtemp = strtemp[:-4].rstrip()

            strtemp = strtemp.replace('르꼬끄', '').replace('스포르티브', '').rstrip().lstrip()
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['type'] = ''
        strtemp = "".join(info_list[1].itertext())

        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = info_list[5].xpath('.//a/@data-lng')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['xcoord'] = strtemp
        temp_list = info_list[5].xpath('.//a/@data-lat')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['ycoord'] = strtemp

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
