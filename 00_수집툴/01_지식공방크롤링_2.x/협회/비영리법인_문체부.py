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

    outfile = codecs.open('institute1_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ID|FEAT|SINCE@@비영리법인\n")

    # 문체부 허가법인 수집
    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s\n' % store['since'])

        page += 1

        if page == 499: break   # 2018년 9월 기준 134페이지까지 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


# 문체부 허가법인
def getStores(intPageNo):
    # 'http://www.mcst.go.kr/web/s_data/corpNaru/corpList.jsp?pCurrentPage=3&pCoType=&pSearchType=&pSearchWord='
    url = 'http://www.mcst.go.kr'
    api = '/web/s_data/corpNaru/corpList.jsp'
    data = {
        'pCoType': '',
        'pSearchType': '',
        'pSearchWord': '',
    }
    data['pCurrentPage'] = intPageNo
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
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@class="tbl-type01 type01-5 bl_none"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith('(재발급)'): strtemp = strtemp[:-5].rstrip()
            store_info['name'] = strtemp

        store_info['feat'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['feat'] = strtemp

        store_info['newaddr'] = ''
        store_info['pn'] = ''
        store_info['id'] = ''
        store_info['since'] = ''

        temp_list = info_list[2].xpath('.//a/@href')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        suburls = 'http://www.mcst.go.kr/web/s_data/corpNaru/' + temp_list[0]

        try:
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
        subtree = html.fromstring(subresponse)
        tag_list = subtree.xpath('//div[@class="viewWarp"]//dl//dt')
        value_list = subtree.xpath('//div[@class="viewWarp"]//dl//dd')

        for i in range(len(tag_list)):
            if len(value_list) <= i: break

            tag = "".join(tag_list[i].itertext())
            value = "".join(value_list[i].itertext())

            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').rstrip().lstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if tag.find('단체주소') != -1: store_info['newaddr'] = value
            elif tag.find('법인설립허가') != -1:
                store_info['since'] = value.replace('(내부결재일)', '').rstrip().lstrip()
            elif tag == '번호': store_info['id'] = value

        store_list += [store_info]

    return store_list

# 지자체 허가법인 (주소정보 없음...)
def getStores2(intPageNo):
    # 'http://www.mcst.go.kr?pSearchMenuCD=0414000000&pCurrentPage=3&pCoType=&pSidoType=&pSearchType=&pSearchWord='
    url = 'http://www.mcst.go.kr'
    api = '/web/s_data/corporation/corpList.jsp'
    data = {
        'pSearchMenuCD': '0414000000',
        'pCoType': '',
        'pSidoType': '',
        'pSearchType': '',
        'pSearchWord': '',
    }
    data['page'] = intPageNo
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
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@class="board"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 7: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith('(재발급)'): strtemp = strtemp[:-5].rstrip()
            store_info['name'] = strtemp

        store_info['feat'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['id'] = strtemp

        store_info['newaddr'] = ''
        store_info['pn'] = ''
        store_info['since'] = ''

        temp_list = info_list[4].xpath('.//a/@href')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        suburls = 'http://www.mcst.go.kr/web/s_data/corporation/' + temp_list[0]

        try:
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
        subtree = html.fromstring(subresponse)
        tagvalue_list = subtree.xpath('//table[@class="view"]//tbody//tr')

        for i in range(len(tagvalue_list)):
            tag_list = tagvalue_list[i].xpath('.//th')
            value_list = tagvalue_list[i].xpath('.//td')
            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            value = "".join(value_list[0].itertext())

            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').rstrip().lstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if tag.find('단체주소') != -1: store_info['newaddr'] = value
            elif tag.find('법인설립허가') != -1: store_info['since'] = value

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
