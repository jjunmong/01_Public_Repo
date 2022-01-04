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

sido_list2 = {      # 테스트용 광역시도 목록
    '부산': '051',
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

    outfile = codecs.open('hanabank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDRSUB|NEWADDR\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['newaddr'])

            page += 1

            if page == 2: break     # 한 페이지에서 광역시도내 지점정보 모두 반환
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 1.1))

        time.sleep(random.uniform(2, 4))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'https://openhanafn.ttmap.co.kr'
    api = '/content.jsp'

    data = {
        'search_flag': 'search',
        'tab': '',
        'lang': 'ko',
        #'branch_check': 'ko',
        'x1': '127046793',
        'x2': '127059689',
        'y1': '37476617',
        'y2': '37485622',
        'seq_no': '',
        'type': '',
        'map_x': '',
        'map_y': '',
        'poi_pg:': '1',
        'poi_ps': '10',
        'poi_x': '',
        'poi_y': '',
        'search_type': '0',
        #'search_word': '서울시 강남구',
        'btn_search': '제출',
    }
    data['search_word'] = sido_name
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        urls = url + api
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="result_list"]//ul')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//li')
        if len(info_list) < 4: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = 'KEB하나은행'
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.endswith('(출)'): strtemp = strtemp[:-3].rstrip() + '출장소'
            elif strtemp.endswith('센터'): pass
            elif strtemp.endswith('본점'): pass
            elif not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['addr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_list += [store_info]

    return store_list


def convert_full_to_half_char(ch):
    codeval = ord(ch)
    if 0xFF00 <= codeval <= 0xFF5E:
        ascii = codeval - 0xFF00 + 0x20;
        return unichr(ascii)
    else:
        return ch


def convert_full_to_half_string(line):
    output_list = [convert_full_to_half_char(x) for x in line]
    return ''.join(output_list)


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
