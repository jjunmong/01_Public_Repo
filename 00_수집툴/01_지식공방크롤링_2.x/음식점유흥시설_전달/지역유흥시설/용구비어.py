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

    outfile = codecs.open('yonggu_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@용구비어\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(store_list) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://www.yonggu.co.kr/bbs/board.php?bo_table=openshop&&page=3
    url = 'http://www.yonggu.co.kr'
    api = '/bbs/board.php'
    data = {
        'bo_table': 'openshop',
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
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@class="table table-hover"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = '용구비어'
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('['):     # '[강원도]  삼척점'에서 '[강원도]' 제거
                idx = strtemp.find(']')
                if idx != -1:
                    strtemp = strtemp[idx+1:].lstrip()

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['id'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['ot'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        temp_list = info_list[1].xpath('.//a/@href')
        if len(temp_list) < 2:
            store_list += [store_info];     continue

        suburls = temp_list[1].lstrip().rstrip()

        try:
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 1.1))
            subresult = urllib.urlopen(suburls)
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

        xinfo_list = subtree.xpath('//div[@class="map-content-wrap"]/@data-map-x')
        yinfo_list = subtree.xpath('//div[@class="map-content-wrap"]/@data-map-y')

        if len(xinfo_list) > 0: store_info['xcoord'] = xinfo_list[0]
        if len(yinfo_list) > 0: store_info['ycoord'] = yinfo_list[0]

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
