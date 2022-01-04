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


sido_list2 = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list = {
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

    outfile = codecs.open('domino_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|PARKING|ID|XCOORD|YCOORD@@도미노피자\n")

    for idx in range(len(sido_list)):
        sub_district_list = getSubDistrictInfo(idx)

        for district_code in sorted(sub_district_list):

            storeList = getStores(district_code)
            if storeList == None: break
            elif len(storeList) == 0:
                break

            for store in storeList:
                outfile.write(u'도미노피자|')
                outfile.write(u'%s|' % store['branch_name'].replace(' ', '/'))
                outfile.write(u'%s|' % store['tel'])

                store_addr = store['addr_ba'] + ' ' + store['addr_de']
                outfile.write(u'%s|' % store_addr)
                store_newaddr = store['road_addr_ba'] + ' ' + store['road_addr_de']
                outfile.write(u'%s|' % store_newaddr)

                store_ot = store['trade_start'] + '~' + store['trade_end']
                outfile.write(u'%s|' % store_ot)

                store_parking = store['parking']
                if store_parking != None:
                    store_parking = store_parking.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                outfile.write(u'%s|' % store_parking)
                outfile.write(u'%s|' % store['branch_code'])
                outfile.write(u'%s|' % store['gmapy'])
                outfile.write(u'%s\n' % store['gmapx'])

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()


def getStores(district_code):
    url = 'https://web.dominos.co.kr'
    api = '/branch/listAjax'
    data = {
        'region_code_2': ''
    }
    data['region_code_2'] = district_code
    #data['pageNo'] = 1
    params = urllib.urlencode(data)
    # print(params)

    try:
        #result = urllib.urlopen(url + api, params)

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
    response_json = json.loads(response)
    store_list = response_json['resultData']['branchList']

    return store_list

def getSubDistrictInfo(idx):
    idx += 1;
    url = 'https://web.dominos.co.kr/branch/regionSubListAjax?region_code_1='
    if idx < 10: url += '0' + str(idx)
    else: url += str(idx)

    try:
        print(url)     # for debugging
        result = urllib.urlopen(url)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['resultData']

    district_list = []
    for i in range(len(entity_list)):
        district_list.append(entity_list[i]['region_code_2'])

    return district_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
