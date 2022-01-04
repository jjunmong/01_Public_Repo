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

    outfile = codecs.open('prospecs_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@프로스펙스\n")

    page = 1
    while True:
        storeList = getStores(page, 'P')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'프로스펙스|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전국 점포정보 모두 얻을 수 있음
        #elif len(storeList) < 10: break

    time.sleep(random.uniform(0.3, 0.9))

    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@몽벨\n")

    page = 1
    while True:
        storeList = getStores(page, 'M')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'몽벨|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break  # 한번 호출로 전국 점포정보 모두 얻을 수 있음
        # elif len(storeList) < 10: break

    outfile.close()

def getStores(intPageNo, store_type):
    url = 'http://www.lsnmall.com'
    api = '/display.do?cmd=getStoreAjaxList'

    data = {
        'AREA_CD' : '',
        'AREA_DTL_CD': '',
        'CORNER_NM': '',
        #'TBRAND_CD': 'P',
    }
    data['TBRAND_CD'] = store_type
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        urls = url + api
        print(urls)     # for debugging
        #req = urllib2.Request(urls, params, headers=hdr)
        req = urllib2.Request(urls, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
        #result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    entity_list = tree.xpath('//div[@class="result_sc"]//ul[@class="text"]')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//li')
        if len(info_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '프로스펙스'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('(주)', '').rstrip().lstrip()
            if strtemp.startswith('몽벨'): strtemp = strtemp[2:].lstrip()

            if strtemp.endswith(']') or strtemp.endswith(')'): pass
            elif not strtemp.endswith('점'): strtemp += '점'

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = '';      store_info['ot'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find('/')
            if idx != -1:
                store_info['ot'] = strtemp[idx+1:].lstrip()
                strtemp = strtemp[:idx].rstrip()

            if strtemp.startswith('T.'): strtemp = strtemp[2:].lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = info_list[0].xpath('.//a/@data-x')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['xcoord'] = strtemp
        temp_list = info_list[0].xpath('.//a/@data-y')
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
