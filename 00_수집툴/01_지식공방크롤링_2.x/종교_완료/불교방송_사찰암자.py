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

    outfile = codecs.open('temple_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|TYPE|SUBNAME|TELNUM|NEWADDR|SOURCE2|XCOORD|YCOORD@@사찰\n")

    outfile2 = codecs.open('temple_small_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|TYPE|SUBNAME|TELNUM|NEWADDR|SOURCE2|XCOORD|YCOORD@@암자\n")


    for sido_name in sorted(sido_list):
        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                if store['name'].endswith('암'):
                    outfile2.write(u'%s|' % store['name'])
                    outfile2.write(u'%s|' % store['type'])
                    outfile2.write(u'%s|' % store['subname'])
                    outfile2.write(u'%s|' % store['pn'])
                    outfile2.write(u'%s|' % store['newaddr'])
                    outfile2.write(u'%s|' % u'불교방송')
                    outfile2.write(u'%s|' % store['xcoord'])
                    outfile2.write(u'%s\n' % store['ycoord'])
                else:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['type'])
                    outfile.write(u'%s|' % store['subname'])
                    outfile.write(u'%s|' % store['pn'])
                    outfile.write(u'%s|' % store['newaddr'])
                    outfile.write(u'%s|' % u'불교방송')
                    outfile.write(u'%s|' % store['xcoord'])
                    outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 99: break
            elif len(store_list) < 50: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()
    outfile2.close()

def getStores(sido_name, intPageNo):
    # 'http://s.bbsi.co.kr/search/search_search_list.asp?areaCd=CTLQ&strArea1=%EC%84%9C%EC%9A%B8&strArea2=%EB%A7%88%ED%8F%AC%EA%B5%AC'
    #url = 'http://www.bbsi.co.kr'
    url = 'http://s.bbsi.co.kr'
    api = '/search/search_search_list.asp'
    data = {
        'areaCd': 'XEVB',
        #'strArea1': '',
        'strArea2': '',
        'sNum': '',
    }
    data['strArea1'] = sido_name
    data['Page'] = intPageNo
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

    entity_list = tree.xpath('//div[@class="wrapList"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//div[@class="subject"]')
        info_list = entity_list[i].xpath('.//div[@class="info"]')
        etc_list = entity_list[i].xpath('.//a/@href')

        if len(name_list) < 1: continue

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['type'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith(')'):
                idx = strtemp.rfind('(')
                if idx > 0:
                    store_info['type'] = strtemp[idx+1:-1].lstrip().rstrip()
                    strtemp = strtemp[:idx].rstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        store_info['pn'] = ''

        if len(info_list) > 0:
            strtemp = "".join(info_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                idx = strtemp.find('(0')
                if idx != -1:
                    store_info['newaddr'] = strtemp[:idx].rstrip()
                    store_info['pn'] = strtemp[idx+1:].replace('.', '-').replace(')', '-').replace(' ', '-')
                else: store_info['newaddr'] = strtemp

            if store_info['newaddr'].find(sido_name) != 0:
                store_info['newaddr'] = sido_name + ' ' + store_info['newaddr']

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if len(etc_list) > 0:
            strtemp = etc_list[0]
            idx = strtemp.find('clickPopup(')
            if idx != -1:
                temp_list = strtemp[idx+11:-2].lstrip().rstrip().split(',')
                if len(temp_list) >= 3:
                    store_info['xcoord'] = temp_list[2].replace('\'', '').lstrip().rstrip()
                    store_info['ycoord'] = temp_list[1].replace('\'', '').lstrip().rstrip()

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
