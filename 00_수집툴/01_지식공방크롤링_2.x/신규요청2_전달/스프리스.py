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

    outfile = codecs.open('spris_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@스프리스\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전국 점포정보 모두 얻을 수 있음
        #elif len(storeList) < 10: break

        #time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0
def getStores(intPageNo):
    'https://www.spris.com'
    url = 'http://spris.w-gens.com/'
    api = '/ASP/Company/StoreList.asp'
    #data = {}
    #params = urllib.urlencode(data)

    try:
        urls = url + api
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
    entity_list = tree.xpath('//ul[@id="mapLocation"]//li')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//dl//dd')
        if len(info_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '스프리스'

        store_info['id'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find('스프리스')
            if idx != -1:
                store_info['id'] = strtemp[:idx].rstrip()
                strtemp = strtemp[idx+4:].lstrip()

            idx = strtemp.find('레스모아')
            if idx != -1:
                store_info['id'] = strtemp[:idx].rstrip()
                strtemp = strtemp[idx+4:].lstrip()
                store_info['name'] = '레스모아'

            idx = strtemp.find('넥스텝')
            if idx != -1:
                store_info['id'] = strtemp[:idx].rstrip()
                strtemp = strtemp[idx+3:].lstrip()
                store_info['name'] = '넥스텝'


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

        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = entity_list[i].xpath('./@data-xpoint')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['xcoord'] = strtemp
        temp_list = entity_list[i].xpath('./@data-ypoint')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['ycoord'] = strtemp

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
