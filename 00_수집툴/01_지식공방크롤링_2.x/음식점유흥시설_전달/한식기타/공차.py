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

    outfile = codecs.open('gongcha_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|FEAT\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        break   # 한번 호출로 전국 점포 모두 얻을 수 있음

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.gong-cha.co.kr'
    api = '/brand/store/store.php?m=l'
    data = {
        'sido': '',
        'etc9': '',
        'etc10': '',
        'subject': '',
    }
    params = urllib.urlencode(data)
    #print(params)

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=sm7h8s2duqhbeq90qhdo1cp555; 2a0d2363701f23f8a75028924a3af643=MTI1LjEyOS4yNDIuMjI3; _gat=1; _ga=GA1.3.1065939222.1486961929'
    }
    try:
        req = urllib2.Request(url + api, params)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)

    entity_list = tree.xpath('//li')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//span')
        if len(info_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '공차'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        store_info['feat'] = '';    store_info['id'] = ''

        temp_list = entity_list[i].xpath('.//a/@store')
        if len(temp_list) > 0:
            store_info['id'] = temp_list[0]

        # 상세정보 페이지 호출
        if store_info['id'] != '':
            suburls = 'http://www.gong-cha.co.kr/brand/store/view.php?m=s&no=' + store_info['id']
            print(suburls)
            try:
                time.sleep(random.uniform(0.3, 0.9))
                subresult = urllib.urlopen(suburls)
            except:
                print('Error calling the subAPI');
                store_list += [store_info];     continue

            code = subresult.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code);
                store_list += [store_info];      continue

            subresponse = subresult.read()
            #print(subresponse)
            #subtree = html.fromstring(subresponse)
            subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)

            subinfo_list = subtree.xpath('//div[@class="contents"]//tbody//tr//td')
            if len(subinfo_list) >= 2:
                strtemp = "".join(subinfo_list[1].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    if strtemp == '-' or strtemp == '미설치' or strtemp == '없음': strtemp = ''
                    store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

            feat_list = subtree.xpath('//div[@class="service"]//img/@alt')
            for j in range(len(feat_list)):
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += feat_list[j]

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
