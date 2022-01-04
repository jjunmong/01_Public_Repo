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
import ast
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

    outfile = codecs.open('cadillac_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|SUBNAME2|XCOORD|YCOORD\n")

    for page in range(1,16,1):
        store_list = getStores(page)
        if store_list == None: continue

        for store in store_list:

            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['subname2'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.cadillac.co.kr'
    api = '/shopping/showroom.php'
    data = {}
    data['idx'] = intPageNo
    params = urllib.urlencode(data)
    # print(params)

    try:
        urls = url + api
        print(urls)
        req = urllib2.Request(urls, params)
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

    entity_list = tree.xpath('//label')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//input/@onclick')
        if len(info_list) < 1: continue

        strtemp = info_list[0]      # 'newMarker('35.856026','127.068501'); dealer_address(28);'
        idx = strtemp.find('address(')
        shop_id = strtemp[idx+8:]
        idx = shop_id.find(')')
        shop_id = shop_id[:idx]

        idx = strtemp.find('newMarker(')
        strtemp = strtemp[idx+10:]
        idx = strtemp.find(')')
        temp_list = strtemp[:idx].split(',')
        xcoord = temp_list[1][1:-1]
        ycoord = temp_list[0][1:-1]

        subdata = {}
        subdata['idx'] = shop_id
        subparams = urllib.urlencode(subdata)

        try:
            suburls = url + '/include/dealer_address.php'
            print(suburls)
            subreq = urllib2.Request(suburls, subparams)
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the sub API');     continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);     continue

        subresponse = subresult.read()
        #print(subresponse)
        #subtree = html.fromstring(subresponse)
        subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + subresponse)

        name_list = subtree.xpath('.//div[@class="title2"]')
        info_list = subtree.xpath('.//span')
        if len(name_list) < 1: continue

        store_info = {}

        store_info['name'] = '캐딜락'
        store_info['subname'] = '';     store_info['subname2'] = ''
        store_info['newaddr'] = '';     store_info['pn'] = ''
        store_info['xcoord'] = xcoord;  store_info['ycoord'] = ycoord
        strtemp = name_list[0].text
        if strtemp != None:
            idx = strtemp.find('(')
            if idx != -1:
                store_info['subname2'] = strtemp[:idx].rstrip().replace(' ', '/')
                strtemp = strtemp[idx+1:]
                idx = strtemp.find(')')
                strtemp = strtemp[:idx].rstrip()
                store_info['subname'] = strtemp.replace(' ', '/')

        for j in range(len(info_list)):
            info_item = info_list[j]
            key = info_item.text
            value = info_item.tail

            if key == None or value == None: continue
            key = key.lstrip().rstrip()
            value = value.lstrip().rstrip()
            if value.startswith(':'): value = value[1:].lstrip()

            if key == '주소': store_info['newaddr'] = value
            elif key == '전화': store_info['pn'] = value.replace('(', '').replace(' ', '').replace(')', '-').replace('.', '-')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
