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
    '서울': 10,
}

sido_list = {
    '서울': 10,
    '광주': 52,
    '대구': 43,
    '대전': 32,
    '부산': 42,
    #'울산': '052',
    '인천': 11,
    '경기': 12,
    '강원': 20,
    '경남': 40,
    '경북': 41,
    '전남': 50,
    '전북': 51,
    '충남': 30,
    '충북': 31,
    #'제주': '064',
    #'세종': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('lottesuper_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|NEWADDR|FEAT@@롯데슈퍼\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            storeList = getStores('롯데슈퍼', 'STORE', sido_list[sido_name], page)
            if storeList == None: break;

            for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['feat'])

            page += 1

            if page == 99: break
            elif len(storeList) < 10: break
            elif storeList == [] : break
            time.sleep(random.uniform(0.3, 0.9))

    page = 1
    while True:
        storeList = getStores('롯데마켓999', 'MARKET', '', page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 99: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    # 가맹점 정보 얻기
    storeList = getStores2('롯데슈퍼', 'MARKET', '', '')
    if storeList != None:
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

    outfile.close()


def getStores(franchise_name, search_code, sido_code, intPageNo):
    url = 'http://www.lottesuper.co.kr'
    api = '/handler/cc/Store-Start'
    data = {
        #'gubun': 'STORE',
        'searchType': 'A',
        'atmp_nm': '',
        'skk_nm': '',
        'emd_nm': '',
        'storeSearchWord': '',
    }
    data['gubun'] = search_code
    data['store_area_gubun_code'] = sido_code
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': '',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'SPEEDCDN=894690707; MOBILEYN=N; ec_chl_no=000000; _USER_INFO_SUPPORT_=rO0ABXNyADBjb20ubG90dGVzdXBlci5mcm9udC5lbnRpdHkudXNlci5Vc2VySW5mb1N1cHBvcnTTPBbVycirCwIAAHhyACljb20ubG90dGVzdXBlci5mcm9udC5lbnRpdHkudXNlci5Vc2VySW5mb9Mv8OJovIVWAgBWWgAFYWR1bHRJAANhZ2VJAAphdXRoU3RhdHVzWgAGYklNYWxsWgAIYklzTG9naW5aAAliTG90dGVFbXBaAAxpc1N1cGVyU3RhZmZJAAtsb2dpblN0YXR1c0kACWxvZ2luVHlwZVoACHBvaW50UXJ5TAAJYWRkclNjdENkdAASTGphdmEvbGFuZy9TdHJpbmc7TAAIYmlydGhkYXlxAH4AAkwACWNlbGxFbmROb3EAfgACTAAJY2VsbFNjdE5vcQB+AAJMAAhjZWxsVHhOb3EAfgACTAAIY2hnU3ViQ2RxAH4AAkwABWNobE5vcQB+AAJMAAZjdXN0Tm9xAH4AAkwAB2RlbGlNc2dxAH4AAkwACGRsdlNocENkcQB+AAJMAAhkbHZTdHJObXEAfgACTAAIZGx2U3RyTm9xAH4AAkwABmRsdnBObXEAfgACTAAHZHRsQWRkcnEAfgACTAAJZW1haWxBZGRycQB+AAJMABBlbWFpbFJjdkFnckRUaW1lcQB+AAJMAAplbWFpbFJjdllucQB+AAJMAAZlbnRyTm9xAH4AAkwAC2ZhbWlseU1icklkcQB+AAJMAAtmYW1pbHlNYnJZTnEAfgACTAANZnJlc2hDZW50ZXJZbnEAfgACTAAOZnJzdExvZ2luRHRpbWVxAH4AAkwACGdlblNjdENkcQB+AAJMAAlpcGluVXNlWU5xAH4AAkwACGpvYlNjdENkcQB+AAJMAA1sb3R0ZU1ickFncllOcQB+AAJMAAxtYnJDZXJ0U2N0Q2RxAH4AAkwACm1ickRsdnBTZXFxAH4AAkwACm1ickdyYWRlQ2RxAH4AAkwAEm1ickdyYWRlQ3BuSXNzdWVZbnEAfgACTAAFbWJySWRxAH4AAkwADW1ickluZndQYXRoQ2RxAH4AAkwAB21ick5hbWVxAH4AAkwABW1ick5vcQB+AAJMAAhtYnJTY3RDZHEAfgACTAAKbmF0aW9uRmxhZ3EAfgACTAAFb3JkTm9xAH4AAkwACHBhc3N3b3JkcQB+AAJMAA5wYXNzd29yZEluaXRZbnEAfgACTAAIcG9zdEFkZHJxAH4AAkwABnBvc3ROb3EAfgACTAAMcHJldkRsdlNlcUNkcQB+AAJMAAlwcmV2U3RyTm1xAH4AAkwACHJlQWRtc1lOcQB+AAJMABFyZWZ1bmRBY2NvdW50TmFtZXEAfgACTAAPcmVmdW5kQWNjb3VudE5vcQB+AAJMAAxyZWZ1bmRCYW5rQ2RxAH4AAkwADHJlZnVuZEJhbmtObXEAfgACTAAJcmV0dXJuVXJscQB+AAJMAApybWl0Q2VsbE5vcQB+AAJMAAtybWl0RHRsQWRkcnEAfgACTAANcm1pdEVtYWlsQWRkcnEAfgACTAAGcm1pdE5tcQB+AAJMAAtybWl0UGhvbmVOb3EAfgACTAAMcm1pdFBvc3RBZGRycQB+AAJMAApybWl0UG9zdE5vcQB+AAJMAA1ybWl0UG9zdE5vU2VxcQB+AAJMAApzY3NuQ2F1c0NkcQB+AAJMAAxzY3NuQ2F1c0NvbnRxAH4AAkwACXNjc25EdGltZXEAfgACTAAGc2NzbllOcQB+AAJMAA5zbXNSY3ZBZ3JEVGltZXEAfgACTAAIc21zUmN2WW5xAH4AAkwAB3NvbGFyWW5xAH4AAkwAA3NzbnEAfgACTAAHc3RhZmZZbnEAfgACTAAPc3RubVJtaXREdGxBZGRycQB+AAJMABBzdG5tUm1pdFBvc3RBZGRycQB+AAJMAA5zdG5tUm1pdFBvc3ROb3EAfgACTAAIdGVsRW5kTm9xAH4AAkwACHRlbFJnbk5vcQB+AAJMAAd0ZWxUeE5vcQB+AAJMAAZ1c2VySXBxAH4AAkwADHdlZEFubml2RGF0ZXEAfgACTAAId2VkU2N0Q2RxAH4AAkwACndpZGVBcmVhWU5xAH4AAnhwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBwcHBwcHQABjAwMDAwMHBwdAACMTB0AAzrjIDtkZzrp6TsnqV0AAYxMDAwMDBwcHBwcHQAATBwcHQAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHA=; GSESID=Fns0XTTeRT8AjuI067pCsN1A4qpgQgw1mnwfxTIfBIO1jyhWgYFxDWH1JacGgtus.espfwas1_servlet_front; STR_NO=100000; JSESSIONID=Dqbn8TNH8zYYBue46C0eiwPAZUvZJlNGmCz8Jwe8Uf5frVaRgSzNGLpB3iD5uYxv.espfwas2_servlet_front',
    }

    #params = 'pageNo=3&store_area_gubun_code=10&gubun=STORE&searchType=A&atmp_nm=&skk_nm=&emd_nm=&storeSearchWord='
    try:
        urls = url + api
        #req = urllib2.Request(urls, params)
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');
        return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entityList = tree.xpath('//div[@id="storeListArea1"]//tbody//tr')

    storeList = []
    for i in range(len(entityList)):

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 4개 필드 있음

        storeInfo = {}
        storeInfo['name'] = franchise_name

        subname = "".join(infoList[0].itertext()).strip('\r\t\n')
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['id'] = ''
        temp_list = infoList[0].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('StoreDetail(')
            if idx != -1:
                strtemp = strtemp[idx+12:]
                idx = strtemp.find(')')
                storeInfo['id'] = strtemp[:idx][1:-1]

        storeInfo['addr'] = '';     storeInfo['newaddr'] = '';
        addr_info = infoList[1].xpath('./a')
        if len(addr_info) > 0:
            strtemp = "".join(addr_info[0].itertext()).strip('\r\t\n')
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            strtemp = strtemp.replace('&#91;', '').replace('&#93;', '')

            idx = strtemp.find('도로명주소')
            if idx != -1:
                storeInfo['addr'] = strtemp[:idx].rstrip()
                storeInfo['newaddr'] = strtemp[idx+5:].lstrip()
                if storeInfo['addr'].endswith('['): storeInfo['addr'] = storeInfo['addr'][:-1].rstrip()
                if storeInfo['newaddr'].startswith(']'): storeInfo['newaddr'] = storeInfo['newaddr'][1:].lstrip()
            else:
                storeInfo['addr'] = strtemp

        storeInfo['pn'] = ''
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip().replace(')', '-')

        storeInfo['feat'] = ''
        # 상세정보 페이지에 주차장, 영업시간 정보 등 있음, 필요할 때 추출할 것!

        storeList += [storeInfo]

    # 가맹점 정보 추출
    if sido_code == '10' and intPageNo == 1:
        entityList = tree.xpath('//div[@id="storeListArea2"]//tbody//tr')

        for i in range(len(entityList)):
            infoList = entityList[i].xpath('.//td')

            if (infoList == None): continue;  # for safety
            elif (len(infoList) < 4): continue  # 4개 필드 있음

            storeInfo = {}
            storeInfo['name'] = franchise_name

            storeInfo['subname'] = ''
            subname = "".join(infoList[1].itertext())
            if subname != None:
                subname = subname.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                if not subname.endswith('점'): subname += '점'
                storeInfo['subname'] = subname.replace(' ', '/')

            storeInfo['id'] = ''

            storeInfo['addr'] = '';     storeInfo['newaddr'] = '';
            strtemp = "".join(infoList[2].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                storeInfo['addr'] = strtemp

            storeInfo['pn'] = ''
            strtemp = "".join(infoList[3].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                storeInfo['pn'] = strtemp.replace(')', '-')

            storeInfo['feat'] = '가맹점'

            storeList += [storeInfo]

    return storeList

# 가맹점 검색 결과 얻기 (앞에서 처리함)
def getStores2(franchise_name, search_code, sido_code, intPageNo):
    url = 'http://www.lottesuper.co.kr'
    api = '/handler/cc/Store-Start'
    data = {
        #'gubun': 'STORE',
        'searchType': 'A',
        'atmp_nm': '',
        'skk_nm': '',
        'emd_nm': '',
        'storeSearchWord': '',
    }
    data['gubun'] = search_code
    data['store_area_gubun_code'] = sido_code
    data['pageNo'] = intPageNo

    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': '',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'SPEEDCDN=894690707; MOBILEYN=N; ec_chl_no=000000; _USER_INFO_SUPPORT_=rO0ABXNyADBjb20ubG90dGVzdXBlci5mcm9udC5lbnRpdHkudXNlci5Vc2VySW5mb1N1cHBvcnTTPBbVycirCwIAAHhyACljb20ubG90dGVzdXBlci5mcm9udC5lbnRpdHkudXNlci5Vc2VySW5mb9Mv8OJovIVWAgBWWgAFYWR1bHRJAANhZ2VJAAphdXRoU3RhdHVzWgAGYklNYWxsWgAIYklzTG9naW5aAAliTG90dGVFbXBaAAxpc1N1cGVyU3RhZmZJAAtsb2dpblN0YXR1c0kACWxvZ2luVHlwZVoACHBvaW50UXJ5TAAJYWRkclNjdENkdAASTGphdmEvbGFuZy9TdHJpbmc7TAAIYmlydGhkYXlxAH4AAkwACWNlbGxFbmROb3EAfgACTAAJY2VsbFNjdE5vcQB+AAJMAAhjZWxsVHhOb3EAfgACTAAIY2hnU3ViQ2RxAH4AAkwABWNobE5vcQB+AAJMAAZjdXN0Tm9xAH4AAkwAB2RlbGlNc2dxAH4AAkwACGRsdlNocENkcQB+AAJMAAhkbHZTdHJObXEAfgACTAAIZGx2U3RyTm9xAH4AAkwABmRsdnBObXEAfgACTAAHZHRsQWRkcnEAfgACTAAJZW1haWxBZGRycQB+AAJMABBlbWFpbFJjdkFnckRUaW1lcQB+AAJMAAplbWFpbFJjdllucQB+AAJMAAZlbnRyTm9xAH4AAkwAC2ZhbWlseU1icklkcQB+AAJMAAtmYW1pbHlNYnJZTnEAfgACTAANZnJlc2hDZW50ZXJZbnEAfgACTAAOZnJzdExvZ2luRHRpbWVxAH4AAkwACGdlblNjdENkcQB+AAJMAAlpcGluVXNlWU5xAH4AAkwACGpvYlNjdENkcQB+AAJMAA1sb3R0ZU1ickFncllOcQB+AAJMAAxtYnJDZXJ0U2N0Q2RxAH4AAkwACm1ickRsdnBTZXFxAH4AAkwACm1ickdyYWRlQ2RxAH4AAkwAEm1ickdyYWRlQ3BuSXNzdWVZbnEAfgACTAAFbWJySWRxAH4AAkwADW1ickluZndQYXRoQ2RxAH4AAkwAB21ick5hbWVxAH4AAkwABW1ick5vcQB+AAJMAAhtYnJTY3RDZHEAfgACTAAKbmF0aW9uRmxhZ3EAfgACTAAFb3JkTm9xAH4AAkwACHBhc3N3b3JkcQB+AAJMAA5wYXNzd29yZEluaXRZbnEAfgACTAAIcG9zdEFkZHJxAH4AAkwABnBvc3ROb3EAfgACTAAMcHJldkRsdlNlcUNkcQB+AAJMAAlwcmV2U3RyTm1xAH4AAkwACHJlQWRtc1lOcQB+AAJMABFyZWZ1bmRBY2NvdW50TmFtZXEAfgACTAAPcmVmdW5kQWNjb3VudE5vcQB+AAJMAAxyZWZ1bmRCYW5rQ2RxAH4AAkwADHJlZnVuZEJhbmtObXEAfgACTAAJcmV0dXJuVXJscQB+AAJMAApybWl0Q2VsbE5vcQB+AAJMAAtybWl0RHRsQWRkcnEAfgACTAANcm1pdEVtYWlsQWRkcnEAfgACTAAGcm1pdE5tcQB+AAJMAAtybWl0UGhvbmVOb3EAfgACTAAMcm1pdFBvc3RBZGRycQB+AAJMAApybWl0UG9zdE5vcQB+AAJMAA1ybWl0UG9zdE5vU2VxcQB+AAJMAApzY3NuQ2F1c0NkcQB+AAJMAAxzY3NuQ2F1c0NvbnRxAH4AAkwACXNjc25EdGltZXEAfgACTAAGc2NzbllOcQB+AAJMAA5zbXNSY3ZBZ3JEVGltZXEAfgACTAAIc21zUmN2WW5xAH4AAkwAB3NvbGFyWW5xAH4AAkwAA3NzbnEAfgACTAAHc3RhZmZZbnEAfgACTAAPc3RubVJtaXREdGxBZGRycQB+AAJMABBzdG5tUm1pdFBvc3RBZGRycQB+AAJMAA5zdG5tUm1pdFBvc3ROb3EAfgACTAAIdGVsRW5kTm9xAH4AAkwACHRlbFJnbk5vcQB+AAJMAAd0ZWxUeE5vcQB+AAJMAAZ1c2VySXBxAH4AAkwADHdlZEFubml2RGF0ZXEAfgACTAAId2VkU2N0Q2RxAH4AAkwACndpZGVBcmVhWU5xAH4AAnhwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBwcHBwcHQABjAwMDAwMHBwdAACMTB0AAzrjIDtkZzrp6TsnqV0AAYxMDAwMDBwcHBwcHQAATBwcHQAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHA=; GSESID=Fns0XTTeRT8AjuI067pCsN1A4qpgQgw1mnwfxTIfBIO1jyhWgYFxDWH1JacGgtus.espfwas1_servlet_front; STR_NO=100000; JSESSIONID=Dqbn8TNH8zYYBue46C0eiwPAZUvZJlNGmCz8Jwe8Uf5frVaRgSzNGLpB3iD5uYxv.espfwas2_servlet_front',
    }

    #params = 'pageNo=3&store_area_gubun_code=10&gubun=STORE&searchType=A&atmp_nm=&skk_nm=&emd_nm=&storeSearchWord='
    try:
        urls = url + api
        #req = urllib2.Request(urls, params)
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');
        return None

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    tableSelector = '//div[@id="storeListArea2"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody//tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 4개 필드 있음

        storeInfo = {}
        storeInfo['name'] = franchise_name

        storeInfo['subname'] = ''
        subname = "".join(infoList[1].itertext())
        if subname != None:
            subname = subname.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            if not subname.endswith('점'): subname += '점'
            storeInfo['subname'] = subname.replace(' ', '/')

        storeInfo['addr'] = '';     storeInfo['newaddr'] = '';
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['addr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = "".join(infoList[3].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip().replace(')', '-')

        storeInfo['id'] = ''
        storeInfo['feat'] = '가맹점'
        # 상세정보 페이지에 주차장, 영업시간 정보 등 있음, 필요할 때 추출할 것!

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
