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
import requests
from lxml import html
import bs4

sido_list2 = {      # 테스트용 광역시도 목록
    '부산광역시': '051',
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

    outfile = codecs.open('citibank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@씨티은행\n")

    for sido_name in sido_list:

        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 199: break   # 2017년7월 기준 134개 지점 있음
            # elif len(store_list) < 3: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'https://www.citibank.co.kr'
    api = '/AtmSrch10.act'

    data = {
        'tab': '1',
        'search_flag': 'search',
        'ps': '3',
        'type': '',
        'idx': '',
        'chk_branch': 'on',
        'search_type': '1',
    }

    data['pg'] = intPageNo
    data['search_word'] = sido_name
    # data['search_word'] = ''
    params = urllib.urlencode(data)
    print(url, params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'cookie': 'WMONID=PHHxWigHAo1; delfino.recentModule=G3; JEX_LANG=KO; JEX_LOCAL_LANG=KO; s_pgb_product=%5B%5BB%5D%5D; s_fid=1BB8B7DB1F222A52-19495530BFF4CF52; s_nr=1579661673813-New; s_vnum=1580482800813%26vn%3D1; s_cc=true; JSESSIONID=0001t51mnE-3Lm3QZoIzfroQaOU:-1G2VQ80; JEX_UI_UUID_SND=26211ec4-d2f4-4ffe-89b6-5f16edcf7784; JEX_UI_UUID=0c28e72c-20d3-4ed0-a8ac-6c2074cde447'
    }

    try:
        urls = url + api
        req = requests.post(urls, data=data, headers=hdr).text
        # req.get_method = lambda: 'POST'
        # result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    # code = req.getcode()
    # if code != 200:
    #     print('HTTP request error (status %d)' % code);     return None
    html = bs4.BeautifulSoup(req, "html.parser")
    # response = result.read()
    # tree = html.fromstring(response)

    entity_list = html.xpath('//ul[@class="branchResult"]')
    print(entity_list)

    store_list = []
    for i in range(len(entity_list)):
        subname_list = entity_list[i].xpath('./a')
        info_list = entity_list[i].xpath('.//ul//textarea')
        pn_list = entity_list[i].xpath('./div')

        # if len(subname_list) < 1: continue

        store_info = {}

        store_info['name'] = '씨티은행'
        store_info['subname'] = ''
        strtemp = "".join(subname_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.endswith('(출)'):
                strtemp = strtemp[:-3].rstrip() + '출장소'
            elif strtemp.endswith('센터'):
                pass
            elif strtemp.endswith('본점'):
                pass
            elif not strtemp.endswith('지점'):
                strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['xcoord'] = '';
        store_info['ycoord'] = ''
        temp_list = subname_list[0].xpath('./@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                idx = strtemp.find('showLoc(')
                if idx != -1:
                    strtemp = strtemp[idx + 8:]
                    idx = strtemp.find(');')
                    strtemp = strtemp[:idx]
                    subinfo_list = strtemp.split(',')
                    if len(subinfo_list) >= 4:
                        store_info['xcoord'] = subinfo_list[2][1:-1]
                        store_info['ycoord'] = subinfo_list[3][1:-1]

                        if len(store_info['xcoord']) > 5:
                            store_info['xcoord'] = store_info['xcoord'][:3] + '.' + store_info['xcoord'][3:]
                        if len(store_info['ycoord']) > 5:
                            store_info['ycoord'] = store_info['ycoord'][:2] + '.' + store_info['ycoord'][2:]

        store_info['newaddr'] = ''
        if len(pn_list) > 0:
            strtemp = info_list[0].text
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        store_info['id'] = ''
        if len(info_list) > 0:
            strtemp = pn_list[0].text
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                idx = strtemp.find('|')
                if idx != -1: strtemp = strtemp[:idx].lstrip()
                strtemp = strtemp.replace('Tel.', '').lstrip().rstrip()
                store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

            temp_list = pn_list[0].xpath('.//a/@onclick')
            if len(temp_list) > 0:
                strtemp = temp_list[0]
                if strtemp != None:
                    strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                    idx = strtemp.find('showInfo(')
                    if idx != -1:
                        strtemp = strtemp[idx + 9:]
                        idx = strtemp.find(');')
                        strtemp = strtemp[:idx]
                        subinfo_list = strtemp.split(',')
                        if len(subinfo_list) >= 2:
                            store_info['id'] = subinfo_list[1][1:-1]

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
