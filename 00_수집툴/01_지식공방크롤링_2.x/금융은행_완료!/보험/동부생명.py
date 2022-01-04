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

    outfile = codecs.open('insurance_donbulife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR@@동부생명\n")

    # 지점
    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores(page)
        page += 1

        if store_list == None: break;
        elif len(store_list) > 0:
            if store_list[0]['id'] ==  sentinel_store_id: break
            elif store_list[0]['id'] != '': sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        if page == 49: break
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.idblife.com'
    api = '/support/branch/index'
    data = {
        '_csrf': 'c1edb16b-8452-4630-81b7-b791356c14cf',
        'pageRecordCount': '5',
        'page': '1',
        'org_seq':'',
        'workCode':'',
        'regionCode':'',
        }
    data['page'] = intPageNo
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
        req = urllib2.Request(url+api, params, headers=hdr)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//div[@class="sch_body"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '동부생명'

        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['type'] = ''
        temp_list = info_list[0].xpath('.//img/@alt')
        if len(temp_list) > 0:
            store_info['type'] = temp_list[0]

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = info_list[4].xpath('.//a/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('getMap(')
            if idx != -1:
                strtemp = strtemp[idx+7:].lstrip()
                idx = strtemp.find(');')
                temp_list = strtemp[:idx].split(',')
                if len(temp_list) >= 2:
                    store_info['id'] = temp_list[1].lstrip().rstrip()[1:-1]

        # 상세정보 페이지에 좌표정보 있음 (필요할 때 추출할 것!)

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
