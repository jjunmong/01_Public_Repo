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

    outfile = codecs.open('cleantopia_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|FEAT|XCOORD|YCOORD@@크린토피아\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 999: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.cleantopia.com'
    api = '/kr/store/storeList.do'
    data = {
        'totalpage': '',
        'searchType': '',
        'searchKeyword': '',
    }
    data['pageIndex'] = intPageNo
    params = urllib.urlencode(data)
    print(params)   # for debugging

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@id="storeList"]//div[@class="item"]')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//span[@class="name"]')
        info_list = entity_list[i].xpath('.//span[@class="addr"]//em')

        if len(name_list) < 1 or len(info_list) < 2: continue

        store_info = {}

        store_info['name'] = '크린토피아'

        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('코인워시'):
                strtemp = strtemp[4:].lstrip()
                store_info['name'] = '코인워시'
            if strtemp.endswith(')'): strtemp = strtemp[:-1].rstrip().replace('(', '/')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['feat'] = ''
        feat_list = entity_list[i].xpath('.//span[@class="blt"]//img/@alt')
        for j in range(len(feat_list)):
            feat_item = feat_list[j]
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_item

        store_info['id'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        temp_list = entity_list[i].xpath('.//a/@onclick')
        for j in range(len(temp_list)):
            strtemp = temp_list[j]
            if strtemp == None: continue
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            idx = strtemp.find('goMapCenter(')
            if idx != -1:
                strtemp = strtemp[idx+12:].lstrip()
                idx = strtemp.find(');')
                coord_list = strtemp[:idx].split(',')
                if len(coord_list) >= 2:
                    store_info['xcoord'] = coord_list[1].lstrip().rstrip()[1:-1]
                    store_info['ycoord'] = coord_list[0].lstrip().rstrip()[1:-1]
            else:
                idx = strtemp.find('goStoreInfo(')
                if idx != -1:
                    strtemp = strtemp[idx+12:].lstrip()
                    idx = strtemp.find(')')
                    store_info['id'] = strtemp[:idx].lstrip().rstrip()[1:-1]

        # 상세정보 페이지에 영업시간 정보 있음 (필요할 때 추출할 것!!)

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
