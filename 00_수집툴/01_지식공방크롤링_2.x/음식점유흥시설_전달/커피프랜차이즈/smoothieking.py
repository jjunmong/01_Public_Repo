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

    outfile = codecs.open('smoothieking_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|FEAT@@스무디킹\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;
        elif len(storeList) == 0: break;

        for store in storeList:
            outfile.write(u'스무디킹|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 49: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/6)
def getStores(intPageNo):
    # 'http://www.smoothieking.co.kr'
    url = 'http://www.smoothieking.co.kr'
    api = '/ajax/store_search_ajax.php'
    data = {
        'sc_addr1': '',
        'sc_addr2': '',
        'sc_str': '',
        'sc_option1_yn': '',
        'sc_option2_yn': '',
        'sc_option3_yn': '',
        'sc_option4_yn': '',
        'sc_option5_yn': '',
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
        print('HTTP request error (status %d)' % code);        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//div[@class="str_dnbox"]//table//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '스무디킹'

        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find('/')
            if idx != -1: strtemp = strtemp[:idx].rstrip()
            if strtemp == '-': strtemp = ''
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['feat'] = '';
        feat_list = info_list[4].xpath('.//img/@alt')
        for j in range(len(feat_list)):
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_list[j]

        store_info['id'] = ''
        temp_list = info_list[1].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('go_view(')
            if idx != -1:
                strtemp = strtemp[idx+8:]
                idx = strtemp.find(')')
                store_info['id'] = strtemp[:idx].rstrip().lstrip()[1:-1]

        # 상세정보 페이지에서 영업시간, 좌표정보 추가로 얻을 수 있음

        store_list += [store_info]

    return store_list

# v1.0
'''
def getStores(intPageNo):
    url = 'http://www.smoothieking.co.kr'
    api = '/store/store_search.do'
    data = {
        'type': '',
        'pageSize': '',
        'cmd': '',
        'addr2': '',
        'sc_addr1': '',
        'sc_str': '',
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
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//div[@class="str_dnbox"]//table//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '스무디킹'

        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find('/')
            if idx != -1: strtemp = strtemp[:idx].rstrip()
            if strtemp == '-': strtemp = ''
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['feat'] = '';
        feat_list = info_list[4].xpath('.//img/@alt')
        for j in range(len(feat_list)):
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_list[j]

        store_info['id'] = ''
        temp_list = info_list[1].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('go_view(')
            if idx != -1:
                strtemp = strtemp[idx+8:]
                idx = strtemp.find(')')
                store_info['id'] = strtemp[:idx].rstrip().lstrip()[1:-1]

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
