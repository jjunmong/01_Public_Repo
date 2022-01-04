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

    outfile = codecs.open('smalllibrary_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@작은도서관\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 999: break     # 2018년 7월 기준 6491곳 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://www.smalllibrary.org/library/index?&searchSido=&searchGugun=&searchLibraryName=&currentPage=7'
    url = 'http://www.smalllibrary.org'
    api = '/library/index'
    data = {}
    params = '&searchSido=&searchGugun=&searchLibraryName=&currentPage=' + str(intPageNo)
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

    entity_list = tree.xpath('//table[@class="table table-location"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//td//a')
        addr_list = entity_list[i].xpath('.//div[@class="location"]')
        info_list = entity_list[i].xpath('.//td')

        if len(name_list) < 1: continue

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.endswith('문고') or strtemp.find('문고') != -1: pass
            elif strtemp.endswith('책방') or strtemp.find('책방') != -1: pass
            elif strtemp.endswith('북카페') or strtemp.find('북카페') != -1: pass
            elif not strtemp.endswith('도서관') and strtemp.find('도서관') == -1: strtemp += ' 작은도서관'
            #store_info['name'] = strtemp.replace(' ', '/')
            store_info['name'] = strtemp

        store_info['newaddr'] = ''
        if len(addr_list) > 0:
            strtemp = "".join(addr_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        if len(info_list) >= 2:
            strtemp = "".join(info_list[1].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('연락처'): strtemp = strtemp[3:].lstrip()
                if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                store_info['pn'] = strtemp

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
