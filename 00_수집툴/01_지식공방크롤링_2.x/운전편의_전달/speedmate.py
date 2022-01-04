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

    outfile = codecs.open('speedmate_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@SK스피드메이트\n")

    for sido_name in sido_list:

        page = 1
        while True:
            storeList = getStores(sido_name, page)
            if storeList == None: continue;

            for store in storeList:
                outfile.write(u'SK스피드메이트|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['feat'])

            page += 1

            if page == 999: break
            elif len(storeList) < 10: break

            delay_time = random.uniform(0.3, 0.9)
            time.sleep(delay_time)

        delay_time = random.uniform(1, 2)
        time.sleep(delay_time)

    outfile.close()

def getStores(sido_name, intPageNo):
    # 'https://www.speedmate.com/shop_search/shop_search.do'
    url = 'https://www.speedmate.com'
    api = '/shop_search/shop_search.do'
    data = {
        'mode': 'list',
        'isCheck': 0,
        'checkCity': '',
        'shop1': '',
        'shop2': '',
        'shop3': 'SM',
        'shop4': '',
        'shop5': '',
        'shop6': '',
        'shop7': '',
        'shop8': '',
        'shop9': '',
        'shop10': '',
        'shop11': '',
        'shop12': '',
        'shop13': '',
        'shop': 'SM',
        'city': '',
        'shopName': '',

    }
    data['province'] = sido_name
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    print(params)

    # to do : 쿠키값 주기적으로 갱신해 주어야 함
    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #'Cookie': 'WMONID=s67ycL84fN2; JSESSIONID=kVm_jypWGp2BUX2s8Ch5Xjp6Qv47yrcc76ttC22ebRjTHB0v8Dfr!618572257; _ga=GA1.3.635326233.1527927237; _gid=GA1.3.2011233373.1527927237; _gat=1; _gat_Universe=1; _gali=btnSearchByArea; _gat_UA-96349244-1=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }

    try:
        req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)         # header 없이 호출하면 '' 반환
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
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@class="board_list"]//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        if i == 0: continue     # 첫번째 데이터는 칼럼 정의 데이터

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 5): continue  # 최소 5개 필드 있어야

        storeInfo = {}
        subname = "".join(infoList[0].itertext()).strip('\r\t\n').rstrip().lstrip()
        if not subname.endswith('점'): subname += '점'
        storeInfo['subname'] = subname.replace(' ', '/')

        storeInfo['newaddr'] = ''
        strtemp = "".join(infoList[1].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        storeInfo['pn'] = '';
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None:
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-')
            if storeInfo['pn'] == '--': storeInfo['pn'] = ''

        storeInfo['feat'] = ''
        featList = infoList[4].xpath('.//img/@src')
        for j in range(len(featList)):
            strfeat = '';   strtemp = featList[j]
            if strtemp.endswith('ico_maintenance2.gif'): strfeat = '정비'
            elif strtemp.endswith('icon_tire2.gif'): strfeat = '타이어'
            elif strtemp.endswith('ico_importcar2.gif'): strfeat = '수입차정비'
            elif strtemp.endswith('ico_accident.gif'): strfeat = '수입차사고정비'
            elif strtemp.endswith('icon_gloss.gif'): strfeat = '스팀세차'
            elif strtemp.endswith('ico_rentercar.gif'): strfeat = '렌터카'
            elif strtemp.endswith('ico_oil.gif'): strfeat = 'SK주유소'
            elif strtemp.endswith('ico_membership.gif'): strfeat = '멤버십'
            elif strtemp.endswith('ico_lpg.gif'): strfeat = 'SK충전소'
            elif strtemp.endswith('ico_clean.gif'): strfeat = '자동세차'
            elif strtemp.endswith('icon_division.gif'): strfeat = '직영'
            elif strtemp.endswith('ico_tire.gif'): strfeat = '타이어할인전문'
            elif strtemp.endswith('ico_event.gif'): strfeat = '판촉행사'

            if storeInfo['feat'] != '': storeInfo['feat'] += ';'
            storeInfo['feat'] += strfeat

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
