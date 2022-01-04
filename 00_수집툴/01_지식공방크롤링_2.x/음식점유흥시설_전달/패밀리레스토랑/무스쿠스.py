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

    outfile = codecs.open('muscus_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT@@무스쿠스\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['ot'])

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.muscus.com'
    api = '/home/page/'
    data = {
        'pid': 'shop1',
    }
    params = urllib.urlencode(data)
    # print(params)

    try:
        urls = url + api + '?' + params
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

    entity_list = tree.xpath('//div[@class="page-category-list"]//span//a')

    store_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('./@href')
        if len(temp_list) == 0: continue

        store_info = {}

        store_info['name'] = '무스쿠스'
        subname = entity_list[i].text
        if not subname.endswith('점'): continue      # 점포가 아닌 정보는 skip
        store_info['subname'] = subname.lstrip().rstrip().replace(' ', '/')

        time.sleep(random.uniform(0.3, 0.9))
        try:
            suburl = url + temp_list[0]
            print(suburl)  # for debugging
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');
            continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        addr_entity = subtree.xpath('//div[@class="storeInfo"]//p')
        pn_entity = subtree.xpath('//div[@class="call_program"]')
        ot_entity = subtree.xpath('//div[@class="storeInfo2"]//p')

        store_info['newaddr'] = ''
        strtemp = "".join(addr_entity[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('주소:', '').rstrip().lstrip()
            idx = strtemp.find('주소')
            if idx != -1:
                strtemp = strtemp[idx+2:].lstrip()
            if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
            idx = strtemp.find('☆')
            if idx != -1:
                strtemp = strtemp[:idx].rstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(pn_entity[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('예약문의', '').replace(':', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace('.', '-').replace('|', ';')

        store_info['ot'] = ''
        for j in range(len(ot_entity)):
            strtemp = "".join(ot_entity[j].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if store_info['ot'] != '': store_info['ot'] += ';'
                store_info['ot'] += strtemp

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
