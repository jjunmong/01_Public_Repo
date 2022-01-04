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

    outfile = codecs.open('hyundai_motors_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|FEAT|XCOORD|YCOORD\n")

    # '대리점' 정보 크롤링
    page = 1
    while True:
        storeList = getStores3(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'현대자동차|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 199: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    # '지점' 정보 크롤링
    page = 1
    while True:
        storeList = getStores3jijum(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'현대자동차|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 199: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v3.0 (2019/1)
def getStores3(intPageNo):   # '대리점' 정보 크롤링
    # 'https://www.hyundai.com/wsvc/kr/core/front/biz/purchaseGuide/carAgencyFind.getAgentList.do'
    url = 'https://www.hyundai.com'
    api = '/wsvc/kr/core/front/biz/purchaseGuide/carAgencyFind.getAgentList.do'
    data = {
        #'lat': '37.4861845',
        #'lon': '127.0336886',
        'lat': '',
        'lon': '',
        #'brNm': '대리점',
        #'cmNm': '대리점',
        #'carNm': '대리점',
        #'ctrNm': '대리점',
        'brAgenScd': '2',
        'rowCount': '10',
    }
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)  # POST 방식일 땐 이렇게 호출해야 함!!!
        req = urllib2.Request(url + api, params)        # header값 맞추기 어려운 경우에는, 그냥 header 정보 없이 호출할 것! (특별한 경우를 빼고는 이렇게 호출해도 됨)
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

    entity_list = response_json['data']['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '현대자동차'
        subname = entity_list[i]['brNm'].lstrip().rstrip()
        store_info['orgname'] = subname
        store_info['subname'] = ''
        if not subname.endswith('대리점'):
            store_info['subname'] = subname + '대리점'
        else: store_info['subname'] = subname

        store_info['newaddr'] = ''
        strtemp = entity_list[i]['brBdnmNmAdr']
        if strtemp != None:
            store_info['newaddr'] = strtemp

            if entity_list[i].get('brBdnmNmDtlAdr'):
                store_info['newaddr'] += ' ' + entity_list[i]['brBdnmNmDtlAdr']

        store_info['pn'] = ''
        strtemp = entity_list[i]['tn']
        if strtemp != None:
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['id'] = entity_list[i]['brCd']
        store_info['feat'] = entity_list[i]['cdNm']

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['lat']
        store_info['ycoord'] = entity_list[i]['lon']

        store_list += [store_info]

    return store_list

def getStores3jijum(intPageNo):      # '지점' 정보 크롤링
    # 'https://www.hyundai.com/wsvc/kr/core/front/biz/purchaseGuide/carAgencyFind.getAgentList.do'
    url = 'https://www.hyundai.com'
    api = '/wsvc/kr/core/front/biz/purchaseGuide/carAgencyFind.getAgentList.do'
    data = {
        #'lat': '37.4861845',
        #'lon': '127.0336886',
        'lat': '',
        'lon': '',
        #'brNm': '지점',
        #'cmNm': '지점',
        #'carNm': '지점',
        #'ctrNm': '지점',
        'brAgenScd': '1',
        'rowCount': '10',
    }
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req = urllib2.Request(url + api, params)        # header값 맞추기 어려운 경우에는, 그냥 header 정보 없이 호출할 것! (특별한 경우를 빼고는 이렇게 호출해도 됨)
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

    entity_list = response_json['data']['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '현대자동차'
        subname = entity_list[i]['brNm'].lstrip().rstrip()
        store_info['orgname'] = subname
        store_info['subname'] = ''
        if not subname.endswith('지점'):
            store_info['subname'] = subname + '지점'
        else: store_info['subname'] = subname

        store_info['newaddr'] = ''
        strtemp = entity_list[i]['brBdnmNmAdr']
        if strtemp != None:
            store_info['newaddr'] = strtemp

            if entity_list[i].get('brBdnmNmDtlAdr'):
                store_info['newaddr'] += ' ' + entity_list[i]['brBdnmNmDtlAdr']

        store_info['pn'] = ''
        strtemp = entity_list[i]['tn']
        if strtemp != None:
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['id'] = entity_list[i]['brCd']
        store_info['feat'] = entity_list[i]['cdNm']

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['lat']
        store_info['ycoord'] = entity_list[i]['lon']

        store_list += [store_info]

    return store_list

# v2.0 (2018/2)
def getStores(intPageNo):   # '대리점' 정보 크롤링
    url = 'https://www.hyundai.com'
    api = '/wsvc/kr/core/front/biz/purchaseGuide/carAgencyFind.getAgentList.do'
    data = {
        #'lat': '37.4861845',
        #'lon': '127.0336886',
        'lat': '',
        'lon': '',
        'brNm': '대리점',
        'cmNm': '대리점',
        'carNm': '대리점',
        'ctrNm': '대리점',
        'rowCount': '10',
    }
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)  # POST 방식일 땐 이렇게 호출해야 함!!!
        req = urllib2.Request(url + api, params)        # header값 맞추기 어려운 경우에는, 그냥 header 정보 없이 호출할 것! (특별한 경우를 빼고는 이렇게 호출해도 됨)
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

    entity_list = response_json['data']['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '현대자동차'
        subname = entity_list[i]['brNm'].lstrip().rstrip()
        store_info['orgname'] = subname
        store_info['subname'] = ''
        if not subname.endswith('대리점'):
            store_info['subname'] = subname + '대리점'
        else: store_info['subname'] = subname

        store_info['newaddr'] = ''
        strtemp = entity_list[i]['brBdnmNmAdr']
        if strtemp != None:
            store_info['newaddr'] = strtemp

            if entity_list[i].get('brBdnmNmDtlAdr'):
                store_info['newaddr'] += ' ' + entity_list[i]['brBdnmNmDtlAdr']

        store_info['pn'] = ''
        strtemp = entity_list[i]['tn']
        if strtemp != None:
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['id'] = entity_list[i]['brCd']
        store_info['feat'] = entity_list[i]['cdNm']

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['lat']
        store_info['ycoord'] = entity_list[i]['lon']

        store_list += [store_info]

    return store_list

def getStores2(intPageNo):      # '지점' 정보 크롤링
    url = 'https://www.hyundai.com'
    api = '/wsvc/kr/core/front/biz/purchaseGuide/carAgencyFind.getAgentList.do'
    data = {
        #'lat': '37.4861845',
        #'lon': '127.0336886',
        'lat': '',
        'lon': '',
        'brNm': '지점',
        'cmNm': '지점',
        'carNm': '지점',
        'ctrNm': '지점',
        'rowCount': '10',
    }
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req = urllib2.Request(url + api, params)        # header값 맞추기 어려운 경우에는, 그냥 header 정보 없이 호출할 것! (특별한 경우를 빼고는 이렇게 호출해도 됨)
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

    entity_list = response_json['data']['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '현대자동차'
        subname = entity_list[i]['brNm'].lstrip().rstrip()
        store_info['orgname'] = subname
        store_info['subname'] = ''
        if not subname.endswith('지점'):
            store_info['subname'] = subname + '지점'
        else: store_info['subname'] = subname

        store_info['newaddr'] = ''
        strtemp = entity_list[i]['brBdnmNmAdr']
        if strtemp != None:
            store_info['newaddr'] = strtemp

            if entity_list[i].get('brBdnmNmDtlAdr'):
                store_info['newaddr'] += ' ' + entity_list[i]['brBdnmNmDtlAdr']

        store_info['pn'] = ''
        strtemp = entity_list[i]['tn']
        if strtemp != None:
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['id'] = entity_list[i]['brCd']
        store_info['feat'] = entity_list[i]['cdNm']

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['lat']
        store_info['ycoord'] = entity_list[i]['lon']

        store_list += [store_info]

    return store_list

'''
# v1.0
def getStores(intPageNo):
    url = 'http://www.hyundai.com'
    api = '/kr/biz/selectBizNwrkMgmtDtlPaging.do'
    data2 = {
        'brType': 1,
        'brType': 2,
        'brType': 3,
        'brGuType': 'C',
        'brDtlAdr1Tmp': '',
        'carCd': '',
        'carveType': '',
        'brDtlAdr1': '',
        'searchKeyword': '',
        'brScn': 'A',
    }
    data = {
    }
    data['pageIndex'] = intPageNo
    # 같은 파라미터에 다음과 같이 값을 다르게 3개 넣어 전달해야 함 '&brType=1&brType=2&brType=3' <= 이유는 모르겠음 ㅠㅠ
    params = urllib.urlencode(data) + '&brType=1&brType=2&brType=3&brGuType=C&brDtlAdr1Tmp=&carCd=&carveType=&brDtlAdr1=&searchKeyword=&brScn=A'
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive'
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req = urllib2.Request(url + api, params)        # header값 맞추기 어려운 경우에는, 그냥 header 정보 없이 호출할 것! (특별한 경우를 빼고는 이렇게 호출해도 됨)

        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@class="boardlist-wrap subsection"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        info_list = entityList[i].xpath('.//td')

        if len(info_list) < 4: continue  # 최소 필드 수 체크

        storeInfo = {}
        subname = "".join(info_list[1].itertext())
        storeInfo['subname'] = subname.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '/')

        storeInfo['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')

        storeInfo['newaddr'] = ''
        temp_list  = info_list[3].xpath('.//a/@onclick')
        if len(temp_list) < 1:
            storeList += [storeInfo];   continue

        strtemp = temp_list[0]
        idx = strtemp.find('fnView(\'')
        if idx == -1: storeList += [storeInfo];    continue

        strtemp = strtemp[idx+8:].lstrip()
        idx = strtemp.find('\'')
        if idx == -1: storeList += [storeInfo];    continue     # for safety
        strtemp = strtemp[:idx].rstrip()

        subapi = '/kr/biz/selectBizNwrkMgmtView.do'
        subdata = {
            'brScn': 1,
            'brViewType': 0,
        }
        subdata['brCd'] = strtemp
        subparams = urllib.urlencode(subdata)

        time.sleep(random.uniform(0.3, 0.9))
        try:
            # result = urllib.urlopen(url + api, params)
            suburl = url + subapi + '?' + subparams
            print(suburl)  # for debugging
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');  continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);      continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="information"]//ul[@class="list-type01"]')
        for j in range(len(subinfo_list)):
            tag_list = subinfo_list[j].xpath('.//li/b')
            value_list = subinfo_list[j].xpath('.//li')

            if len(tag_list) < 1 or len(value_list) < 1 or len(tag_list) != len(value_list): continue

            for k in range(len(tag_list)):
                tag = "".join(tag_list[k].itertext())
                if tag == None: continue
                tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

                value = "".join(value_list[k].itertext())
                if value == None: continue
                value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

                if tag == '주소':
                    if value.startswith('주소'): value = value[2:].lstrip()
                    if value.startswith('|'): value = value[1:].lstrip()
                    storeInfo['newaddr'] = value
                    break

            break   # 첫번째 항목에 새주소 정보 있음... (첫번째 항목만 검사하면 됨)

            # 좌표 정보도 subresponse에 포함되어 있음 (필요할 때 추출할 것!)

        storeList += [storeInfo]

    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
