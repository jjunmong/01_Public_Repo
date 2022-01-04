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

    outfile = codecs.open('goobne_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@굽네치킨\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;
        elif len(storeList) == 0: break;

        for store in storeList:
            outfile.write(u'굽네치킨|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 999: break
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.goobne.co.kr'
    api = '/get.do?callback=jQuery11240011469600411261327_1505029352478'
    data = {
        'ex': 'Store',
        'ac': 'selectStore',
        'lat': '36.1919362266',
        'lng': '127.0923767491',
        'sGubun': '0',
        'sSelsi': '',
        'sSelgu': '',
        'sText': '',
    }
    data['sPage'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    # header 잘못 설정하면 api 호출 오류 발생, 아래 조합은 동작함 (2017년9월 기준)
    hdr = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        #'Accept-Encoding': 'None',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        #'Content-Length': '100',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=A40238840A7451F3372898F5D0239FC8; _ga=GA1.3.841758395.1615187481; _gid=GA1.3.475766377.1615187481',
        #'Host': 'www.goobne.co.kr',
        #'Origin': 'http://www.goobne.co.kr',
        #'Referer': 'http://www.goobne.co.kr/store/search_store.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        #'X-Requested-With,': 'XMLHttpRequest',
    }

    try:
        req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url + api, params, headers=None)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    print(response)
    response = response.lstrip().rstrip()
    idx = response.find('([{')
    if idx == -1: return None
    response = response[idx+1:-1]

    #2020/03/08 strict=False 코드 추가함 // 해당 코드 추가시 json에서 허용하지 않는 문자열도 읽어 들임.
    entity_list = json.loads(response, strict=False)
    if entity_list == None: return None

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '굽네치킨'
        store_info['id'] = entity_list[i]['a_branch_id']

        strtemp = entity_list[i]['a_branch_nm'].lstrip().rstrip()
        store_info['subname'] = strtemp.replace(' ', '/')

        strtemp = entity_list[i]['a_branch_addr']
        if strtemp != None: strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        else: strtemp = ''
        store_info['newaddr'] = strtemp

        store_info['pn'] = entity_list[i]['a_branch_tel'].replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['ot'] = '주중:' + entity_list[i]['a_week_starttime'] + '-' + entity_list[i]['a_week_endtime']
        store_info['ot'] += ';주말:' + entity_list[i]['a_end_starttime'] + '-' + entity_list[i]['a_end_endtime']
        store_info['ot'] = store_info['ot'].replace('0000', ':00').replace('NULL-NULL', 'N/A').replace(':-', ':N/A')

        store_info['xcoord'] = entity_list[i]['lng']
        store_info['ycoord'] = entity_list[i]['lat']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
