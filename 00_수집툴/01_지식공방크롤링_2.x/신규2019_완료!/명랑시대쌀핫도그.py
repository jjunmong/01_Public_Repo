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

    outfile = codecs.open('myungrangsidae_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'명랑핫도그|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 99: break
        elif len(storeList) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://xn--vk1b3pg3gnxdbzo4mihuxlgb.com'
    api = '/information/page/'
    data = {}
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + str(intPageNo) + '/'
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//table[@class="map_list"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        info_list = entityList[i].xpath('.//td')

        if len(info_list) < 4: continue  # 최소 필드 수 체크

        storeInfo = {}

        subinfo_list = info_list[1].xpath('./a')
        if len(subinfo_list) < 1: continue

        storeInfo['subname'] = ''
        storeInfo['pn'] = ''
        subname = "".join(subinfo_list[0].itertext())
        if subname != None:
            subname = subname.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            if subname.startswith('명랑핫도그'): subname = subname[5:].lstrip()
            storeInfo['subname'] = subname.replace(' ', '/')

        # 사이트에 html syntax error 있음 ㅠㅠ, <td></td> 쌍이 맞지 않음 ㅠㅠ
        if len(subinfo_list) >= 2:
            strtemp = "".join(subinfo_list[1].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                storeInfo['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')
        else:
            pn_list = entityList[i].xpath('.//a[@class="mobile_tel"]')
            if len(pn_list) > 0:
                strtemp = "".join(pn_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                    storeInfo['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')
            else:
                strtemp = "".join(info_list[1].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                    idx = strtemp.find('010')
                    if idx != -1:
                        strtemp = strtemp[idx:]
                        storeInfo['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')

        storeInfo['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            storeInfo['newaddr'] = strtemp

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
