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

sido_list = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list2 = {
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

    outfile = codecs.open('libsta4_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ETCADDR|TYPE|TYPE2|SINCE|WEBSITE@@기타도서관\n")

    page = 1
    while True:
        # 장애인 도서관
        requested_url = 'https://www.libsta.go.kr/libportal/libStats/etcLib/disabledLib/getDisabledLibPopAjax.do?gubun=STEP0000000001&libGubun=LIBTYPE004&dataYear='
        requested_url += '2016'     # 연도
        requested_url += '&searchKeyword=&sido=&siselect=&sigugunSi=&sigugunGugun=&fixYn=N&dhxr1531825572377=1'
        store_list = getStores(requested_url)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['etcaddr'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['type2'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s\n' % store['website'])

        # 전문 도서관
        requested_url = 'https://www.libsta.go.kr/libportal/libStats/etcLib/specialLib/getSpecialLibPopAjax.do?gubun=STEP0000000001&libGubun=LIBTYPE007&dataYear='
        requested_url += '2017'     # 연도
        requested_url += '&searchKeyword=&sido=&siselect=&sigugunSi=&sigugunGugun=&fixYn=N&foundation=&dhxr1531825917900=1'
        store_list = getStores2(requested_url)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['etcaddr'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['type2'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s\n' % store['website'])

        page += 1

        if page == 2: break     # 한 페이지에 정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(urls):
    try:
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = response.replace('<![CDATA[', '').replace(']]>', '')
    tree = html.fromstring(response)

    entity_list = tree.xpath('//row')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//cell')

        if len(info_list) < 4: continue

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['name'] = strtemp

        store_info['type'] = '장애인도서관'
        store_info['type2'] = ''

        store_info['since'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['since'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['newaddr'] += ' ' + strtemp

        store_info['pn'] = ''
        store_info['etcaddr'] = ''
        store_info['website'] = ''

        store_list += [store_info]

    return store_list

def getStores2(urls):
    try:
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = response.replace('<![CDATA[', '').replace(']]>', '')
    tree = html.fromstring(response)

    entity_list = tree.xpath('//row')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//cell')

        if len(info_list) < 8: continue

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['name'] = strtemp

        store_info['type'] = '전문도서관'

        store_info['type2'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['type2'] = strtemp

        store_info['since'] = ''
        strtemp = "".join(info_list[5].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['since'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[6].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[7].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(')', '-').replace(' ', '')

        store_info['etcaddr'] = ''
        store_info['website'] = ''

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
