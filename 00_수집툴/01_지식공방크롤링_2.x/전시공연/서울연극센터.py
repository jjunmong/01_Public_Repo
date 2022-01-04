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

    outfile = codecs.open('stc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ALTNAME|TELNUM|ADDR|NEWADDR|REGION|SINCE|WEBSITE|SOURCE2@@문화센터_서울연극재단\n")

    page = 1
    while True:     # 대학로 소극장
        store_list = getStores('/Front/play/placeUniv.asp', page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['altname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['region'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s\n' % u'서울연극재단')

        page += 1

        if page == 49: break     # 2018년 7월 기준 17페이지까지 있음
        #elif len(store_list) < 10: break
        elif len(store_list) < 9: break

        time.sleep(random.uniform(0.3, 0.9))

    time.sleep(random.uniform(1, 2))

    page = 1
    while True:     # 기타서울지역 소극장
        store_list = getStores('/Front/play/placeEtc.asp', page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['altname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['region'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s\n' % u'서울연극재단')

        page += 1

        if page == 49: break     # 2018년 7월 기준 16페이지까지 있음
        #elif len(store_list) < 10: break
        elif len(store_list) < 9: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(requested_api, intPageNo):
    # 'http://www.e-stc.or.kr/Front/play/placeUniv.asp?page=17'
    url = 'http://www.e-stc.or.kr'
    #api = '/Front/play/placeUniv.asp'
    api = requested_api
    data = {}
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    #print(params)

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

    entity_list = tree.xpath('//table[@class="tableBbs"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('.//td')
        if len(temp_list) < 3: continue

        supapi_list = temp_list[2].xpath('.//a/@href')
        if len(supapi_list) < 1: continue

        subapi = supapi_list[0]

        try:
            suburls = url + subapi
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        tag_list = subtree.xpath('//div[@class="view_section"]//dt')
        value_list = subtree.xpath('//div[@class="view_section"]//dd')

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['altname'] = ''
        store_info['addr'] = ''
        store_info['newaddr'] = ''
        store_info['region'] = ''
        store_info['since'] = ''
        store_info['pn'] = ''
        store_info['website'] = ''

        for j in range(len(tag_list)):
            tag = "".join(tag_list[j].itertext())
            if j >= len(value_list): continue
            value = "".join(value_list[j].itertext())

            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if tag == '공연장명(한글)':
                store_info['name'] = value
            elif tag == '공연장명(영어)':
                store_info['altname'] = value
            elif tag == '연락처':
                store_info['pn'] = value
            elif tag == '홈페이지':
                store_info['website'] = value
            elif tag == '주소':
                store_info['addr'] = value
            elif tag == '새주소':
                store_info['newaddr'] = value
            elif tag == '개관년도':
                store_info['since'] = value
            elif tag == '지역구분':
                store_info['region'] = value

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
