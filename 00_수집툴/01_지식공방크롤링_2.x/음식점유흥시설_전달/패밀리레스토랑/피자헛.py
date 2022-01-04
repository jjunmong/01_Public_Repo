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


sido_list = {      # 테스트용 시도 목록
    '서울': '11',
}

sido_list2 = {
    '서울': '42',
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

    outfile = codecs.open('pizzahut_utf8.txt', 'a', 'utf-8')
    #outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|OT|FEAT|KATECX|KATECY@@피자헛\n")

    page = 1
    while True:
        storeList = getStores3()
        if len(storeList) == 0:
            break

        for store in storeList:
            if store['subname'].find('테스트') != -1: continue

            outfile.write("피자헛|")
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['katecx'])
            outfile.write(u'%s\n' % store['katecy'])

        page += 1

        if page == 2:     # 한번 호출로 전국 점포정보 모두 얻을 수 있음
            break

    outfile.close()

# v3.0
def getStores3():
    # 'https://www.pizzahut.co.kr/gis/action/searchBranchByBCode'
    url = 'https://www.pizzahut.co.kr'
    api = '/gis/action/searchBranchByBCode'
    #data = {}
    #params = json.dumps(data)
    #data = {"lang":"ko","requestAt":1554618210677,"data":{"code":"42"}}
    data = {"lang":"ko", "data":{"code":"41"}}
    params = json.dumps(data)
    print(params)  # for debugging

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,fr;q=0.5,it;q=0.4,zh-CN;q=0.3,zh;q=0.2',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        # to do : Cookie, X-CSRF-TOKEN 값 매달 변경해 주어야 함 (매일 바뀜)
        'Cookie':' WMONID=V5n_iinaukh; JSESSIONID=6606ED1BAC7C8B767A21A4B4CA211FE1; _ga=GA1.3.1706380575.1585205026; _gid=GA1.3.1310280450.1585205026; RB_PCID=1585205025882831937; adn_uid=MTEyLjE2OS4zMy42N18xNTg1MjA1MDI2; _gat=1; RB_GUID=3942edd8-d7b2-4947-9b42-34dafe866934; wcs_bt=s_2dc859750f2:1585205056; RB_SSID=78fVwIcTfn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Host': 'www.pizzahut.co.kr',
        'Origin': 'https://www.pizzahut.co.kr',
        'Referer': 'https://www.pizzahut.co.kr/branch/location',
        'X-CSRF-TOKEN' : 'de99d552-f06f-4bdf-a568-19792f8a2be3',    # 이것 필요 (2018/10)
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        print(url+api)
        req = urllib2.Request(url+api, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #response = '{"success":true,"lang":null,"responseAt":1555161524395,"resultCode":"OK","message":null,"redirectUrl":null,"validationErrorSet":[],"data":[{"branchId":"820201","branchName":"분평대로점","branchAddressNumber":"충북 청주시 서원구 분평동 561","x":999415.02,"y":1845330.49,"distance":null,"zoneId":null,"delayTime":null,"storeDelivery":null,"zoneDelivery":null},{"branchId":"896101","branchName":"제천청전점","branchAddressNumber":"충북 제천시 청전동 126-1","x":1063413.16,"y":1905673.6,"distance":null,"zoneId":null,"delayTime":null,"storeDelivery":null,"zoneDelivery":null},{"branchId":"818801","branchName":"청주가경점","branchAddressNumber":"충북 청주시 서원구 복대로 13","x":995154.4,"y":1846731.17,"distance":null,"zoneId":null,"delayTime":null,"storeDelivery":null,"zoneDelivery":null},{"branchId":"878901","branchName":"청주대점","branchAddressNumber":"충북 청주시 청원구 우암동 232-8","x":998982.14,"y":1850438.91,"distance":null,"zoneId":null,"delayTime":null,"storeDelivery":null,"zoneDelivery":null},{"branchId":"811201","branchName":"충북대2호점","branchAddressNumber":"충북 청주시 흥덕구 복대2동 903-3","x":996059.77,"y":1848497.54,"distance":null,"zoneId":null,"delayTime":null,"storeDelivery":null,"zoneDelivery":null},{"branchId":"898801","branchName":"충북오창점","branchAddressNumber":"충북 청원군 오창읍 양청리 752-6 101호","x":993082.23,"y":1857503.06,"distance":null,"zoneId":null,"delayTime":null,"storeDelivery":null,"zoneDelivery":null},{"branchId":"822201","branchName":"충주본점","branchAddressNumber":"충북 충주시 연수동 1705","x":1039185.35,"y":1887184.41,"distance":null,"zoneId":null,"delayTime":null,"storeDelivery":null,"zoneDelivery":null}],"listCount":null,"num1":null}'
    #print(response)
    response_json = json.loads(response)

    entity_list = response_json['data']

    store_list = []
    loop_count = 0      # for debugging
    for i in range(len(entity_list)):

        store_info = {}
        store_info['name'] = '피자헛'
        store_info['subname'] = ''

        strtemp = entity_list[i]['branchName']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['branchId']
        store_info['addr'] = entity_list[i]['branchAddressNumber']
        store_info['pn'] = ''
        store_info['ot'] = ''
        store_info['katecx'] = entity_list[i]['y']  # 맞음? 확인 필요!
        store_info['katecy'] = entity_list[i]['x']  # 맞음? 확인 필요!
        store_info['feat'] = ''

        store_list += [store_info]

    return store_list


# previous version
def getStores():
    # 'https://www.pizzahut.co.kr/branch/location' 호출하면 아래 api 호출해 점포정보 받아 옴
    url = 'https://www.pizzahut.co.kr'
    api = '/gis/action/findAllBranch'
    data = {}
    params = json.dumps(data)
    # print(params)  # for debugging

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,fr;q=0.5,it;q=0.4,zh-CN;q=0.3,zh;q=0.2',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        # to do : Cookie, X-CSRF-TOKEN 값 매달 변경해 주어야 함
        'Cookie': 'WMONID=mxpRF7fVEHS; _ga=GA1.3.1672151892.1554529304; RB_PCID=1554529304047804605; RB_GUID=201de53a-c69d-4157-aea0-feb752b03258; etSessionId=0f41923d-2a7d-4895-afa3-a90c9fe72f59; JSESSIONID=1A9161117F05322ECE0F82316D1135ED; wcs_bt=s_2dc859750f2:1554618030; _gid=GA1.3.1687898803.1554618030; RB_SSID=hyuIgvIX4Y; etRemoteOptions=%7B%7D; etPageInfo=%7B%22pathname%22%3A%22/branch/location%22%2C%22timestamp%22%3A1554618031120%7D; _gali=selectAddress1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Host': 'www.pizzahut.co.kr',
        'Origin': 'https://www.pizzahut.co.kr',
        'Referer': 'https://www.pizzahut.co.kr/branch/location',
        'X-CSRF-TOKEN' : 'd53f3a6c-fcdf-4de0-84f2-1564a5a65f38',    # 이것 필요 (2018/10)
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        print(url+api)
        req = urllib2.Request(url+api, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    response_json = json.loads(response)

    entity_list = response_json['data']

    store_list = []
    loop_count = 0      # for debugging
    for i in range(len(entity_list)):

        store_info = {}
        store_info['name'] = '피자헛'
        store_info['subname'] = ''

        strtemp = entity_list[i]['branchName']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['branchId']
        store_info['addr'] = entity_list[i]['branchAddressNumber'] + ' ' + entity_list[i]['branchAddressDetail']
        store_info['pn'] = entity_list[i]['branchPhone']
        store_info['ot'] = '주중 ' + entity_list[i]['weekdayStartTime'] + '~' + entity_list[i]['weekdayEndTime']
        store_info['ot'] += ';주말 ' + entity_list[i]['weekendStartTime'] + '~' + entity_list[i]['weekendEndTime']
        store_info['katecx'] = entity_list[i]['longitude']
        store_info['katecy'] = entity_list[i]['latitude']

        store_info['feat'] = ''
        if entity_list[i]['restaurantFlag'] == 'YES':
            store_info['feat'] += '레스토랑'
        if entity_list[i]['packingFlag'] == 'YES':
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += '포장'
        if entity_list[i]['deliveryFlag'] == 'YES':
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += '배달'
        if entity_list[i]['parkingFlag'] == 'YES':
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += '주차'
        if entity_list[i]['playroomFlag'] == 'YES':
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += '플레이룸'
        if entity_list[i]['partyFlag'] == 'YES':
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += '파티'
        if entity_list[i]['kidsFlag'] == 'YES':
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += '키즈'
        if entity_list[i]['saladBarFlag'] == 'YES':
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += '샐러드바'
        if entity_list[i]['hotzoneFlag'] == 'YES':
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += '핫존'

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
