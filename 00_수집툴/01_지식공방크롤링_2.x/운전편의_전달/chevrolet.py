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
#import json
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

    outfile = codecs.open('chevrolet_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|XCOORD|YCOORD\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'쉐보레|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 499: break
        elif len(storeList) < 5: break

        time.sleep(random.uniform(0.3, 0.7))

    outfile.close()

def getStores(intPageNo):
    # 'https://www.chevrolet.co.kr/purchase/dealer-location.gm?'
    url = 'https://www.chevrolet.co.kr'
    api = '/purchase/dealer-location.gm?'
    data = {
        '_csrf':'75813b3e-4afd-47e6-9b2e-e73031be935d',
        'accessType': 'search',
        'addrCi': '',
        'addrGu': '',
        'searchType': '1',
        'searchCity': '0',
        'searchGu': '',
        'mgmtDeptName': '',
    }
    # data['pgIdx'] = intPageNo
    # params = urllib.urlencode(data)
    params = '_csrf=75813b3e-4afd-47e6-9b2e-e73031be935d&accessType=search&addrCi=&addrGu=&searchType=1&searchCity=0&searchGu=&mgmtDeptName=%C0%FC%BD%C3%C0%E5%B8%ED%C0%BB+%C0%D4%B7%C2%C7%CF%BC%BC%BF%E4+%BF%B9%29%B5%BF%BC%AD%BF%EF&pgIdx='
    params += str(intPageNo)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '223',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID_WWW=jkdhpxjHVG0qCXZyFg2kJMfgHwFQtsMLZj2hlWnxpyl33MhJf2lX!-487265162!-1464099489; ak_bmsc=FC89332D151FC9B6E77C28BF2C81C382AFCF0E9CD5360000C823315EB77A8314~pluJdEJUlknaSJqGF5Qd0P9/uoe2u9I/aiEbJ2AolEttBPmaz+rKPWl3VnsmJP72QVg6xww96foarheDVShKbr2+v5boNiqWRSbQIKmJoFA3p+mw9c3GPPaPLrPmp1hstjSseBgyH2/QxsyixUyonFTkULaij5h4M82MSiGKWKaKpTScDEkICJKrdw8LIcCBZqHd2VGdie9vtLQnmKsJlNwah6FXUiFh8GK4dmKgU/HCI=; s_cc=true; bm_sv=179A235DD25BC744417E897C8578ED90~Az79D8x2YIjQRxsSTRM8wX4H0MxZuaUf0G6eS0M02Kguli/n5o0Y3iGiVLu3FN5ldCM2aQcMClJ8jFBP+aPXRaEmd/MRRMYNRzPuUMTpbOl605VdiqTFI2kr++TKXQOuO+dlaApN73HKpyrVg53b/xV231/19yZteReD7M2SjKI=; s_nr=1580279240833-New; s_sq=gmapkrchevroletbb%3D%2526pid%253Dch%25253Aich%25253Akr%25253Ako%25253Apurchase%25253Adealer-guide%25253Adealer-location%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.chevrolet.co.kr%25252Fpurchase%25252Fdealer-location.gm%25253FaccessType%25253Dsearch%252526addrCi%25253D%252526addrGu%25253D%252526searchType%2526ot%253DA',
        'Host': 'www.chevrolet.co.kr',
        'Origin': 'https://www.chevrolet.co.kr',
        'Referer': 'https://www.chevrolet.co.kr/purchase/dealer-location.gm?accessType=search&addrCi=&addrGu=&searchType=1&searchCity=0&searchGu=&mgmtDeptName=%C0%FC%BD%C3%C0%E5%B8%ED%C0%BB+%C0%D4%B7%C2%C7%CF%BC%BC%BF%E4+%BF%B9%29%B5%BF%BC%AD%BF%EF&pgIdx=1',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }

    try:
        urls = url + api + params
        print(urls)     # for debugging
        #result = urllib.urlopen(urls)

        urls = url + api
        req = urllib2.Request(urls, params, headers=hdr)
        #req = urllib2.Request(urls, params)
        #req = urllib2.Request(urls, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entityList = tree.xpath('//div[@class="exhibit_list"]//li')

    storeList = []
    for i in range(len(entityList)):
        subname_list = entityList[i].xpath('.//dt')
        info_list = entityList[i].xpath('.//dd')

        if len(subname_list) < 1 or len(info_list) < 2: continue

        storeInfo = {}
        storeInfo['subname'] = ''

        strtemp = "".join(subname_list[0].itertext()).strip('\r\t\n')
        storeInfo['subname'] = strtemp.lstrip().rstrip().replace(' ', '/')

        storeInfo['newaddr'] = '';
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace(':', '')
            if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
            storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace(':', '')
            if strtemp.startswith('전화번호'): strtemp = strtemp[4:].lstrip()
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')

        subinfo_list = entityList[i].xpath('.//dt/a/@onclick')

        storeInfo['xcoord'] = '';     storeInfo['ycoord'] = ''
        if len(subinfo_list) > 0:
            feat_list = subinfo_list[0].split(',')
            if len(feat_list) >= 7:
                storeInfo['xcoord'] = feat_list[3].lstrip().rstrip()[1:-1]
                storeInfo['ycoord'] = feat_list[2].lstrip().rstrip()[1:-1]

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
