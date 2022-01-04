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
import urllib2
from lxml import html

sido_list2 = {      # 테스트용 시도 목록
    '부산': '051'
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

    outfile = codecs.open('himart_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|OT|XCOORD|YCOORD@@하이마트\n")

    page = 1
    while True:
        storeList = getStores(page)

        if storeList == None: break;
        elif len(storeList) == 0: break

        for store in storeList:
            store_name = store['brchNm']
            if store_name.endswith('하이마트'): store_name = store_name[:-4]
            store_name.lstrip().rstrip()

            if store_name == '테스트지점': continue
            elif store_name.endswith('콜센터'): continue
            elif not store_name.endswith('점'): store_name += '점'

            outfile.write(u'롯데하이마트|')
            outfile.write(u'%s|' % store_name)

            outfile.write(u'%s|' % store['telNo'])

            store_addr = store['fullRgnNm'] + ' ' + store['dtlAddr']
            outfile.write(u'%s|' % store_addr)

            outfile.write(u'%s|' % store['bizTime'])
            outfile.write(u'%s|' % store['mapYpoxVal'])     # x, y 거꾸로 입력되어 있음
            outfile.write(u'%s\n' % store['mapXpoxVal'])

        page += 1
        if page == 999: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.e-himart.co.kr'
    api = '/app/common/findListMyStoreAjax'
    data = {
        'skkNm': '',
        'atmpNm': '',
        'searchGbn': 'undefined',
        'brchNm': '',
        'page': '',
        'size': 10,
    }
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'PCID=15069365403109872789288; alido_pcid=nZJhuHIvOmqtHuwuMkGBV; alido_uid=nZJhuHIvOmqtHuwuMkGBV; _ga=GA1.3.984666410.1510336171; MyKeywordWN=; PCID=15069365403109872789288; LMSSO=isSSOLogin-Y|isSVCAgree-N; TS01417953=01930021002235fbb9baf4cbea320da877aec20079c112103014f322fa7c2f9cd55367416ae55fac8d7348b5819b971e13c31b06245c0c9f8e98941886458fda8e5a6dd12c; JSESSIONID=c8c9fab0-ed31-11e7-9ec7-0050569d44dd; wcs_bt=s_2cafe37f3587:1514618375; __fromShop=drfKEAqUevBLU9udVTNIP+9bOVDiipBAltSBc2J7hFFyB3ma9p5KQIHk1+o1Afif2gkSjTMmoCvn9+NPTetspLYaMQquMjEFJt0frZEbIhLqdQz78MxclNdesKcT5MzcyDyvZcwWnj+yY14dihGvbQ==; __csFP=drfKEAqUevBLU9udVTNIP4zUeTlwzGqjq7HpCEY0sP0wh3ejyB8tJzudxzD4uTlP8IJZsWsRVICGrINnQbrjVfm6nfCViV+WqVAYuztHizGkmJQw1PQ2BWsA8wbpg+kKQesVxp5/35x6XkHVZq3hrou3gV5xwUnp/4/ymIY7Jx16GxS5EXoMSxnLKCwGnYKKr2xxnRNjLw99n0cPJhtFWA==; TS0154a0aa=0194c1154512fdca7de505851e051d5002938ff0c58ef8d341b518f43ab134f31f29107f619962632ab9fb223ce72ef659adf528b0; TS015866e0=0194c115453aba4ef3caa4541be4a73d8ac61ec96f99d9c0064fe36f6b18f65758e5ce0794dc3329ded90520d465e38b10ba47ade311757a83a9701918e0aa8a107a74a67839e7ecfe4ecfcdddab6d3e86ecf886b3c9715a64c467bf29548dcc2f4275e070a5e530fbffa5c2d5aa4048073688f006',
        'Host': 'www.e-himart.co.kr',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    }

    try:
        urls = url + api
        req = urllib2.Request(urls, params, headers=hdr)
        #req = urllib2.Request(urls, params, None)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    print(response)        # for debugging

    receivedData = json.loads(response)  # json 포맷으로 결과값 반환

    if receivedData.get('data'): storeList = receivedData['data']
    else: storeList = []

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
