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

    outfile = codecs.open('kovea_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@코베아\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'코베아|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 19: break
        elif len(storeList) < 12: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.koveashop.co.kr'
    api = '/board/board.html'
    data = {
        'code': 'kovea1_board4',
        'board_cate': '',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)

    try:
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
    entity_list = tree.xpath('//div[@class="bbs-table-list"]//tbody//tr//dl')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//dd')
        if len(info_list) < 4: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '코베아'

        store_info['subname'] = ''
        store_info['type'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('['):
                strtemp = strtemp[1:].lstrip()
                idx = strtemp.find(']')
                if idx != -1:
                    strtemp = strtemp[idx+1:].lstrip()

            if strtemp.startswith('코베아'): strtemp = strtemp[3:].lstrip()

            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
