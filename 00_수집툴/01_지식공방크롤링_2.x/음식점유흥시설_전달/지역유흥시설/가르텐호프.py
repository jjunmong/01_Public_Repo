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

    outfile = codecs.open('gartenhof_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|OT@@가르텐비어\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['ot'])

        page += 1

        if page == 99: break
        elif len(store_list) < 16: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://garten22014.cafe24.com'
    api = '/_www/bbs/board.php'
    data = {
        'bo_table': 'sub04_01_02',
    }
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
    response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)
    #tree = html.fromstring('<head><meta charset="utf-8"/></head>' + response)

    entity_list = tree.xpath('//form[@class="board_list"]//table//tr')

    store_list = []
    for i in range(len(entity_list)):
        if i == 0: continue     # 첫번째 항목은 서식 정보 수록

        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 5: continue  # 최소 4개 필드 있어야 함

        store_info = {}
        store_info['name'] = '가르텐비어'

        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('가르텐비어'): strtemp = strtemp[5:].lstrip()
            if strtemp.startswith('가르텐'): strtemp = strtemp[3:].lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['addr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None: store_info['addr'] = strtemp.rstrip().lstrip()

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None: store_info['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')

        store_info['ot'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None: store_info['ot'] = strtemp.rstrip().lstrip()

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
