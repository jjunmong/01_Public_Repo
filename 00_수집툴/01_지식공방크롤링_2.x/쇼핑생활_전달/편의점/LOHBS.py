# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import random
import codecs
import urllib
import random
import json
from lxml import html


sido_list2 = {      # 테스트용 시도 목록
    '서울특별시': '02',
}

sido_list = {
    '서울특별시': '02',
    '광주광역시': '062',
    '대구광역시': '053',
    '대전광역시': '042',
    '부산광역시': '051',
    '울산광역시': '052',
    '인천광역시': '032',
    '경기도': '031',
    '강원도': '033',
    '경상남도': '055',
    '경상북도': '054',
    '전라남도': '061',
    '전라북도': '063',
    '충청남도': '041',
    '충청북도': '043',
    '제주특별자치도': '064',
    '세종특별자치시': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('lohbs_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ID|NEWADDR@@롭스\n")

    # 현재는 한 페이지에 전국 점포 정보 다 있음
    for sido_name in sorted(sido_list):
        page = 1
        while True:
            storeList = getStores(sido_name)
            if len(storeList) == 0:
                break

            for store in storeList:
                outfile.write(u'롭스|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s\n' % store['newaddr'])

            page += 1

            if page == 2:
                break       # 한번 호출로 시도내 모든 결과값을 받을 수 있음

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/9)
def getStores(sido_name):
    url = 'https://m.lohbs.co.kr'
    api = '/cs/store/api/storeInfoListBrand'
    data = {}
    data['sido'] = sido_name
    params = urllib.urlencode(data)
    #print(params)

    try:
        #result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None


    response = result.read()
    entity_list = json.loads(response)
    #entity_list = response_json['resultSVO']['hesIcaCr91M00DVO']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '롭스'
        store_info['subname'] = entity_list[i]['storeName']
        store_info['newaddr'] = entity_list[i]['addr1']
        store_info['id'] = entity_list[i]['storeCode']
        store_info['pn'] = entity_list[i]['telNo']

        # 영업시간 정보도 있음

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
