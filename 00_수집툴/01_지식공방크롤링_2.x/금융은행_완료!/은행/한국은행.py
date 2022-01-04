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

    outfile = codecs.open('bankofkorea_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@한국은행\n")

    # 본부, 지역본부 정보 얻기
    #store_list = getStores('http://www.bok.or.kr/map/region_map.action?menuNaviId=449')     # 한번 호출로 한국은행 전국 지역본부 목록을 얻을 수 있음
    store_list = getStores('http://www.bok.or.kr/portal/submain/submain/rgHqt.do?menuNo=200219')     # 한번 호출로 한국은행 전국 지역본부 목록을 얻을 수 있음
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

    time.sleep(random.uniform(0.3, 0.9))

    # 본부 정보 얻기
    # ...

    # 인재개발원 정보 얻기
    store_list = getStores2('http://www.bok.or.kr/portal/main/contents.do?menuNo=200508')
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

    outfile.close()

# v2.0 (2018/7)
def getStores(urls):
    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        print(urls)     # for debugging
        req = urllib2.Request(urls, None, headers=hdr)
        #req = urllib2.Request(urls, None)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="tabCont"]//div[@class="txt"]')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//p')
        if len(info_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '한국은행'

        store_info['subname'] = ''
        store_info['pn'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            idx = strtemp.find('Tel.')
            if idx != -1:
                store_info['subname'] = strtemp[:idx].replace('[', '').replace(']', '').lstrip().rstrip().replace(' ', '/')
                strtemp = strtemp[idx+4:].lstrip()
                store_info['pn'] = strtemp
            else:
                store_info['subname'] = strtemp[:idx].lstrip().rstrip().replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            if strtemp.startswith('['):
                idx = strtemp.find(']')
                if idx != -1:
                    strtemp = strtemp[idx+1:].lstrip()

            store_info['newaddr'] = strtemp

        store_list += [store_info]

    # 본부 정보 추출
    info_list = tree.xpath('//div[@class="addressSet"]//address')
    if len(info_list) > 0:
        store_info = {}
        store_info['name'] = '한국은행'

        store_info['subname'] = '본부'
        store_info['newaddr'] = ''
        store_info['pn'] = ''
        strtemp = info_list[0].text
        #strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            idx = strtemp.find('/')
            if idx != -1:
                str_newaddr = strtemp[:idx].rstrip()
                str_pn = strtemp[idx+1:].lstrip()
                if str_newaddr.startswith('['):
                    idx = str_newaddr.find(']')
                    if idx != -1:
                        str_newaddr = str_newaddr[idx + 1:].lstrip()

                store_info['newaddr'] = str_newaddr

                if str_pn.startswith('대표전화'): str_pn = str_pn[4:].lstrip()
                if str_pn.startswith(':'): str_pn = str_pn[1:].lstrip()
                store_info['pn'] = str_pn

        store_list += [store_info]

        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            idx = strtemp.find('[임시 본부]')
            if idx != -1:
                strtemp = strtemp[idx+7:].lstrip()
                str_pn = store_info['pn']

                store_info = {}
                store_info['name'] = '한국은행'
                store_info['subname'] = '임시본부'
                store_info['pn'] = str_pn
                store_info['newaddr'] = ''

                if strtemp.startswith('('):
                    idx = strtemp.find(')')
                    if idx != -1:
                        strtemp = strtemp[idx+1:].lstrip()

                store_info['newaddr'] = strtemp
                store_list += [store_info]

    return store_list

def getStores2(urls):
    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        print(urls)     # for debugging
        req = urllib2.Request(urls, None, headers=hdr)
        #req = urllib2.Request(urls, None)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="bankMap"]')

    store_list = []
    for i in range(len(entity_list)):
        name_list = entity_list[i].xpath('.//img/@alt')
        tag_list = entity_list[i].xpath('.//dl//dt')
        value_list = entity_list[i].xpath('.//dl//dd')
        if len(name_list) < 1 or len(tag_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '한국은행'

        store_info['subname'] = ''
        strtemp = name_list[0]
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('한국은행', '').replace('전경사진', '').lstrip().rstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = '';     store_info['pn'] = ''

        for j in range(len(tag_list)):
            tag = "".join(tag_list[j].itertext())
            value = "".join(value_list[j].itertext())
            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').lstrip().rstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

            if tag == '주소': store_info['newaddr'] = value
            elif tag == '전화번호': store_info['pn'] = value

        store_list += [store_info]

    return store_list


# v1.0
'''
def getStores(urls):
    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        print(urls)     # for debugging
        req = urllib2.Request(urls, None, headers=hdr)
        #req = urllib2.Request(urls, None)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="bankMap"]')

    store_list = []
    for i in range(len(entity_list)):
        name_list = entity_list[i].xpath('.//img/@alt')
        tag_list = entity_list[i].xpath('.//dl//dt')
        value_list = entity_list[i].xpath('.//dl//dd')
        if len(name_list) < 1 or len(tag_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '한국은행'

        store_info['subname'] = ''
        strtemp = name_list[0]
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('한국은행', '').replace('전경사진', '').lstrip().rstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = '';     store_info['pn'] = ''

        for j in range(len(tag_list)):
            tag = "".join(tag_list[j].itertext())
            value = "".join(value_list[j].itertext())
            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').lstrip().rstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

            if tag == '주소': store_info['newaddr'] = value
            elif tag == '전화번호': store_info['pn'] = value

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
