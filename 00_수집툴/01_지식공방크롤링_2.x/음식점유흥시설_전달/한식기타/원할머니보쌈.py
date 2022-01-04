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

    outfile = codecs.open('wonandone_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ADDR@@원할머니보쌈\n")

    for sido_name in sido_list:
        page = 1
        while True:
            storeList = getStores(sido_name)
            if len(storeList) == 0:
                break

            for store in storeList:
                outfile.write(u'원할머니보쌈|')
                outfile.write(u'%s|' % store['store_nm'].replace(' ', '/'))
                outfile.write(u'%s|' % store['store_phone'])
                newaddress = store['store_addr1'] + ' ' + store['store_addr2'] + ' ' + store['store_addr4']
                newaddress = newaddress.rstrip().lstrip()
                outfile.write(u'%s|' % newaddress)
                address = store['store_addr1'] + ' ' + store['store_addr2'] + ' ' + store['store_addr3']
                address = address.rstrip().lstrip()
                outfile.write(u'%s\n' % address)

                # 상세정보는 필요할 때 추출할 것!!!

            page += 1

            if page == 2:
                break

    outfile.close()

def getStores(strSidoName):
    url = 'http://bossam.co.kr'
    api = '/wordpress/wp-content/plugins/owl-dbms/interlock/bossam_store_json.php'
    data = {
        'site_gubun': 'w',
        'store_addr2': '',
        'bossamchk': 'N',
        'bossamcompchk': 'N',
        'bossamworldchk': 'N',
        'kuksuchk': 'N',
        'gunchk': 'N',
        'banchk': 'N',
        'deliverychk': 'N',
        'childrenroomchk': 'N',
        'dosirakchk': 'N',
        'mobile_coupon': 'N',
        'ordering': ''
    }
    data['store_addr1'] = strSidoName
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

#    result_encoding = result.headers.getparam('charset')
#    # response = result.read()
#    response = result.read().decode(result_encoding)  # 이렇게 해도 한글이 깨짐 (이유 모르겠음 ㅠㅠ)

    response = result.read()
    response = response.replace('\\"', '"').strip('\r\t\n').rstrip().lstrip()
    if response.startswith('"'): response = response[1:]
    if response.endswith('"'): response = response[:len(response)-1]

    receivedData = json.loads(response)  # json 포맷으로 결과값 반환

    #storeList = receivedData
    if receivedData.get('data'): storeList = receivedData['data']
    else: storeList = []

    time.sleep(random.uniform(0.3, 1.1))
    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
