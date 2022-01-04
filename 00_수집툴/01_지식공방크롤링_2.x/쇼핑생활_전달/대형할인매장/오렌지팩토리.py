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

    outfile = codecs.open('orangefactory_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|MTYPE|XCOORD|YCOORD@@오렌지팩토리\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % u'아울렛')
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(store_list) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://www.orangefactory.com/bbs/board.php?bo_table=orange_office&page=2&page=3'
    url = 'http://www.orangefactory.com'
    api = '/bbs/board.php'
    data = {
        'bo_table': 'orange_office',
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

    entity_list = tree.xpath('//div[@class="search-list-wrap"]//table//tr')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//th')
        info_list = entity_list[i].xpath('.//td')
        if len(name_list) < 1 or len(info_list) < 1: continue

        store_info = {}

        store_info['name'] = '오렌지팩토리'
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['addr'] = '' ;    store_info['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        temp_list = name_list[0].xpath('.//a/@href')
        if len(temp_list) < 1:
            store_list += [store_info]
            continue

        subapi = temp_list[0]
        if subapi.startswith('..'): subapi = subapi[2:]

        suburl = url + subapi
        print(suburl)  # for debugging

        try:
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="office-information"]//p')

        for j in range(len(subinfo_list)):
            strtemp = "".join(subinfo_list[j].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if strtemp.startswith('전화번호'):
                    strtemp = strtemp[4:].lstrip()
                    if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                    store_info['pn'] = strtemp

        idx = subresponse.find('function(){initialize(')
        if idx != -1:
            strtemp = subresponse[idx+22:]
            idx = strtemp.find(')}')
            if idx != -1:
                temp_list = strtemp[:idx].replace('"', '').split(',')
                if len(temp_list) == 2:
                    store_info['xcoord'] = temp_list[1].lstrip().rstrip()
                    store_info['ycoord'] = temp_list[0].lstrip().rstrip()

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
