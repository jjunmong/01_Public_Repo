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
#import json
from lxml import html

sido_list2 = {      # 테스트용 시도 목록
    '서울': '02',
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

    outfile = codecs.open('church2_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|FEAT|SUBNAME|TELNUM|NEWADDR|FATHER|SOURCE2@@교회\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['father'])
            outfile.write(u'%s\n' % u'아멘선교회')

        page += 1

        if page == 2999: break      # 2018년9월 기준 1896까지 있음
        elif len(store_list) < 18: break
        elif len(store_list) < 20:
            print('%d : %d' % (page-1, len(store_list)))

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://amen.kr'
    api = '/bbs/board.php'
    data = {
        'bo_table': 'church',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)

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

    entity_list = tree.xpath('//div[@class="tbl_head01 tbl_wrap"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//h5')
        info_list = entity_list[i].xpath('.//td')
        if len(name_list) < 1 or len(info_list) < 1: continue

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '') \
                .replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').rstrip().lstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['type'] = ''
        store_info['father'] = ''
        store_info['newaddr'] = ''
        store_info['pn'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.rfind('전화')
            if idx != -1:
                strtail = strtemp[idx+2:].lstrip()
                if strtail.startswith(':'): strtail = strtail[1:].lstrip()
                store_info['pn'] = strtail.replace('.', '-').replace(')', '-').replace(' ', '')
                strtemp = strtemp[:idx].rstrip()

            idx = strtemp.rfind('주소')
            if idx != -1:
                strtail = strtemp[idx+2:].lstrip()
                if strtail.startswith(':'): strtail = strtail[1:].lstrip()
                store_info['newaddr'] = strtail
                strtemp = strtemp[:idx].rstrip()

            idx = strtemp.rfind('교단')
            if idx != -1:
                strtail = strtemp[idx+2:].lstrip()
                if strtail.startswith(':'): strtail = strtail[1:].lstrip()
                store_info['type'] = strtail
                strtemp = strtemp[:idx].rstrip()

            idx = strtemp.rfind('담임목사')
            if idx != -1:
                strtail = strtemp[idx+4:].lstrip()
                if strtail.startswith(':'): strtail = strtail[1:].lstrip()
                store_info['father'] = strtail

            # 상세 페이지에 좌표 정보도 있음

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
