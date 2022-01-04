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

    outfile = codecs.open('stock_yuwha_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@유화증권\n")

    while True:
        store_list = getStores()
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        break

    outfile.close()


def getStores():
    url = 'http://www.yhs.co.kr'
    api = '/company/branch_headoffice.asp'
    data = {}
    params = urllib.urlencode(data)
    #print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, None, headers=hdr)
        req = urllib2.Request(url+api, None)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)

        #urls = url + api
        #print(urls)     # for debugging
        #result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    tree = html.fromstring(response)
    subname_list = tree.xpath('//ul[@class="content-tab"]//li//a//img/@alt')
    subapi_list = tree.xpath('//ul[@class="content-tab"]//li//a/@href')

    store_list = []
    for i in range(len(subapi_list)):
        subapi = subapi_list[i]
        if subapi == None: continue

        suburl = url + subapi
        print(suburl)

        try:
            time.sleep(random.uniform(0.3, 0.9))
            subreq = urllib2.Request(suburl, None)
            subreq.get_method = lambda: 'GET'
            subresult = urllib2.urlopen(subreq)

            #subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');      continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);     continue

        subresponse = subresult.read()
        #print(subresponse)

        subtree = html.fromstring(subresponse)
        info_list = subtree.xpath('//div[@class="branch_list namum"]//p')

        if len(info_list) < 2: continue

        store_info = {}
        store_info['name'] = '유화증권'
        store_info['subname'] = ''
        strtemp = subname_list[i]
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('·', ' ').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('('):     # 우편번호 정보 없앰
                idx = strtemp.find(')')
                strtemp = strtemp[idx+1:].lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip().upper()
            if strtemp.startswith('TEL'): strtemp = strtemp[3:].lstrip()
            if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
            idx = strtemp.find(',')
            if idx != -1: strtemp = strtemp[:idx].rstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_list += [store_info]

    # 본점 정보 더하기
    info_list = tree.xpath('//div[@class="branch_list namum"]//p')

    if len(info_list) < 2: return store_list

    store_info = {}
    store_info['name'] = '유화증권'
    store_info['subname'] = '본사'

    store_info['newaddr'] = ''
    strtemp = "".join(info_list[0].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        if strtemp.startswith('('):     # 우편번호 정보 없앰
            idx = strtemp.find(')')
            strtemp = strtemp[idx+1:].lstrip()
        store_info['newaddr'] = strtemp

    store_info['pn'] = ''
    strtemp = "".join(info_list[1].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip().upper()
        if strtemp.startswith('TEL'): strtemp = strtemp[3:].lstrip()
        if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
        idx = strtemp.find(',')
        if idx != -1: strtemp = strtemp[:idx].rstrip()
        store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

    store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
