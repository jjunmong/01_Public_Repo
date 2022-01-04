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
from lxml import html

sido_list2 = {      # 테스트용 광역시도 목록
    '부산': '부산광역시',
}

sido_list = {
    '서울': '서울특별시',
    '광주': '광주광역시',
    '대구': '대구광역시',
    '대전': '대전광역시',
    '부산': '부산광역시',
    '울산': '울산광역시',
    '인천': '인천광역시',
    '경기': '경기도',
    '강원': '강원도',
    '경남': '경상남도',
    '경북': '경상북도',
    '전남': '전라남도',
    '전북': '전라북도',
    '충남': '충청남도',
    '충북': '충청북도',
    '제주': '제주특별자치도',
    '세종': '세종특별자치시'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('insurance_mg_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR@@MG손해보험\n")

    while True:
        # 보상센터
        store_list = getStores('https://direct.mggeneralins.com/CS010010_001T.ajax', 'comToken=A3O5QJ4YEMECT4RA1YSMUC86VAP5TBGO&devonTokenFieldSessionscope=comToken&', '보상센터')
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            #outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        time.sleep(random.uniform(0.3, 0.9))

        # 영업 서비스점
        store_list = getStores2('https://direct.mggeneralins.com/CHP026T.ajax', '_ESB_REQ_DATA_=%7B%22dbio_affected_count_%22%3A10%2C%22dbio_total_count_%22%3A10%2C%22dbio_fetch_size_%22%3A5%2C%22dbio_fetch_seq_%22%3A5%2C%22stringINDTO%22%3A%5B%7B%7D%5D%7D&comToken=9QEUI4BYH8M0EZ23WPHV7EBGNL55HLXB&devonTokenFieldSessionscope=comToken&', '영업서비스점')
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            #outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        break

    outfile.close()

def getStores(urls, params, store_type):
    print(urls + ' ' + params)
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cookie': 'JSESSIONID=hAOsov4m91DJVdTPtmL9afi8EqYEeRRddYgTKUv06dU9T4Bn9f319cSN1T9fkrAZ.amV1c19kb21haW4vY29uaGNtMTE=; ACEFCID=UID-5934E93B9D905276251AFA73; ACEUCI=1; _ga=GA1.2.661949403.1496639804; _gid=GA1.2.49028569.1496639804',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        #req = urllib2.Request(urls, params, None)
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    response_json = json.loads(response)
    entity_list = response_json['list']['rows']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'MG손해보험'
        strtemp = entity_list[i]['brchofNm'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        if store_type == '보상센터':
            strtemp = strtemp.replace('보상', '보상센터').replace('센터센터', '센터')
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['dataIdno']
        store_info['type'] = store_type

        store_info['newaddr'] = entity_list[i]['addr']
        store_info['pn'] = entity_list[i]['telAreaNo'] + ' ' + entity_list[i]['securTelExchNo'] + ' ' + entity_list[i]['telSeq']

        store_list += [store_info]

    return store_list


def getStores2(urls, params, store_type):
    print(urls + ' ' + params)
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cookie': 'JSESSIONID=tNibFegdVuLLL0W2K3Z8WRKwPRL5FB7K1hngHATbgaE6HB8G9aSjUHtmoXFZjEl0.amV1c19kb21haW4vY29uaHdwMjE=',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        #req = urllib2.Request(urls, params, None)
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)

    response = response.replace('', '')
    response_json = json.loads(response)
    result_list = json.loads(response_json['_ESB_RES_DATA_'])
    entity_list = result_list['orgMstINDTO']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'MG손해보험'
        strtemp = entity_list[i]['hnglOrgNm'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['orgCd']
        store_info['type'] = store_type

        store_info['newaddr'] = entity_list[i]['dtadr']
        store_info['pn'] = entity_list[i]['telAreaNo'] + ' ' + entity_list[i]['telExchNo'] + ' ' + entity_list[i]['telSeq']

        store_list += [store_info]

    return store_list


def convert_full_to_half_char(ch):
    codeval = ord(ch)
    if 0xFF00 <= codeval <= 0xFF5E:
        ascii = codeval - 0xFF00 + 0x20;
        return unichr(ascii)
    else:
        return ch


def convert_full_to_half_string(line):
    output_list = [convert_full_to_half_char(x) for x in line]
    return ''.join(output_list)


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
