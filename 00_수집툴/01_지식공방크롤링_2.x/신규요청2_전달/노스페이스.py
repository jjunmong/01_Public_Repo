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
#import json
from lxml import html

sido_list2 = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list = {
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

    outfile = codecs.open('northface_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|ADDR|XCOORD|YCOORD@@노스페이스\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'노스페이스|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 19: break
            elif len(store_list) < 16:
                break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

# v2.0 (2018/2)
def getStores(sido_name, intPageNo):
    url = 'https://www.thenorthfacekorea.co.kr'
    api = '/store'
    data = {
        '_search': 'name',
        '_condition': 'like',
    }
    data['_find'] = sido_name
    if intPageNo > 1:
        data['page'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ASPSESSIONIDCCTACBTT=ACCNHAMCLLEGILHLIBELHBCO; ASPSESSIONIDCCQBADTT=CJCAIIFANCKCBNCIOAGIFPOD; wcs_bt=ae960d4b9e602c:1495367762; _ga=GA1.2.1998930491.1495194302; _gid=GA1.2.958050463.1495367763',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        urls = url + api + '?' + params
        #print(urls)     # for debugging
        result = urllib.urlopen(urls)

        #urls = url + api
        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//ul[@class="search-result"]//li[@class="search-list"]')

    store_list = []
    for i in range(len(entity_list)):
        id_list = entity_list[i].xpath('.//a/@data-store-id')
        name_list = entity_list[i].xpath('.//h2[@class="tit"]')
        pn_list = entity_list[i].xpath('.//span[@class="phonenum"]')
        addr_list = entity_list[i].xpath('.//span[@class="address"]')
        shoptype_list = entity_list[i].xpath('.//span[@class="brandstore"]')

        if len(id_list) < 1 or len(name_list) < 1: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '노스페이스'
        store_info['id'] = id_list[0]

        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['type'] = ''
        if len(shoptype_list) > 0:
            strtemp = "".join(shoptype_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if strtemp.startswith('|'): strtemp = strtemp[1:].lstrip()
                store_info['type'] = strtemp

        store_info['addr'] = ''
        if len(addr_list) > 0:
            strtemp = "".join(addr_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['addr'] = strtemp

                # 주소가 둘로 쪼개져 있는 경우가 있음
                if len(addr_list) > 1:
                    strtemp = "".join(addr_list[1].itertext())
                    if strtemp != None:
                        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        store_info['addr'] += ' ' + strtemp

        store_info['pn'] = ''
        if len(pn_list) > 0:
            strtemp = "".join(pn_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['xcoord'] = '';      store_info['ycoord'] = ''

        store_list += [store_info]

    return store_list

'''
# v1.0
def getStores(intPageNo):
    url = 'http://www.thenorthfacekorea.co.kr'
    api = '/brand/findRetailList.lecs'
    data = {
        'storeNo': '62',
        'siteNo': '34206',
        'sidoNm': '',
        'gugunNm': '',
        'searchText': '',
        'retailFlag': '',
        'boDisplaySetting': 'Y',
        'useYn': 'Y',
        'displayYn': 'N',
        'displayNo': 'NF2A02A01',
        'itemCount': '328',
        'perPage': '10',
        'perPageNavi': '10',
    }
    data['currentPage'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ASPSESSIONIDCCTACBTT=ACCNHAMCLLEGILHLIBELHBCO; ASPSESSIONIDCCQBADTT=CJCAIIFANCKCBNCIOAGIFPOD; wcs_bt=ae960d4b9e602c:1495367762; _ga=GA1.2.1998930491.1495194302; _gid=GA1.2.958050463.1495367763',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        urls = url + api + '?' + params
        #print(urls)     # for debugging
        result = urllib.urlopen(urls)

        #urls = url + api
        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//table[@class="table03"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '노스페이스'

        store_info['subname'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['type'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('|'): strtemp = strtemp[1:].lstrip()
            store_info['type'] = strtemp

        store_info['addr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = info_list[5].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('shopSn=')
            if idx != -1:
                strtemp = strtemp[idx+7:]
                idx = strtemp.find('&')
                store_info['id'] = strtemp[:idx]

        # suburl에 좌표값 있음 (필요할 때 추출할 것!)

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
