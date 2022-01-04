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

sido_list2 = {      # 테스트용 시도 목록
    '강원': '033',
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

search_key_list = {
    '법무법인': '01',
    '사무소': '02',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('lawyer_firm_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|OFFICE|TELNUM|NEWADDR|MAJOR|BIRTH|STATUS|SOURCE2@@변호사\n")

    for search_key in sorted(search_key_list):
        page = 1
        retry_count = 0

        while True:
            store_list = getStores(search_key, page)
            if store_list == None:
                if retry_count > 3:
                    break
                else:
                    retry_count += 1
                    continue

            retry_count = 0

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['office'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['major'])
                outfile.write(u'%s|' % store['birth'])
                outfile.write(u'%s|' % store['status'])
                outfile.write(u'%s\n' % u'대한변호사협회')

            page += 1

            if page == 2999: break      # 서울 1652 page까지 있음
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(search_key, intPageNo):
    # 'http://koreanbar.or.kr/pages/search/search3.asp'
    url = 'http://koreanbar.or.kr'
    api = '/pages/search/search3.asp'
    data = {}
    data['lawtitle'] = search_key
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
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)     # 인코딩 정보가 반환값에 없어서...

    entity_list = tree.xpath('//div[@class="board_listW"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 5 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['status'] = ''

        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('(유한)', '').replace(',', ' ')\
                .replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').rstrip().lstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['major'] = ''
        store_info['birth'] = ''
        store_info['office'] = ''

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
