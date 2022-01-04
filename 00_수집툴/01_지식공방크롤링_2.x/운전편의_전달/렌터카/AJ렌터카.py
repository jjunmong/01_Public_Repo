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

    outfile = codecs.open('ajrentacar_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|OT|MTYPE@@AJ렌터카\n")

    page = 1
    while True:
        store_list = getStores2(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % u'렌터카')

        page += 1

        if page == 8: break     # 1~7까지 호출해야 함

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2019/1)
def getStores2(areacode):
    # 'https://www.ajrentacar.co.kr/front/ko/cscenter/branch_list.do?areacode=0001&areadetcode=&depttype=&menuCd=05_01'
    url = 'https://www.ajrentacar.co.kr'
    api = '/front/ko/cscenter/branch_list.do'
    data = {
        'areadetcode': '',
        'depttype': '',
        'menuCd': '05_01',
    }
    data['areacode'] = '000' + str(areacode)
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//tbody[@id="branchList"]//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 3: continue  # 최소 3개 필드 있어야 함

        store_info = {}

        store_info['name'] = 'AJ렌터카'
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['addr'] = '' ;    store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['ot'] = ''
        temp_list = info_list[0].xpath('./a/@href')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        subapi = temp_list[0]

        try:
            suburls = url + subapi
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 1.1))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];
            continue

        code = result.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="tbl01"]//tbody//tr')

        for j in range(len(subinfo_list)):
            tag_list = subinfo_list[j].xpath('.//th')
            value_list = subinfo_list[j].xpath('.//td')

            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            value = "".join(value_list[0].itertext())

            if tag == None or value == None: continue

            tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            if tag == '영업시간':
                store_info['ot'] = value

        store_list += [store_info]

    return store_list

# v1.0
def getStores(intPageNo):
    url = 'http://www.avis.co.kr'
    api = '/front/ko/cscenter/branch_list.do'
    data = {
        'menu_code': 'd1_2',
    }
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//tbody[@id="branchList"]//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 3: continue  # 최소 3개 필드 있어야 함

        store_info = {}

        store_info['name'] = 'AJ렌터카'
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['addr'] = '' ;    store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['ot'] = ''
        temp_list = info_list[0].xpath('./a/@href')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        subapi = temp_list[0]

        try:
            suburls = url + subapi
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 1.1))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];
            continue

        code = result.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="tbl01"]//tbody//tr')

        for j in range(len(subinfo_list)):
            tag_list = subinfo_list[j].xpath('.//th')
            value_list = subinfo_list[j].xpath('.//td')

            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            value = "".join(value_list[0].itertext())

            if tag == None or value == None: continue

            tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            if tag == '영업시간':
                store_info['ot'] = value

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
