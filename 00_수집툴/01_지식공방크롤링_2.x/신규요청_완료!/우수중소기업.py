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
    '대전': '06',
}

sido_list = {
    '서울': '01',
    '광주': '05',
    '대구': '03',
    '대전': '06',
    '부산': '02',
    '울산': '07',
    '인천': '04',
    '경기': '09',
    '강원': '08',
    '경남': '10',
    '경북': '11',
    '전남': '12',
    '전북': '13',
    '충남': '15',
    '충북': '16',
    '제주': '14',
    '세종': '17'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('sme_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@우수중소기업\n")

    for sido_name in sorted(sido_list):
        page = 1
        while True:
            storeList = getStores(sido_list[sido_name], sido_name, page)
            if storeList == None: break;

            for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['feat'])

            page += 1

            if page == 999: break  # 2018년8월 기준 ??? page까지 있음
            elif len(storeList) < 50: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_code, sido_name, intPageNo):
    url = 'http://sminfo.mss.go.kr'
    api = '/gc/ei/GEI002R0.do'
    data = {
        'mode': '',
        'kedcd': '',
        'cmMenuId': '',
        'clickcontrol': 'disable',
        'locSrchCd': '2',
        'gugunCd': '',
        'gugunNm': '',
        'gugunNm2': '',
        'cmQueryOption': '07',
        'cmTotalRowCount': '',
        'cmSortField': '',
        'cmSortOption': '0',
        'tITLESortOption': '2',
        'bZNOSortOption': '2',
        'returnUrl': '',
        'returnCmMenuId': '',
        'iqFlag': 'S',
        'gugunRadio': '',
        'cmRowCountPerPage': '50',
    }
    data['sidoCd'] = sido_code
    data['sidoNm'] = sido_name
    data['cmQuery'] = sido_name
    data['cmPageNo'] = intPageNo
    params = urllib.urlencode(data)
    print('%s, %s, %d' % (sido_name, sido_code, intPageNo))
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #response = unicode(response, 'euc-kr')
    #print(response)
    response = removeComments(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//table[@class="table type3"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = ''
        store_info['subname'] = ''

        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['name'] = strtemp

        store_info['newaddr'] = ''
        temp_list = info_list[4].xpath('.//p')
        if len(temp_list) > 0:
            strtemp = temp_list[0].text
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['newaddr'] = strtemp

        if store_info['newaddr'] == '':
            strtemp = "".join(info_list[4].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['newaddr'] = strtemp

        store_info['feat'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['feat'] = strtemp

        store_info['pn'] = ''

        store_list += [store_info]

    return store_list

def removeComments(src):
    str_org = src
    result = ''
    while True:
        idx = src.find('<!--')
        if idx != -1:
            result += src[:idx]
            src = src[idx+4:]
            idx = src.find('-->')
            if idx == -1:
                return str_org
            else:
                src = src[idx+3:]
        else:
            result += src
            break

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
