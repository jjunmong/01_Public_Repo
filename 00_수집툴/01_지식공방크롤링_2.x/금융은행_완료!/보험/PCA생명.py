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
    '부산': '부산광역시',
}

sido_list = {
    '서울': '서울특별시',
    '광주': '광주광역시',
    '대구': '대구광역시',
    '대전': '대전광역시',
    '부산': '부산광역시',
    '울산': '울산광역시',
    '인천': '인천광역시',
    '경기': '경기도',
    '강원': '강원도',
    '경남': '경상남도',
    '경북': '경상북도',
    '전남': '전라남도',
    '전북': '전라북도',
    '충남': '충청남도',
    '충북': '충청북도',
    '제주': '제주특별자치도',
    '세종': '세종특별자치시'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('insurance_pcalife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|XCOORD|YCOORD@@PCA생명\n")

    page = 1
    while True:
        store_list = getStores(page)
        page += 1

        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        if page == 2: break     # 한번 호출로 전국 지점 정보 모두 얻을 수 있음

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.pcakorea.co.kr'
    api = '/corp/prudential_ko_kr/myprudential/branch/'
    data = {}
    #params = urllib.urlencode(data)
    #print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        req = urllib2.Request(url+api, None)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    nameinfo_list = tree.xpath('//div[@style="display: none" and @tabindex="0"]')
    entity_list = tree.xpath('//ul[@class="info"]')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//li')
        name_list = nameinfo_list[i].xpath('.//img/@alt')
        extrainfo_list = nameinfo_list[i].xpath('.//img/@src')
        if len(name_list) < 1 or len(info_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = 'PCA생명'

        store_info['subname'] = ''
        strtemp = name_list[0]
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('('):
                idx = strtemp.find(')')
                if idx != -1: strtemp = strtemp[idx+1:].lstrip()
            idx = strtemp.find('위치')
            if idx != -1: strtemp = strtemp[:idx].rstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
            if strtemp.startswith(')'): strtemp = strtemp[1:].lstrip()  # 주소 필드 기입 오류 수정
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('전화번호'): strtemp = strtemp[4:].lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        if len(extrainfo_list) > 0:
            # 'http://openapi.naver.com/map/getStaticMap?version=1.0&amp;uri=www.pcakorea.co.kr&amp;key=21edd90b1fd788f09629a3588cd6f923&amp;level=12&amp;w=198&amp;h=198&amp;exception=blank&amp;center=127.380314,36.359444&amp;markers=127.380314,36.359444
            strtemp = extrainfo_list[0]
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                idx = strtemp.rfind('markers=')
                if idx != -1:
                    temp_list = strtemp[idx+8:].split(',')
                    if len(temp_list) >= 2:
                        store_info['xcoord'] = temp_list[0].lstrip().rstrip()
                        store_info['ycoord'] = temp_list[0].lstrip().rstrip()

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
