# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
import random
#import json
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

    outfile = codecs.open('knto_gocamping_utf8.txt', 'w', 'utf-8')
    #outfile.write("##NAME|SUBNAME|TELNUM|ADDR|WEBSITE|FEAT|COST|SOURCE2@@고캠핑\n")
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|FEAT|SOURCE2@@고캠핑\n")

    page = 1
    while True:
        store_list = getStores2(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            #outfile.write(u'%s|' % store['url'])
            outfile.write(u'%s|' % store['feat'])
            #outfile.write(u'%s|' % store['cost'])
            outfile.write(u'%s\n' % u'한국관광공사')

        page += 1

        if page == 499: break   # 2019년1월 기준 2112곳 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


# v2.0 (2019/1)
def getStores2(intPageNo):
    # 'https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=10&searchKrwd=&listOrdrTrget=last_updusr_pnttm&pageIndex=2'
    url = 'https://www.gocamping.or.kr'
    api = '/bsite/camp/info/list.do'
    data = {
        'pageUnit': '10',
        'searchKrwd': '',
        'listOrdrTrget': 'last_updusr_pnttm',
    }
    data['pageIndex'] = intPageNo
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)

    entity_list = tree.xpath('//div[@class="camp_search_list"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//div[@class="camp_cont"]//h2[@class="camp_tt"]')
        if len(name_list) < 1: continue

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('['):
                idx = strtemp.find(']')
                if idx != -1:
                    strtemp = strtemp[idx+1:].lstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['addr'] = ''
        temp_list = entity_list[i].xpath('.//li[@class="addr"]')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
                if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                store_info['addr'] = strtemp

        store_info['pn'] = ''
        temp_list = entity_list[i].xpath('.//li[@class="call_num"]')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['pn'] = strtemp

        store_info['feat'] = ''
        temp_list = entity_list[i].xpath('.//div[@class="camp_item_box"]//ul//li')
        for j in range(len(temp_list)):
            strtemp = "".join(temp_list[j].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += strtemp

        store_list += [store_info]

    return store_list

# v1.0
def getStores(intPageNo):
    url = 'https://www.gocamping.or.kr'
    api = '/campsite/areaList'
    data = {
        'mnCd': '010000',
        'dvOpCd': '',
        'dvCd': '',
        'cpstSral': '',
        'cpstBregYorn': '',
    }
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)

    entity_list = tree.xpath('//div[@class="sub-capping-listbox"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//div[@class="tit"]//p')
        if len(info_list) < 2: continue  # 최소 2개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['addr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
            if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        store_info['url'] = ''
        store_info['cost'] = ''
        store_info['feat'] = ''

        temp_list = info_list[0].xpath('./a/@onclick')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        strtemp = temp_list[0].lstrip().rstrip()
        idx = strtemp.find('areaDetail(')
        if idx == -1:
            store_list += [store_info];     continue

        strtemp = strtemp[idx+11:].lstrip()
        idx = strtemp.find(');')
        if idx == -1:
            store_list += [store_info];     continue

        store_id = strtemp[:idx].replace('\'', '').lstrip().rstrip()
        data['cpstSral'] = store_id
        subparams = urllib.urlencode(data)

        try:
            suburls = url + '/campsite/areaDetail' + '?' + subparams
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];
            continue

        subresponse = subresult.read()
        #print(subresponse)
        #subtree = html.fromstring(subresponse)
        subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)

        subinfo_list = subtree.xpath('//div[@class="camping-detailview"]//tbody//tr')

        for j in range(len(subinfo_list)):
            tag_list = subinfo_list[j].xpath('.//th')
            value_list = subinfo_list[j].xpath('.//td')

            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            value = "".join(value_list[0].itertext())

            if tag == None or value == None: continue

            tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', ' ')

            if tag == '주소': store_info['addr'] = value
            elif tag == '문의처': store_info['pn'] = value
            elif tag == '홈페이지': store_info['url'] = value
            elif tag == '이용요금': store_info['cost'] = value
            elif tag == '예약형태': store_info['feat'] = value.replace('예약하기', '').lstrip().rstrip()

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
