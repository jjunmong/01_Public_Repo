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

    outfile = codecs.open('zzimzilbang_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|SOURCE2|MTYPE@@찜질방\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % u'찜질방닷컴')
            outfile.write(u'%s\n' % u'찜질방')

        page += 1

        if page == 499: break       # 2018년6월 기준 page 182까지 (찜질방 2179곳 있음)
        elif len(store_list) < 12: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'https://zzimzilbang.com/search/search.html?page=3&sido_var=%EC%84%9C%EC%9A%B8'
    url = 'http://zzimzilbang.com'
    api = '/search/search.html'
    data = {
        'sido_var': '',
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="shre_list"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//div')
        if len(info_list) < 1: continue

        temp_list = info_list[0].xpath('.//a/@href')
        if len(temp_list) < 1: continue

        subapi = temp_list[0]
        if subapi.startswith('..'): subapi = subapi[2:]
        suburl = url + subapi
        print(suburl)  # for debugging

        try:
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        name_list = subtree.xpath('//div[@class="home_info"]//h2')
        subinfo_list = subtree.xpath('//div[@class="txt_wrap"]//ul//dl//dd')

        if len(name_list) < 1 or len(subinfo_list) < 2: continue

        store_info = {}

        store_info['name'] = name_list[0].text or ''
        store_info['name'] = store_info['name'].lstrip().rstrip()
        #store_info['name'] = store_info['name'].lstrip().rstrip().replace(' ', '/')
        store_info['subname'] = ''

        store_info['addr'] = ''
        store_info['pn'] = ''

        #strtemp = "".join(subinfo_list[0].itertext())
        strtemp = subinfo_list[0].text or ''
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['addr'] = strtemp

        #strtemp = "".join(subinfo_list[1].itertext())
        strtemp = subinfo_list[1].text or ''
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
