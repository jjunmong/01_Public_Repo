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

    outfile = codecs.open('abcmart_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|FEAT@@ABC마트\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'ABC마트|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 29: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(page_no):
    url = 'http://www.abcmart.co.kr'
    api = '/abc/customer/sortAreaList'
    data = {
        'sort': '',
        'gu': '',
        'gbnSort': '',
        'gbnSort1': '',
        'gbnSort2': '',
        'gbnSort3': '',
        'gbnSort4': '',
        'wearSellYn': '',
        'chngRfndYn': '',
        'giftCardUseYn': '',
        'pointUseYn': '',
        'okcashbackUseYn': '',
        #'searchValue': '',
    }
    data['page'] = str(page_no)
    #data['searchValue'] = ''
    params = urllib.urlencode(data) + '&searchValue='
    print(params)

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'max-age=0',
        'Content-Length': '146',
        'Host': 'www.abcmart.co.kr',
        'Origin': 'https://www.abcmart.co.kr',
        'Referer': 'https://www.abcmart.co.kr/abc/customer/sortAreaList',
        #'Cookie': 'JSESSIONID=ecf4i-qnzSEL-_5idTPQv; _pk_ref.141974880.ecc3=%5B%22%22%2C%22%22%2C1488905844%2C%22https%3A%2F%2Fwww.google.co.kr%2F%22%5D; _gat=1; _ga=GA1.3.765350052.1488905845; wcs_bt=s_2d9add6589e:1488907010; _pk_id.141974880.ecc3=b150353008a8f3e4.1488905844.1.1488907011.1488905844.; _pk_ses.141974880.ecc3=*; _HCVar_abcmart1=intTstFirstCnnabcmart1%7Cundefined%2Cstime_abcmart1%7C1488907010994%2CHLogedabcmart1%7CY',
    }

    try:
        #result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)  # for debugging
        result = urllib.urlopen(urls)

        #req = urllib2.Request(url + api, params, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        #req.get_method = lambda: 'POST'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//section[@class="table_basic no_point mt10 clearbox"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 4: continue  # 4개 필드 있음

        strtemp = "".join(info_list[1].itertext())
        temp_list = info_list[1].xpath('.//p')
        if len(temp_list) < 2: continue
        subname = temp_list[0].text
        pn = temp_list[1].text
        if subname == None or pn == None: continue
        subname = subname.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
        pn = pn.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
        strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
        idx = strtemp.find(pn)
        if idx != -1:
            strtemp = strtemp[:idx].rstrip()
        idx = strtemp.find(subname)
        addr = strtemp[idx+len(subname):].lstrip()

        store_info = {}

        store_info['subname'] = subname.replace(' ', '/')
        store_info['pn'] = pn.replace(' ', '').replace('.', '-').replace(')', '-')
        store_info['addr'] = addr

        store_info['feat'] = ''
        feat_list = info_list[2].xpath('.//span')
        for j in range(len(feat_list)):
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_list[j].text

        # 상세정보 페이지에 x/y 좌표정보 있음

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
