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
import requests as rq
import random
import json
from lxml import html

sido_list2 = {      # 테스트용 시도 목록
    '강원도': 'gangwondo',
}

sido_list = {
    '서울특별시': 'seoul',
    '광주광역시': 'gwangju',
    '대구광역시': 'daegu',
    '대전광역시': 'daejeon',
    '부산광역시': 'busan',
    '울산광역시': 'ulsan',
    '인천광역시': 'incheon',
    '경기도': 'gyeonggido',
    '강원도': 'gangwondo',
    '경상남도': 'gyeongsangnamdo',
    '경상북도': 'gyeongsangbukdo',
    '전라남도': 'jeonnam',
    '전라북도': 'jeonbuk',
    '충청남도': 'chungnam',
    '충청북도': 'chungbuk',
    '제주특별자치도': 'jejudo',
    '세종특별자치시': 'sejong'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    # get cookie data
    url = 'https://www.tstation.com'
    #url = 'https://www.tstation.com/store/locals'
    res = rq.get(url)
    #cookies = list(res.cookies)
    cookies = res.cookies.get_dict()

    str_cookies = ''
    for key, value in cookies.items():
        str_cookies += key + '=' + value
        str_cookies += '; '

    str_cookies = str_cookies.rstrip()

    # open file for output
    outfile = codecs.open('tstation_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|XCOORD|YCOORD\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            storeList = getStores(sido_name, page, str_cookies)
            if storeList == None: break;
            elif len(storeList) == 0: break

            for store in storeList:
                outfile.write(u'티스테이션|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['feat'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 999: break
            elif len(storeList) < 5: break

            delay_time = random.uniform(0.3, 0.9)
            time.sleep(delay_time)

        delay_time = random.uniform(1.5, 3.5)
        time.sleep(delay_time)

    outfile.close()

def getStores(sido_code, intPageNo, str_cookies):
    # 'http://www.tstation.com/store/search'
    url = 'https://www.tstation.com'      # 'http://www.tstation.com/store/search/list'
    api = '/store/locals/getShopList'
    data = {
        'skkNm': '',
        'shopSort': '1',
        'tabIndex': '1',
        'rowsPerPage': '5',
    }
    data['atmpNm'] = sido_code
    data['pageIdx'] = intPageNo

    #data['atmpNm'] = '서울특별시'
    #data['skkNm'] = '강남구'

    #params = json.dumps(data)
    params = urllib.urlencode(data)
    print(params)

    # to do : 쿠키값 주기적으로 갱신해 주어야 함
    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        #'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Cookie': 'WMONID=RGJkMUIcK7J; foCartId=EA261FFD784C33AF5DD2D3A3DDA9B3FB; _ga=GA1.2.624989243.1554539091; _gid=GA1.2.2029679678.1554539091; __zlcmid=rgi8qtuuuS4zco; JSESSIONID=F779C4898D29F03184E76F344577FD59; _STORE_USER_CONTEXT_=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; _gat_UA-132737068-1=1; _dc_gtm_UA-132737068-1=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    hdr['Cookie'] = str_cookies

    try:
        urls = url + api
        req = urllib2.Request(urls, params, headers=hdr)
        #req = urllib2.Request(urls, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['shopList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['subname'] = ''
        strtemp = entity_list[i]['shopNm']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('티스테이션'): strtemp = strtemp[5:].lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['addrBase']
        store_info['pn'] = ''
        strtemp = entity_list[i]['shopHyphenTelNo']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace(' ', '')

        store_info['xcoord'] = entity_list[i]['shopXpos']
        store_info['ycoord'] = entity_list[i]['shopYpos']

        store_info['feat'] = ''

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
