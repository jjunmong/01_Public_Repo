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
import urllib2
import json
from lxml import html

sido_list2 = {      # 테스트용 광역시도 목록
    '인천광역시': '032',
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

    outfile = codecs.open('oliveyoung_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ID@@올리브영\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            storeList = getStores(sido_name, page)
            if storeList == None: break;
            elif len(storeList) == 0: break

            for store in storeList:
                outfile.write("올리브영|")
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['id'])

            page += 1

            if len(storeList) < 20:
                break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'http://www.oliveyoung.co.kr'
    api = '/store/store/getStoreListJson.do'
    data = {
        'searchType': 'word',
    }
    data['pageIdx'] = intPageNo
    data['searchWord'] = sido_name
    params = urllib.urlencode(data)
    print(params)

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
        #req = urllib2.Request(urls, params, headers=hdr)
        req = urllib2.Request(urls, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');        return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    response_json = json.loads(response)
    entity_list = response_json['storeList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['subname'] = ''
        strtemp = entity_list[i]['strNm']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['addr']
        store_info['pn'] = ''
        strtemp = entity_list[i]['phon']
        if strtemp != None:
            store_info['pn'] = strtemp.lstrip().rstrip().replace(' ', '')

        store_info['id'] = entity_list[i]['strNo']

        # 매장 상세정보 페이지'http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=D509'에 영업시간 정보 있음 (좌표 정보도 있는 경우 있음)

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
