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

    outfile = codecs.open('kdbbank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR@@KDB산업은행\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 49: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.kdb.co.kr'
    api = '/ih/simpleJsp.do?actionId=ADIHIHIRBBF02'
    data = {
        'orgC': '001',
        'bbrSeq': '',
        'searchSort': '',
        'mapType': '',
        'mapIdNum': '',
        'pageGbn': '',
        'vipSetuYn': '',
        'pop': '',
        'srchDetailGbn': '',
        'wonhwa': '',
        'lseSfeYn': '',
        'searchArea': '',
    }
    data['pageIndex'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '576',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JEX_LANG=KO; JEX_LOCAL_LANG=KO; PCID=15635265843634695018691; RC_RESOLUTION=1920*1080; RC_COLOR=24; PHAROSVISITOR=026201d0016db46753ca21a30a06325b; JSESSIONID_CHP=1dXuaxgb280wAvfpSWMtk8FPWhShFtp5V0Ii3s6m8tF0kZpuythItLaBd3jtLslQ.UEhNUF9Eb21haW4vQ0hQX01TMTM=',
        'Host': 'www.kdb.co.kr',
        'Origin': 'https://www.kdb.co.kr',
        'pragma': 'no-cache',
        'Referer': 'https://www.kdb.co.kr/CHBIBI21N00.act?_mnuId=IHIHIR0022',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)
        req = urllib2.Request(url + api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)
    #tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="board_list"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = 'KDB산업은행'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('['):
                idx = strtemp.find(']')
                strtemp = strtemp[idx+1:].lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = info_list[4].xpath('.//a/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('Branch(')
            if idx != -1:
                strtemp = strtemp[idx+7:]
                idx = strtemp.find(')')
                store_info['id'] = strtemp[:idx][1:-1]

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
