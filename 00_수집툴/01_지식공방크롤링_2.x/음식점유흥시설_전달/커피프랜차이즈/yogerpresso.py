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

    outfile = codecs.open('yogerpresso_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|PN|NEWADDR|FEAT|SIZE|OT@@요거프레소\n")

    page = 1
    sentinel_pn = '099-9999-9999'
    while True:
        storeList = getStores(page)
        if storeList == None: break;
        elif len(storeList) == 0: break

        if storeList[0]['pn'] == sentinel_pn: break   # 같은 내용이 끝에서 계속 반복되어서... (같은 전화번호가 한번 더 나오면 종료)
        else: sentinel_pn = storeList[0]['pn']

        for store in storeList:
            outfile.write(u'요거프레소|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['size'])
            outfile.write(u'%s\n' % store['ot'])

        page += 1

        if page == 999: break
        elif len(storeList) < 5: break

        time.sleep(random.uniform(0.3, 0.8))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.yogerpresso.co.kr'
    api = '/story/search'
    data = {
        'areacode': '',
        's_seq': '',
        'query': '',
    }
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
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//table[@class="board-list"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 3): continue  # 4개 필드 있음

        subname = "".join(infoList[0].itertext()).strip('\r\t\n')
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['newaddr'] = '';
        strtemp = "".join(infoList[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            strtemp = strtemp.replace('101호', ' 101호').replace('102호', ' 102호').replace('103호', ' 103호').replace('104호', ' 104호').replace('105호', ' 105호').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('106호', ' 106호').replace('107호', ' 107호').replace('108호', ' 108호').replace('109호', ' 109호').replace('110호', ' 110호').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            strtemp = strtemp.replace('1동', '1동 ').replace('2동', '2동 ').replace('3동', '3동 ').replace('4동', '4동 ').replace('5동', '5동 ').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('6동', '6동 ').replace('7동', '7동 ').replace('8동', '8동 ').replace('9동', '9동 ').replace('0동', '0동 ').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('1층', ' 1층').replace('2층', ' 2층').replace('3층', ' 3층').replace('  ', ' ').lstrip().rstrip()

            temp_list = strtemp.split(' ')
            normalized_addr = ''
            for j in range(len(temp_list)):     # '751-10751-10' 이렇게 잘못 입력된 지번 데이터 처리
                temp_item = temp_list[j]
                idx = len(temp_item) / 2
                if temp_item[:idx] == temp_item[idx:]:
                    temp_item = temp_item[:idx]

                if j != 0: normalized_addr += ' '
                normalized_addr += temp_item

            storeInfo['newaddr'] = normalized_addr.replace('  ', ' ')

        storeInfo['pn'] = '';   storeInfo['feat'] = '';     storeInfo['size'] = ''; storeInfo['ot'] = ''

        shop_id  = infoList[2].xpath('.//a/@href')[0]
        idx = shop_id.find("gostore('")
        shop_id = shop_id[idx+9:]
        idx = shop_id.find("')")
        shop_id = shop_id[:idx]

        data['s_seq'] = shop_id

        params = urllib.urlencode(data)
        # print(params)

        delay_time = random.uniform(0.3, 0.8)
        time.sleep(delay_time)

        try:
            # result = urllib.urlopen(url + api, params)
            suburl = url + api + '?' + params
            print(suburl)  # for debugging
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl')
            storeList += [storeInfo]
            continue

        code = subresult.getcode()
        if code != 200:
            # errExit('HTTP request error (status %d)' % code)
            print('suburl HTTP request error (status %d)' % code)
            storeList += [storeInfo]
            continue

        subresponse = subresult.read()
        #print(response)
        subtree = html.fromstring(subresponse)

        subinfoList = subtree.xpath('//table[@class="form_table"]//tbody//tr')

        storeInfo['pn'] = '';   storeInfo['feat'] = '';     storeInfo['size'] = ''; storeInfo['ot'] = ''
        for j in range(len(subinfoList)):
            if j < 2: continue      # 0 : 지점명, 1 : 새주소

            feat_infoList = subinfoList[j].xpath('.//td')
            if len(feat_infoList) < 2: continue

            feat_name = '';     feat_content = '';
            strtemp = "".join(feat_infoList[0].itertext()).strip('\r\t\n')
            if strtemp != None: feat_name = strtemp.rstrip().lstrip()
            strtemp = "".join(feat_infoList[1].itertext()).strip('\r\t\n')
            if strtemp != None: feat_content = strtemp.rstrip().lstrip()

            if feat_name == '전화번호': storeInfo['pn'] = feat_content
            elif feat_name == '좌석수':
                if feat_content.startswith('총'): feat_content = feat_content[1:].lstrip()
                storeInfo['size'] = feat_content
            elif feat_name == '영업시간':
                feat_content = feat_content.replace(' ', '').replace('*', ';').lstrip().rstrip()
                if feat_content.startswith(';'): feat_content = feat_content[1:]
                storeInfo['ot'] = feat_content
            elif feat_name.startswith('주차'):
                feat_content = feat_content.upper().replace('O', '주차가능').replace('X', '주차불가').replace('주차 가능', '주차가능').replace('주차 불가능', '주차불가')
                feat_content = feat_content.replace('가능', '주차가능').replace('불가능', '주차불가').replace('주차주차', '주차').lstrip().rstrip()
                storeInfo['feat'] = feat_content

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
