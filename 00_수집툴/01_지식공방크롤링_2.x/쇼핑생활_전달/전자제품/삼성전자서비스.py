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

    outfile = codecs.open('sec_svc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|NEWADDR|OT@@삼성전자서비스\n")

    page = 1
    notfound_flag = 0
    while True:
        time.sleep(random.uniform(0.3, 0.9))

        store_info = getStores(page)
        if store_info == None:
            notfound_flag += 1
            page += 1
            if notfound_flag > 5: break
            else : continue

        notfound_flag = 0

        store_info['id'] = page

        outfile.write(u'%s|' % store_info['name'])
        outfile.write(u'%s|' % store_info['subname'])
        outfile.write(u'%s|' % store_info['id'])
        outfile.write(u'%s|' % store_info['pn'])
        outfile.write(u'%s|' % store_info['addr'])
        outfile.write(u'%s|' % store_info['newaddr'])
        outfile.write(u'%s\n' % store_info['ot'])

        page += 1
        if page == 399: break       # 221 까지 있음

    outfile.close()

def getStores(intPageNo):
    # 'https://www.samsungsvc.co.kr/reserve/cenSearch.do?method=view&=1'
    url = 'https://www.samsungsvc.co.kr'
    api = '/reserve/cenSearch.do'
    data = {
        'method': 'view',
    }
    data['cenId'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #'Content-Length': '30',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_ga=GA1.3.1287419077.1524554970; _gid=GA1.3.259394370.1524554970; topKeyword=%EA%B0%A4%EB%9F%AD%EC%8B%9CS9%2C%20%ED%9C%B4%EB%8C%80%ED%8F%B0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%9D%B4%EB%8F%99%2C%20%EA%B0%A4%EB%9F%AD%EC%8B%9C%EB%85%B8%ED%8A%B88%2C%20%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84%20%EC%84%A4%EC%B9%98%2C%20%EC%84%B8%ED%83%81%EA%B8%B0%2C%20%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%20%ED%95%B4%EC%A0%9C%2C%20%EB%85%B8%ED%8A%B8%EB%B6%819%20Always; JSESSIONID_CSPN=Fc_272ooLetsrPOJ3Yen25pmJhEyp8cMyJLaL3jiI2s0IEoAHtN9!1580615182!NONE',
        'Host':'www.samsungsvc.co.kr',
        'Origin': 'https://www.samsungsvc.co.kr',
        'Referer': 'https://www.samsungsvc.co.kr/reserve/cenSearch.do?method=list&searchCondition=area',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
        urls = url + api + '?' + params
        print(urls)
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'utf-8')
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)

    name_list = tree.xpath('//div[@class="cen_result"]//p')
    info_list = tree.xpath('//div[@class="center_baseinfo"]//ul//li')

    if len(name_list) < 1 or len(info_list) < 2: return None

    store_info = {}

    store_info['name'] = '삼성전자서비스'
    store_info['subname'] = ''
    strtemp = name_list[0].text
    if strtemp != None:
        strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
        store_info['subname'] = strtemp.replace(' ', '/')

    store_info['pn'] = '1588-3366'
    strtemp = "".join(name_list[0].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        idx = strtemp.find('전화')
        if idx != -1:
            strtemp = strtemp[idx+2:].lstrip()
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

    store_info['newaddr'] = ''
    store_info['addr'] = ''
    strtemp = "".join(info_list[0].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
        word_list = strtemp.split(' ')
        if word_list >= 8:
            addr_header = word_list[0] + ' ' + word_list[1]
            idx = strtemp.rfind(addr_header)
            if idx > 2:
                store_info['addr'] = strtemp[:idx].rstrip()
                store_info['newaddr'] = strtemp[idx:].lstrip()
            else: store_info['addr'] = strtemp
        else: store_info['addr'] = strtemp

    store_info['ot'] = ''
    strtemp = "".join(info_list[1].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        if strtemp.startswith('서비스 가능시간'): strtemp = strtemp[8:].lstrip()
        store_info['ot'] = strtemp.replace(' ', '/')

    # 서비스 가능제품, 주차장 정보도 있음...

    return store_info


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
