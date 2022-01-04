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

    outfile = codecs.open('reebok_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|ADDR|NEWADDR@@리복\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'리복|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 49: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://shop.reebok.co.kr'
    api = '/RPF110101.action'
    data = {
        'command': 'LIST_2',
        'gubn': 'first',
        'paramGubn': '',
        'STORE_NM_PRE': '',
        'STORE_ID': '',
        'SIDO_NM': '전체',
        'GUN_NM': '전체',
        'BRAND': '2',
        'STORE_DIVI': '',
        'STORE_DIVI_NM': '',
        'PAGE_LEN': '',
        'CLUB_YN': 'N',
        'REE_DIRECT_YN': 'N',
        'REE_NODIRECT_YN': 'N',
        'CPON_ID': '',
        'EVENT_ID': '',
        'STORE_NM': ''
    }
    data['PAGE_CUR'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ASPSESSIONIDCCTACBTT=ACCNHAMCLLEGILHLIBELHBCO; ASPSESSIONIDCCQBADTT=CJCAIIFANCKCBNCIOAGIFPOD; wcs_bt=ae960d4b9e602c:1495367762; _ga=GA1.2.1998930491.1495194302; _gid=GA1.2.958050463.1495367763',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)

    response_json = json.loads(response, encoding='utf-8')
    entity_list = response_json['storeList2']['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '리복'
        store_info['subname'] = ''
        strtemp = entity_list[i]['STORE_NM'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        strtemp = strtemp.replace('리복', '').replace('RBK', '').lstrip().rstrip()
        if not strtemp.endswith('점'): strtemp += '점'
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['STORE_ID']
        store_info['type'] = entity_list[i]['STORE_DIVI_NM']

        store_info['addr'] = entity_list[i]['ADDR'] + ' ' + entity_list[i]['DTL_ADDR']
        store_info['newaddr'] = entity_list[i]['DORO_ADDR'] + ' ' + entity_list[i]['DORO_DTL_ADDR']

        store_info['pn'] = ''
        if entity_list[i].get('TEL_NO'):
            store_info['pn'] = entity_list[i]['TEL_NO'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
