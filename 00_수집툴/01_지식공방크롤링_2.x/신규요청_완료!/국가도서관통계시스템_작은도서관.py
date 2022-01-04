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

    outfile = codecs.open('libsta3_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ETCADDR|TYPE|SINCE|WEBSITE@@작은도서관\n")

    page = 1
    while True:
        requested_url = 'https://www.libsta.go.kr/libportal/libStats/smallLib/unitStats/getSmallUnitStatsPopAjax.do?gubun=STEP0000000001&dataYear='
        requested_url += '2016'     # 연도
        requested_url += '&searchKeyword=&sido=&siselect=%EC%A7%80%EC%97%AD%EA%B5%AC%EB%B6%84(%EC%A0%84%EA%B5%AD)&sigugunSi=&sigugunGugun=&foundation=&fixYn=N&libGubun=LIBTYPE003&dhxr1531825352805=1'
        store_list = getStores(requested_url)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['etcaddr'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s\n' % store['website'])

        page += 1

        if page == 2: break     # 한 페이지에 정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 1.1))

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

        if len(info_list) < 7: continue

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['name'] = strtemp

        store_info['type'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('<![CDATA[', '').replace(']]>', '').rstrip().lstrip()
            store_info['type'] = strtemp

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
        store_info['etcaddr'] = ''
        store_info['website'] = ''

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
