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
#from lxml import html

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('gs25_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|NEWADDR|FEAT|SHOPCODE|X|Y@@GS25\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write("GS25|")
            strtemp = store['shopName'] or ''
            if strtemp.startswith('GS25'): strtemp = strtemp[4:].lstrip().rstrip()
            outfile.write(u'%s|' % strtemp)

            outfile.write(u'%s|' % store['address'])

            features = ''
            feat_list = []
            if store.get('offeringService'): feat_list = store['offeringService']
            for i in range(len(feat_list)):
                if i != 0: features += ';'
                features += feat_list[i]
            outfile.write(u'%s|' % features)

            outfile.write(u'%s|' % store['shopCode'])
            store_lon ='';    store_lat = ''
            if store.get('longs'): store_lon = store.get('longs')
            outfile.write(u'%s|' % store_lon)
            if store.get('lat'): store_lat = store.get('lat')
            outfile.write(u'%s\n' % store_lat)
        page += 1

        if page == 1499:     # 2017년11월 기준 1206페이지까지 정보 있음
            break

        delay_time = random.uniform(0.3, 0.9)
        time.sleep(delay_time)

    outfile.close()

def getStores(intPageNo):
    url = 'http://gs25.gsretail.com'
    api = '/gscvs/ko/store-services/locationList'
    data = {
        'pageSize': '10',
        'searchShopName': '',
        'searchSido': '',
        'searchGugun': '',
        'searchDong': '',
        'searchType': '',
        'searchTypeService': 0,
        'searchTypeLotto': 0,
        'searchTypeToto': 0,
        'searchTypeInstant': 0,
        'searchTypeDrug': 0,
        'searchTypeSelf25': 0,
        'searchTypeCoffee': 0,
        'searchTypeBakery': 0,
        'searchTypePost': 0,
        'searchTypeBattery': 0,
        'searchTypeATM': 0,
        'searchTypeTaxrefund': 0
    }
    data['pageNum'] = intPageNo
    # 'CSRFToken=4c38c8bb-ddf5-410b-95d1-bc3b0e51632f' <= 이 값도 있어야 하나???

    params = urllib.urlencode(data)
    #print(params)       # for debugging
    urls = url + api + '?' + params
    print(urls)         # for debugging

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'application/json, text/javascript, */*; q=0.01',     # 이렇게 지정하니 읽을 수 있는 한글코드값 반환
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #'Accept-Charset': 'utf-8',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'Cookie': '_BS_GUUID=ZiYjr7xTIiaTWsdjldiDx6LbgXXcqmWcqrSVVJXE; _ga=GA1.2.404179445.1481533390; JSESSIONID=2C0CDF35523BF80386791545D9D8925A.htomcat1; 3_layerPopCnt=20161219; _TRK_UID=e8827d62752ad2f667b1d956b06190c7:1:6.3018471875:1482076916364; _TRK_CR22400=https%3A%2F%2Fwww.google.co.kr%2F; _dc_gtm_UA-64404561-2=1; _dc_gtm_UA-64404561-6=1; 1_layerPopCnt=2; _TRK_EX22400=3; _TRK_SID=b378301474d361a09579b9e0a7e88834; _ga=GA1.3.129621554.1481045597',
        'Connection': 'keep-alive'
    }

    #response = '"{\"results\":[{\"offeringService\":[\"toto\",\"bakery\",\"post\",\"battery\"],\"shopCode\":\"V3414\",\"longs\":\"546948\",\"address\":\"경기 부천시 오정구 석천로345,  300동 114호(삼정동 365)\",\"shopName\":\"GS252테크노파크점\",\"lat\":\"290926\"},{\"offeringService\":[\"coffee\"],\"shopCode\":\"VM550\",\"longs\":\"600408\",\"address\":\"강원 양양군 현북면 동해대로1242, 38선휴게소 (잔교리 41-10, 38휴게소)\",\"shopName\":\"GS2538선휴게소점\",\"lat\":\"464553\"},{\"offeringService\":[\"post\",\"battery\"],\"shopCode\":\"VQ037\",\"longs\":\"547940\",\"address\":\"서울 양천구 목동서로159-1 (목1동 917-1, CBS방송국1층)\",\"shopName\":\"GS25CBS점\",\"lat\":\"300750\"},{\"offeringService\":[\"post\"],\"shopCode\":\"VO395\",\"longs\":\"553479\",\"address\":\"서울 마포구 매봉산로75, 1층 107호 (상암동 1610)\",\"shopName\":\"GS25DDMC점\",\"lat\":\"302413\"},{\"offeringService\":[\"post\",\"battery\",\"tax\"],\"shopCode\":\"VF073\",\"longs\":\"552104\",\"address\":\"서울 중구 을지로281 (을지로7가 2-1)\",\"shopName\":\"GS25DDP점\",\"lat\":\"312720\"},{\"offeringService\":[\"drug\",\"post\"],\"shopCode\":\"VO550\",\"longs\":\"552978\",\"address\":\"서울 서대문구 남가좌동124-1번지 DMC파크뷰자이 203동 101호\",\"shopName\":\"GS25DMC가재울점\",\"lat\":\"304459\"},{\"offeringService\":[\"drug\",\"self25\",\"post\"],\"shopCode\":\"VO355\",\"longs\":\"446818\",\"address\":\"충북 청주시 상당구 호미로165번길64 (용암동 2682)\",\"shopName\":\"GS25GS상당점\",\"lat\":\"356896\"},{\"shopCode\":\"VU494\",\"longs\":\"250235\",\"address\":\"전남 여수시 여수산단로918(적량동 1320)\",\"shopName\":\"GS25GS칼텍스점\",\"lat\":\"372899\"},{\"offeringService\":[\"post\"],\"shopCode\":\"VQ045\",\"longs\":\"558041\",\"address\":\"인천 강화군 화도면 해안남로2351 (장화리 1106-2)\",\"shopName\":\"GS25G강화가나안점\",\"lat\":\"257443\"},{\"offeringService\":[\"drug\",\"battery\"],\"shopCode\":\"VI989\",\"longs\":\"550678\",\"address\":\"서울 강동구 고덕로39 (암사3동 441-14)\",\"shopName\":\"GS25G고덕점\",\"lat\":\"323290\"}],\"pagination\":{\"totalNumberOfResults\":10477,\"numberOfPages\":1048,\"pageSize\":10,\"currentPage\":0}}"'
    #response = response.replace("\\", '').lstrip().rstrip()
    #if response.startswith('"'): response = response[1:]
    #if response.endswith('"'): response = response[:-1]
    #receivedData = json.loads(response)

    #if receivedData.get('results'): storeList = receivedData['results']
    #else: storeList = []

    #time.sleep(1.1)
    #return storeList

    try:
        #req = urllib2.Request(url+api, data, headers=hdr)      # 이렇게 호출하면 error
        #req.get_method = lambda: 'POST'
        #result = urllib2.urlopen(req)

        req = urllib2.Request(urls, headers=hdr)
        #req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)

        #result = urllib.urlopen(url + api, params, headers=hdr)    # 이렇게 호출하면 error
        #result = urllib.urlopen(urls)     # 이렇게 호출하면 사이트보안정책 위반 결과 반환
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)


    response = result.read()
    #result_encoding = result.headers.getparam('charset')
    #response = result.read().decode(result_encoding)        # 이렇게 해도 한글이 깨짐 (이유 모르겠음 ㅠㅠ)

    #print(response)
    response = response.replace("\\", '').lstrip().rstrip()
    if response.startswith('"'): response = response[1:]
    if response.endswith('"'): response = response[:-1]
    receivedData = json.loads(response)     # GS 25는 json 포맷으로 결과값 반환

    if receivedData.get('results'): storeList = receivedData['results']
    else: storeList = []

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
