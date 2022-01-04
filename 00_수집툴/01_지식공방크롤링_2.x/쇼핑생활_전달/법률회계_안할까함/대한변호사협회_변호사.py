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

sido_list2 = {
    '서울': '02',
}

sido_list = {      # 테스트용 시도 목록
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

    outfile = codecs.open('lawyer2_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|OFFICE|TELNUM|NEWADDR|MAJOR|BIRTH|STATUS|SOURCE2@@변호사\n")

    for sido_name in sorted(sido_list):
        page = 1
        retry_count = 0

        while True:
            store_list = getStores(sido_name, page)
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

def getStores(sido_name, intPageNo):
    # 'http://koreanbar.or.kr/pages/search/search.asp'
    url = 'http://koreanbar.or.kr'
    api = '/pages/search/search.asp'
    data = {
        'gun1': '',
        'dong1': '',
        'special1_1': '',
        'special1': '',
        'searchtype': 'mname',
        'searchstr': '',
    }
    data['sido1'] = sido_name
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
        if len(info_list) < 7: continue  # 최소 7개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['status'] = ''

        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            if strtemp.find('휴업') != -1:
                store_info['status'] = '휴업'
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('보기', '').replace('휴업', '').rstrip().lstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['major'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['major'] = strtemp

        store_info['birth'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['birth'] = strtemp

        store_info['office'] = ''
        strtemp = "".join(info_list[5].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['office'] = strtemp

        store_info['newaddr'] = ''
        store_info['pn'] = ''
        strtemp = "".join(info_list[6].itertext())
        strtemp2 = info_list[6].text
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.rfind(' ')
            if idx != -1 and strtemp[idx+1:idx+2] == '0':
                store_info['newaddr'] = strtemp[:idx].rstrip()
                store_info['pn'] = strtemp[idx+1:].lstrip()
            else:
                store_info['newaddr'] = strtemp

        # suburl에서 상세정보도 얻을 수 있음 (시험기수, 생년월일, 이메일 ...)

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
