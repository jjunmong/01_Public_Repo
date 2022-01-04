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

    outfile = codecs.open('angelinus_utf8_pp.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|FEAT@@엔제리너스\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'엔제리너스커피|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 999: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.angelinus.com'
    api = '/Shop/Shop_Ajax.asp'
    data = {
        'PageSize' : 10,
        'BlockSize': 10,
        'SearchArea1': '',
        'SearchArea2': '',
        'SearchType': 'TEXT',
        'SearchText': '',
        'SearchIs24H': 0,
        'SearchIsUmbrella': 0,
        'SearchIsParking': 0,
        'SearchIsEvent': 0,
        'SearchIsNewOpen': 0,
        'SearchIsWifi': 0,
        'SearchIsPC': 0,
        'SearchIsMeetingRoom': 0,
        'SearchIsSmokingRoom': 0,
        'SearchIsCatering': 0,

    }
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
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//table[@class="list"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')

        if info_list == None: continue;  # for safety
        elif len(info_list) < 4: continue  # 4개 필드 있음

        store_info = {}
        subname = "".join(info_list[1].itertext()).strip('\r\t\n')
        store_info['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        store_info['pn'] = '';
        strtemp = "".join(info_list[3].itertext()).strip('\r\t\n')
        if strtemp != None: store_info['pn'] = strtemp.rstrip().lstrip().replace(',', '-').replace(')', '-')

        store_info['feat'] = ''
        feat_list = info_list[2].xpath('.//img/@alt')
        for j in range(len(feat_list)):
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_list[j]

        store_info['newaddr'] = '';      store_info['ot'] = ''

        temp_list = info_list[1].xpath('./a/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0].lstrip().rstrip()
            idx = strtemp.find('goView(')
            strtemp = strtemp[idx+7:-1]
            id_list = strtemp.split(',')
            shop_id1 = id_list[0]
            shop_id2 = id_list[1][1:-1]

            subdata = {
                'SearchAreaSi': '',
                'SearchAreaGn': '',
                'SearchText': '',
                'Mode': '',
                'PageSize': 10,
                'BlockSize': 10,
                'SearchType': '',
                'SearchIs24H': 0,
                'SearchIsUmbrella': 0,
                'SearchIsParking': 0,
                'SearchIsEvent': 0,
                'SearchIsNewOpen': 0,
                'SearchIsWifi': 0,
                'SearchIsPC': 0,
                'SearchIsMeetingRoom': 0,
                'SearchIsSmokingRoom': 0,
                'SearchIsCatering': 0,
                'SearchAreaSi_N': '',
                'SearchAreaGn_N': '',
            }
            subdata['Page'] = intPageNo
            subdata['Idx'] = shop_id1
            subdata['StoreCode'] = shop_id2
            subparams = urllib.urlencode(subdata)

            subapi = '/Shop/Shop_View.asp'

            time.sleep(random.uniform(0.3, 0.9))
            try:
                suburl = url + subapi + '?' + subparams
                print(suburl)  # for debugging
                subresult = urllib.urlopen(suburl)
            except:
                print('Error calling the suburl');
                store_list += [store_info]
                continue

            code = subresult.getcode()
            if code != 200:
                print('suburl HTTP request error (status %d)' % code);
                store_list += [store_info]
                continue

            subresponse = subresult.read()
            # print(response)
            subtree = html.fromstring(subresponse)

            subinfo_list = subtree.xpath('//table[@class="data_row2"]//tbody//tr')

            if len(subinfo_list) < 3:  # 최소 3개 필드 있어야 함
                store_list += [store_info]
                continue

            strtemp = "".join(subinfo_list[0].itertext())
            store_info['newaddr'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            strtemp = "".join(subinfo_list[2].itertext())
            store_info['ot'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
