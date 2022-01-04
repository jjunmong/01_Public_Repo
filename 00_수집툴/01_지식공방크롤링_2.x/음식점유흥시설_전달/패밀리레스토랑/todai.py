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

    outfile = codecs.open('todai_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@토다이\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'토다이|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 2: break     # 한 페이지에 다 있음
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.todaikorea.com'
    api = '/new/store/store_main.asp'
    data = {}
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    print(response)
    #response = unicode(response, 'euc-kr')
    #print(response)    # for debugging
    #tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    tree = html.fromstring('<head><meta charset="utf-8"/></head>' + response)

    entity_list = tree.xpath('//div[@class="store_s_list"]/dl/dd')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('./h3')
        info_list = entity_list[i].xpath('./p')

        if len(name_list) < 1 or len(info_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        subname = "".join(name_list[0].itertext()).strip('\r\t\n')
        store_info['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext()).strip('\r\t\n')
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('주소 :'): strtemp = strtemp[4:].lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[0].itertext()).strip('\r\t\n')
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('(지점:')
            if idx != -1:
                strtemp = strtemp[idx+4:-1].lstrip().rstrip()
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-')

        store_info['feat'] = ''
        feat_list = entity_list[i].xpath('./div/img/@alt')
        for j in range(len(feat_list)):
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_list[j]

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
