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

sido_list2 = {      # 테스트용 시도 목록
    '부산': '051',
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

    outfile = codecs.open('wooribank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR\n")

    for sido_name in sido_list:

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

            if page == 99: break
            elif len(store_list) < 15: break

            time.sleep(random.uniform(0.3, 1.1))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'https://spib.wooribank.com'
    api = '/pib/jcc?withyou=CMCOM0153&__ID=c009291'
    data = {
        'search_tab': 0,
        'search_select': 1,
        'branch_kind': '',
        'branch_check': '',
        'search_range': 0,
        'search_range_for': '',
        'search_type': 'location',
        'result_type': 'location',
        'dong': '',
        'branch_name_giro': '',
        'branch_code_giro': '',
        'subway_name': '',
        'place_name': '',
        'pageno': 1,
        'search_string': '',
        'Total': 0,
        'flag': '',
        'code': '',
        'imgcode': 'brch',
        'PR_TYPE': '',
        'PR_CONTENTS': '',
    }
    data['PAGE_INDEX'] = intPageNo
    data['province'] = sido_name
    data['gungu'] = ''
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
        print(urls)     # for debugging
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
    tree = html.fromstring('<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>' + response + '</body></html>')

    entity_list = tree.xpath('//ul[@class="list-result-branch"]//li')
    subinfo_list = tree.xpath('//ul[@class="list-result-branch"]//script')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//span')
        if len(info_list) < 4: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = '우리은행'
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = convert_full_to_half_string(strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', ''))
            strtemp = strtemp.replace('　', ' ')     # 위 함수에서 '　' 문자는 제대로 못 바꿈 ㅠㅠ
            if strtemp.endswith('(출)'):
                strtemp = strtemp[:-3].rstrip() + '출장소'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = convert_full_to_half_string(strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', ''))
            store_info['newaddr'] = strtemp

        store_info['addr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = convert_full_to_half_string(strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', ''))
            if strtemp.startswith('[지번]'): strtemp = strtemp[4:].lstrip()
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = subinfo_list[i].text
        if strtemp != None:
            idx = strtemp.find('][4]')
            if idx != -1:
                strtemp = strtemp[idx:]
                idx = strtemp.find('"')
                strtemp = strtemp[idx+1:].lstrip()
                idx = strtemp.find('"')
                strtemp = strtemp[:idx].rstrip()
                idx = strtemp.find('(')     # 02-518-9317(9) 와 같은 경우 (9) 떼어내기
                if idx != -1: strtemp = strtemp[:idx].rstrip()
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
