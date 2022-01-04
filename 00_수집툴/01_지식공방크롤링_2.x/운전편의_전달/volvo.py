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
import json
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

    outfile = codecs.open('volvo_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|WEBSITE\n")

    page = 1
    for page in range(1,12,1):
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['website'])

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://vckiframe.com'
    api = '/showroom'
    if intPageNo != 1: api += str(intPageNo)
    api += '.html'

    try:
        urls = url + api
        print(urls)
        req = urllib2.Request(urls, '')
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    #tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@id="wrap"]//section')

    store_list = []
    for i in range(len(entity_list)):
        name_list = entity_list[i].xpath('.//h5')
        info_list = entity_list[i].xpath('.//dl')
        if len(name_list) < 1: continue

        store_info = {}

        store_info['name'] = '볼보'
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            strtemp = strtemp.replace('(주)', '').replace('㈜', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = '';     store_info['pn'] = '';      store_info['website'] = ''

        for j in range(len(info_list)):
            tag_list = info_list[j].xpath('.//dt')
            value_list = info_list[j].xpath('.//dd')

            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            value = "".join(value_list[0].itertext())

            if tag == None or value == None: continue

            tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            if tag == '주소': store_info['newaddr'] = value
            elif tag == '홈페이지': store_info['website'] = value
            elif tag == '대표번호': store_info['pn'] = value.replace('.', '-').replace(')', '-')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
