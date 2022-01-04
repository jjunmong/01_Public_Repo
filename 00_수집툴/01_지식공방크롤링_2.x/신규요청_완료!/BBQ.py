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
    '세종': '044',
    '경상남도': '055',
    '경상북도': '054',
    '전라남도': '061',
    '전라북도': '063',
    '충청남도': '041',
    '충청북도': '043',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('bbq_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ID|TYPE|XCOORD|YCOORD@@BBQ\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            storeList = getStores(sido_name, page)
            if storeList == None: break
            elif len(storeList) == 0:
                break

            for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()


# v3.0 (2019년4월)
def getStores(strSidoName, intPageNo):
    # https://www.bbq.co.kr/shop/shopListJs.asp
    url = 'http://www.bbq.co.kr'    # https 로 호출하면 API 호출 오류 발생 ㅠㅠ
    api = '/shop/shopListJs.asp'
    data = {
        'lat': '37.491872',
        'lng': '127.115922',
    }
    data['search_text'] = strSidoName
    params = urllib.urlencode(data)
    print(strSidoName)   # for debugging
    #print(params)   # for debugging

    # POST 호출 필요
    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,fr;q=0.5,it;q=0.4,zh-CN;q=0.3,zh;q=0.2',
        'Cookie': 'ASPSESSIONIDQATBBSDC=IPOCEICAPPFOMDJBJCCIPOGD; ASPSESSIONIDQETBBSDC=JPOCEICAHNMBEEDADOHOHNFP',
        #'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API')
        return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()

    entity_list = json.loads(response)
    #entity_list = response_json['shopList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'BBQ'
        store_info['subname'] = ''
        strtemp = entity_list[i]['branch_name']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['branch_address']
        store_info['pn'] = ''
        strtemp = entity_list[i]['branch_tel']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace(' ', '')

        store_info['type'] = entity_list[i]['branch_type']
        store_info['id'] = entity_list[i]['branch_id']

        store_info['xcoord'] = entity_list[i]['wgs84_x']
        store_info['ycoord'] = entity_list[i]['wgs84_y']

        # 기타 속성정보들 있음, 필요할 때 추출할 것!
        store_info['feat'] = ''

        store_list += [store_info]

    return store_list


'''
def getStores(strSidoName, intPageNo):
    url = 'https://www.bbq.co.kr'
    api = '/shop/shop_ajax.asp'
    data = {
        'pagesize': 10,
        'ss': '',
        'gu': '',
        'schval': ''
    }
    data['si'] = strSidoName
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    tableSelector = '//table[@class="table2"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody//tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 5): continue  # 5개 필드 있음

        strSubName = "".join(infoList[0].itertext()).strip('\r\t\n')
        idx = strSubName.find('(')
        if idx != -1: strSubName = strSubName[:idx].lstrip()    # '대명본점(Cafe)'와 같은 지점명 처리 (괄호 부분 삭제, 대부분 FEAT에 같은 내용 있음)
        storeInfo['subname'] = strSubName.rstrip().lstrip().replace(' ', '/')

        storeInfo['newaddr'] = '';
        strtemp = "".join(infoList[1].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = infoList[2].text
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip()

        storeInfo['feat'] = ''
        featList = infoList[3].xpath('.//img/@title')
        for j in range(len(featList)):
            if storeInfo['feat'] != '': storeInfo['feat'] += ';'
            storeInfo['feat'] += featList[j]

        # infoList[4]에 상세정보 페이지 url 정보 있음 (좌석수, 영업시간 정보 등 있음, 필요할 때 추출할 것)

        storeList += [storeInfo]

    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
