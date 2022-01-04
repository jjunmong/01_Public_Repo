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

    outfile = codecs.open('shoemaker_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|TYPE|XCOORD|YCOORD@@슈마커\n")

    page = 1
    while True:
        storeList = getStores2(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'슈마커|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(storeList) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2019/2)
def getStores2(intPageNo):
    url = 'https://www.shoemarker.co.kr'
    api = '/ASP/Customer/Ajax/StoreView.asp'
    urls = url + api + '?page=' + str(intPageNo)
    data = {
        'ChannelNM': '',
        'Keyword': '',
    }
    params = urllib.urlencode(data)
    print(intPageNo)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)  # POST 방식일 땐 이렇게 호출해야 함!!!
        req = urllib2.Request(urls, params)        # header값 맞추기 어려운 경우에는, 그냥 header 정보 없이 호출할 것! (특별한 경우를 빼고는 이렇게 호출해도 됨)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)
    entity_list = tree.xpath('//div[@class="contents"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//label//span')
        if len(info_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '슈마커'

        store_info['subname'] = ''
        store_info['feat'] = ''
        store_info['type'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith('(직)'):
                strtemp = strtemp[:-3]
                store_info['feat'] = '직영점'

            store_info['subname'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')
            if store_info['pn'] == '-': store_info['pn'] = ''

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        x_list = entity_list[i].xpath('.//input[@type="radio"]/@data-xpoint')
        y_list = entity_list[i].xpath('.//input[@type="radio"]/@data-ypoint')
        if len(x_list) > 0:
            store_info['xcoord'] = x_list[0]
        if len(y_list) > 0:
            store_info['ycoord'] = y_list[0]

        store_list += [store_info]

    return store_list

# v1.0
def getStores(intPageNo):
    url = 'http://www.shoemarker.co.kr'
    api = '/home/customer/store_list.php'
    data = {
        'act': 'list',
        'name': '',
        'sido': '',
        'gugun': '',
        'dong': '',
        'store_search': '',
        'kind': '',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
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
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)
    entity_list = tree.xpath('div[@class="section"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '슈마커'

        store_info['type'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['subname'] = ''
        store_info['feat'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith('(직)'):
                strtemp = strtemp[:-3]
                store_info['feat'] = '직영점'

            store_info['subname'] = strtemp

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

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
