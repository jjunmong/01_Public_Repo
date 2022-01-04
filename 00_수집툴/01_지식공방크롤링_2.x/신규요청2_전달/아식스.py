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

sido_list2 = {      # 테스트용 광역시도 목록
    '경기도': '031',
}

sido_list = {
    '서울특별시': '02',
    '광주광역시': '062',
    '대구광역시': '053',
    '대전광역시': '042',
    '부산광역시': '051',
    '울산광역시': '052',
    '인천광역시': '032',
    '경기도': '031',
    '강원도': '033',
    '경상남도': '055',
    '경상북도': '054',
    '전라남도': '061',
    '전라북도': '063',
    '충청남도': '041',
    '충청북도': '043',
    '제주도': '064',
    '세종시': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('asics_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|XCOORD|YCOORD@@아식스\n")

    for sido_name in sorted(sido_list):

        page = 1
        prev_pn = '999-999-9999'
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                if store['pn'] == prev_pn: continue  # 같은 지점이 중복 추출되어 전화번호 체크로 같은 것 한번만 출력
                prev_pn = store['pn']

                outfile.write(u'아식스|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 20: break
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'https://www.asics.com'
    api = '/kr/ko-kr/store-locator'
    data = {
        'sortKey': 'nearest-list',
    }
    data['text'] = sido_name
    data['page'] = intPageNo-1
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

    entity_list = tree.xpath('//li[@class="store"]')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//h4/a/@title')
        info_list = entity_list[i].xpath('.//span')
        coord_list = entity_list[i].xpath('.//p/a/@href')
        if len(name_list) <1 or len(info_list) < 4: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['subname'] = ''
        strtemp = name_list[0]
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/').replace('-', '/')

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            strtemp = strtemp.replace('전화번호', '').replace(':', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-')

        # '서울특별시'로 검색했을 때 인근 지역(경기도)도 검색되므로 전화번호로 광역시도명을 만들어 붙여줌
        sido_prefix = ''
        if store_info['pn'].startswith('02-'): sido_prefix = '서울특별시'
        elif store_info['pn'].startswith('031-'): sido_prefix = '경기도'
        elif store_info['pn'].startswith('032-'): sido_prefix = '인천광역시'
        elif store_info['pn'].startswith('033-'): sido_prefix = '강원도'
        elif store_info['pn'].startswith('041-'): sido_prefix = '충청남도'
        elif store_info['pn'].startswith('042-'): sido_prefix = '대전광역시'
        elif store_info['pn'].startswith('043-'): sido_prefix = '충청북도'
        elif store_info['pn'].startswith('044-'): sido_prefix = '세종특별자치시'
        elif store_info['pn'].startswith('051-'): sido_prefix = '부산광역시'
        elif store_info['pn'].startswith('052-'): sido_prefix = '울산광역시'
        elif store_info['pn'].startswith('053-'): sido_prefix = '대구광역시'
        elif store_info['pn'].startswith('054-'): sido_prefix = '경상북도'
        elif store_info['pn'].startswith('055-'): sido_prefix = '경상남도'
        elif store_info['pn'].startswith('061-'): sido_prefix = '전라남도'
        elif store_info['pn'].startswith('062-'): sido_prefix = '광주광역시'
        elif store_info['pn'].startswith('063-'): sido_prefix = '전라북도'
        elif store_info['pn'].startswith('064-'): sido_prefix = '제주특별자치도'

        if sido_prefix == '': sido_prefix = sido_name   # '070' 전화번호이거나 '010' 전화번호이거나 전화번호 정보가 없으면...

        store_info['newaddr'] = ''  # 광역시도 이름은 없음 ㅠㅠ
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.find('광명시') != -1: sido_prefix = '경기도'
            elif strtemp.find('부천시') != -1: sido_prefix = '경기도'
            store_info['newaddr'] = sido_prefix + ' ' + strtemp   # 광역시도 이름 붙여줌

        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] += ' ' + strtemp


        store_info['xcoord'] = '';  store_info['ycoord'] = ''
        if len(coord_list) > 0:
            strtemp = coord_list[0]
            idx = strtemp.find('addr=')
            if idx != -1:
                temp_list = strtemp[idx+5:].split(',')
                store_info['xcoord'] = temp_list[1]
                store_info['ycoord'] = temp_list[0]

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
