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
import xml.etree.ElementTree as ElementTree

sido_list = {      # 테스트용 광역시도 목록
    '서울': '02',
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

    outfile = codecs.open('samsungfire_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|TYPE|FEAT@@삼성화재\n")

    for sido_name in sorted(sido_list):

        type_cd = 1
        while True:
            store_list = getStores(sido_name, type_cd)     # 한번 호출로 전국의 해당유형 지점정보 모두 수집
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s\n' % store['feat'])

            type_cd += 1
            if type_cd == 8: break

            time.sleep(random.uniform(1, 2))

    outfile.close()

# v2.0 (2018/2)
def getStores(sido_name, type_cd):
    if type_cd == 5: return []

    # 'https://www.samsungfire.com/sfmi/ui/wshomepage/service/free/anycarland/CN_jidoList.jsp?corpGubun=2&sidoGubun=%BC%AD%BF%EF&gusiGubun=%B0%AD%B3%B2%B1%B8'
    url = 'https://www.samsungfire.com'
    api = '/data/VH.RPCS0128.do?'

    data = {
        #'corpGubun': '2',
        #'sidoGubun': '',
        #'gusiGubun': '',
    }
    data['corpGubun'] = '2'     # 1=고객지원센터
    data['sidoGubun'] = sido_name
    data['gusiGubun'] = ''
    params = urllib.urlencode(data)     # 이렇게 호출하니 한번에 전국 지점 정보가 모두 반환됨???
    print(params)

    params = 'header={"tranId":"VH.RPCS0128"}&body=%7B%22corpGubun%22%3A%22' + str(type_cd) + '%22%2C%22'
    #params += 'sidoGubun%22%3A%22%EC%84%9C%EC%9A%B8%22%2C%22gusiGubun%22%3A%22%EA%B0%95%EB%82%A8%EA%B5%AC%22%7D'   # 광역시도명, 시군구명 지정
    #params += 'sidoGubun%22%3A%22%EC%84%9C%EC%9A%B8%22%2C%22gusiGubun%22%3A%22%22%7D'  # 광역시도명만 지정
    params += 'sidoGubun%22%3A%22%22%2C%22gusiGubun%22%3A%22%22%7D'     # 광역시도명 시군구 이름 없이 호출하면 전체 목록 반환

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        urls = url + api
        req = urllib2.Request(urls, params)
        #req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)
    response_json = json.loads(response)

    entity_list = response_json['responseMessage']['body']['sResult']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}
        store_info['name'] = '삼성화재'

        store_info['subname'] = ''
        if entity_list[i].get('name'):
            strtemp = entity_list[i]['name']
            store_info['subname'] = strtemp.lstrip().rstrip().replace('.', '/').replace(',', '/').replace(' ', '/')

        store_info['id'] = ''
        if entity_list[i].get('cd'):
            store_info['id'] = entity_list[i]['cd']

        store_info['newaddr'] = ''
        if entity_list[i].get('addr'):
            store_info['newaddr'] = entity_list[i]['addr']

        store_info['pn'] = ''
        if entity_list[i].get('tel'):
            store_info['pn'] = entity_list[i]['tel'].lstrip().rstrip().replace(' ', '')

        store_info['type'] = ''
        if entity_list[i].get('gubun'):
            strtemp = entity_list[i]['gubun']
            if strtemp == '1': store_info['type'] = '고객지원센터'
            elif strtemp == '2': store_info['type'] = '지역단/지점'
            elif strtemp == '3': store_info['type'] = '융자지점'
            elif strtemp == '4': store_info['type'] = '보상센터'
            elif strtemp == '6':
                store_info['type'] = '애니카패밀리센터'
                store_info['name'] = '애니카패밀리센터'
                subname_info = entity_list[i]['name']
                subname_info = subname_info.replace('(주)', '').replace('(유)', '').replace('주식회사', '').replace('유한회사', '').lstrip().rstrip()
                store_info['subname'] = subname_info.lstrip().rstrip().replace('.', '/').replace(',', '/').replace(' ', '/')
            elif strtemp == '7':
                store_info['type'] = '애니카랜드'
                store_info['name'] = '애니카랜드'
                subname_info = entity_list[i]['name']
                subname_info = subname_info.replace('(주)', '').replace('(유)', '').replace('주식회사', '').replace('유한회사', '').lstrip().rstrip()
                subname_info = subname_info.replace('애니카랜드', '').lstrip().rstrip()
                store_info['subname'] = subname_info.lstrip().rstrip().replace('.', '/').replace(',', '/').replace(' ', '/')

        store_info['feat'] = ''
        if entity_list[i].get('service'):
            store_info['feat'] = entity_list[i]['service']

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
