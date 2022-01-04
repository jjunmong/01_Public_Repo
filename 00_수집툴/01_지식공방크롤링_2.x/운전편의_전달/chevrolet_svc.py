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

    outfile = codecs.open('chevrolet_svc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|TELNUM2|FEAT|XCOORD|YCOORD@@쉐보레서비스센터\n")

    outfile2 = codecs.open('chevrolet_svc_other_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|NEWADDR|TELNUM2|FEAT|XCOORD|YCOORD@@쉐보레지정서비스센터\n")

    outfile3 = codecs.open('chevrolet_svc_baro_utf8.txt', 'w', 'utf-8')
    outfile3.write("##NAME|SUBNAME|TELNUM|NEWADDR|TELNUM2|FEAT|XCOORD|YCOORD@@쉐보레바로서비스센터\n")


    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:

            if store['subname'].find('바로서비스') != -1:    # 바로서비스센터
                outfile3.write(u'쉐보레서비스센터|')
                outfile3.write(u'%s|' % store['subname'])
                outfile3.write(u'%s|' % store['pn'])
                outfile3.write(u'%s|' % store['newaddr'])
                outfile3.write(u'%s|' % store['pn2'])
                outfile3.write(u'%s|' % store['feat'])
                outfile3.write(u'%s|' % store['xcoord'])
                outfile3.write(u'%s\n' % store['ycoord'])
            elif store['subname'].find('서비스센터') != -1:  # 직영서비스센터
                outfile.write(u'쉐보레서비스센터|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['pn2'])
                outfile.write(u'%s|' % store['feat'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])
            else:   # 지정서비스센터
                outfile2.write(u'쉐보레서비스센터|')
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s|' % store['pn2'])
                outfile2.write(u'%s|' % store['feat'])
                outfile2.write(u'%s|' % store['xcoord'])
                outfile2.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 999: break
        elif len(storeList) < 5: break

        time.sleep(random.uniform(0.3, 0.7))

    outfile.close()
    outfile2.close()
    outfile3.close()

def getStores(intPageNo):
    url = 'https://www.chevrolet.co.kr'
    api = '/chevy/as.gm?'
    data = {
        'accessType': 'search',
        'addrSi': '',
        'addrGu': '',
        'searchType': '1',
        'searchCity': '0',
        'searchGu': '',
        'firmName': '',
    }
    #data['pgIdx'] = intPageNo
    #params = urllib.urlencode(data)
    params = 'accessType=search&addrSi=&addrGu=&workArea=&searchType=1&searchCity=0&searchGu=&firmName=%BC%AD%BA%F1%BD%BA%BC%BE%C5%CD%B8%ED%C0%BB+%C0%D4%B7%C2%C7%CF%BC%BC%BF%E4&pgIdx='
    params += str(intPageNo)
    # print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Encoding': 'deflate, br',   # gzip 옵션이 포함되어 있으면 압축해서 결과를 보냄
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        #'Cookie': '_ga=GA1.3.1047499610.1543994023; JSESSIONID_WWW=VGfhc0nL9N6bx2JGCyvhDJLxMhyKTLLlBqCTY8y2LVjH4z9wQ10D!240099268!-1851550024; s_cc=true; _gid=GA1.3.1632263789.1546956364; s_nr=1546957058097-New; s_sq=gmapkrchevroletbb%3D%2526pid%253Dch%25253Aich%25253Akr%25253Ako%25253Apurchase%25253Adealer-guide%25253Adealer-location%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.chevrolet.co.kr%25252Fpurchase%25252Fdealer-location.gm%25253F%252523%2526ot%253DA',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
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

    entityList = tree.xpath('//div[@class="list_box"]//li')

    storeList = []
    for i in range(len(entityList)):
        subname_list = entityList[i].xpath('.//dt')
        info_list = entityList[i].xpath('.//dd')

        if len(subname_list) < 1 or len(info_list) < 2: continue

        storeInfo = {}
        storeInfo['subname'] = '';      storeInfo['feat'] = ''

        strtemp = "".join(subname_list[0].itertext()).strip('\r\t\n').lstrip().rstrip()
        if strtemp.startswith('[직영]'):
            strtemp = strtemp[4:].lstrip()
            storeInfo['feat'] = '직영'
        storeInfo['subname'] = strtemp.lstrip().rstrip().replace(' ', '/')

        storeInfo['newaddr'] = '';
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace(':', '')
            if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
            storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = '';   storeInfo['pn2'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace(':', '')
            if strtemp.startswith('전화번호'): strtemp = strtemp[4:].lstrip()
            idx = strtemp.find('(')
            if idx != -1:
                storeInfo['pn2'] = strtemp[idx+1:-1].rstrip().lstrip().replace('.', '-')
                storeInfo['pn'] = strtemp[:idx].rstrip().lstrip().replace('.', '-')
            else:
                storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-')

        subinfo_list = entityList[i].xpath('.//dt/a/@onclick')

        storeInfo['xcoord'] = '';     storeInfo['ycoord'] = ''
        if len(subinfo_list) > 0:
            feat_list = subinfo_list[0].split(',')
            if len(feat_list) >= 7:
                storeInfo['xcoord'] = feat_list[2].lstrip().rstrip()[1:-1]
                storeInfo['ycoord'] = feat_list[1].lstrip().rstrip()[1:-1]

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
