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

    outfile = codecs.open('insurance_metlife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR@@메트라이프생명\n")

    for i in range(1, 12):  # 서울=1, 제주도=11 (2017년9월 기준)
        page = 1
        while True:
            store_list = getStores(i, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s\n' % store['newaddr'])

            page += 1
            if page == 49: break
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.7))

        time.sleep(random.uniform(0.3, 0.7))

    outfile.close()


def getStores(area_code, page_no):
    url = 'https://brand.metlife.co.kr'
    api = '/cc/custCetr/searchBrn.do'
    data = {
        'brnId': '',
        'isAem': 'isAem:true',
        #'arCd': '1',
        'searchCondition2': '',
        'searchKeyword': '',
    }
    data['arCd'] = area_code
    data['pageIndex'] = page_no
    params = urllib.urlencode(data)
    print(params)

    try:
        req = urllib2.Request(url + api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
        #result = urllib.urlopen(url+api)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    tree = html.fromstring(response)
    entity_list = tree.xpath('//ul[@class="boardList"]//li')

    store_list = []
    for i in range(len(entity_list)):
        name_list = entity_list[i].xpath('.//strong')
        if len(name_list) < 1: continue

        strtemp = "".join(entity_list[i].itertext())
        if strtemp == None: continue

        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

        store_info = {}
        store_info['name'] = '메트라이프생명'

        store_info['subname'] = ''
        subname = "".join(name_list[0].itertext())
        if subname != None:
            subname = subname.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = subname.replace(' ', '/')
            idx = strtemp.find(subname)
            if idx != -1:
                strtemp = strtemp[idx+len(subname):].lstrip()

        store_info['newaddr'] = ''
        idx = strtemp.find('전화')
        if idx != -1:
            store_info['newaddr'] = strtemp[:idx].rstrip()
            strtemp = strtemp[idx+2:].lstrip()
            if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()

        store_info['pn'] = ''
        idx = strtemp.find('FAX')
        if idx != -1:
            store_info['pn'] = strtemp[:idx].rstrip().replace(' ', '').replace(')', '-').replace('.', '-')
        else:
            idx = strtemp.find('팩스')
            if idx != -1:
                store_info['pn'] = strtemp[:idx].rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = entity_list[i].xpath('.//span/a/@onclick')
        if len(temp_list) > 0:
            strtemp2 = temp_list[0]
            idx = strtemp2.find('mapPopUp(')
            if idx != -1:
                strtemp2 = strtemp2[idx+9:]
                idx = strtemp2.find(');')
                if idx != -1:
                    store_info['id'] = strtemp2[:idx][1:-1]

        store_list += [store_info]

    # 고객플라자 정보 추출
    if area_code == 1 and page_no == 1:
        plazaname_list = tree.xpath('//div[@class="plazaInfo"]//dl//dt')
        plazaaddr_list = tree.xpath('//div[@class="plazaInfo"]//dl//dd')

        for i in range(len(plazaname_list)):
            plazaname = plazaname_list[i].text
            plazaaddr = plazaaddr_list[i].text
            if plazaname == None or plazaaddr == None: continue

            plazaname = plazaname.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            plazaaddr = plazaaddr.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if not plazaname.endswith('플라자'): continue

            store_info = {}
            store_info['name'] = '메트라이프생명'

            store_info['subname'] = plazaname.replace(' ', '/')
            store_info['newaddr'] = plazaaddr
            store_info['pn'] = ''
            store_info['id'] = ''

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
