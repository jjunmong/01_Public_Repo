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

    outfile = codecs.open('benz_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|WEBSITE@@벤츠\n")

    outfile2 = codecs.open('benz_svc_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|WEBSITE@@벤츠서비스센터\n")


    page = 1
    while True:
        storeList = getStores2_1('')    # 전사장, 공식인증중고차전시장
        if storeList == None: break;

        for store in storeList:
            if store['subname'].find('서비스') != -1:
                outfile2.write(u'메르세데스벤츠|')
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s|' % store['ot'])
                outfile2.write(u'%s\n' % store['website'])
            else:
                outfile.write(u'메르세데스벤츠|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s\n' % store['website'])

        break;

    page = 1
    while True:
        storeList = getStores2_2('')    # 서비스센터
        if storeList == None: break;

        for store in storeList:
            if store['subname'].find('서비스') != -1:
                outfile2.write(u'메르세데스벤츠|')
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s|' % store['ot'])
                outfile2.write(u'%s\n' % store['website'])
            else:
                outfile.write(u'메르세데스벤츠|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s\n' % store['website'])

        break;

    outfile.close()
    outfile2.close()

# v2.0 (2019년4월)
def getStores2_1(type_info):  # 전시장, 공식인증중고차전시장
    # 'http://mbk-showroom.co.kr/'
    # 'http://mbk-showroom.co.kr/service/'
    url = 'http://mbk-showroom.co.kr'
    api = '/'
    data = {
     }
    params = urllib.urlencode(data)

    try:
        urls = url + api
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
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    subname_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="title"]')
    addr_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="address"]')
    ot_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="hours"]')
    pn_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="tel"]//a/@href')
    website_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="site"]')

    store_list = []
    for i in range(len(subname_list)):      # 웹사이트 있는 것들까지만 처리하면 됨 (나머지 것들은 공식인증 중고차 전시장)
        strtemp = "".join(subname_list[i].itertext())
        if strtemp == None: continue

        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
        if strtemp == '명칭': continue

        store_info = {}
        store_info['subname'] = strtemp.replace(' ', '/')

        if i < len(website_list):       # 공식전시장
            store_info['newaddr'] = '';
            strtemp = "".join(addr_list[i].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['newaddr'] = strtemp

            store_info['pn'] = ''
            strtemp = pn_list[i]
            if strtemp != None:
                strtemp = strtemp.replace('tel:', '').replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['pn'] = strtemp

            store_info['ot'] = '';
            strtemp = "".join(ot_list[i].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['ot'] = strtemp

            store_info['website'] = '';
            strtemp = "".join(website_list[i].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['website'] = strtemp

            store_list += [store_info]

        else:  # 공식인증중고차전시장
            store_info['subname'] = store_info['subname'].replace('전시장', '공식인증/중고차/전사장')

            store_info['newaddr'] = ''
            strtemp = addr_list[i].text
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['newaddr'] = strtemp

            store_info['pn'] = ''
            store_info['website'] = '';
            store_info['ot'] = '';

            strtemp = "".join(addr_list[i].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                idx = strtemp.find('Tel')
                if idx != -1: strtemp = strtemp[:idx].rstrip()
                idx = strtemp.find('월~')
                if idx != -1: store_info['ot'] = strtemp[idx:]
                else:
                    idx = strtemp.find('평일')
                    if idx != -1: store_info['ot'] = strtemp[idx:]

            temp_list = addr_list[i].xpath('.//a/@href')
            if len(temp_list) >= 1: store_info['pn'] = temp_list[0].replace('tel:', '')
            if len(temp_list) >= 2: store_info['website'] = temp_list[1]

            store_list += [store_info]

    return store_list

def getStores2_2(type_info):  # 서비스센터
    # 'http://mbk-showroom.co.kr/'
    # 'http://mbk-showroom.co.kr/service/'
    url = 'http://mbk-showroom.co.kr'
    api = '/service/'
    data = {
     }
    params = urllib.urlencode(data)

    try:
        urls = url + api
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
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    subname_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="title"]')
    addr_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="address"]')
    ot_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="hours"]')
    pn_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="tel"]//a/@href')
    website_list = tree.xpath('//div[@class="wpb_wrapper"]//p[@class="site"]')

    store_list = []
    for i in range(len(subname_list)):      # 웹사이트 있는 것들까지만 처리하면 됨 (나머지 것들은 공식인증 중고차 전시장)
        strtemp = "".join(subname_list[i].itertext())
        if strtemp == None: continue

        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
        if strtemp == '명칭': continue

        store_info = {}
        store_info['subname'] = strtemp.replace(' ', '/')

        if i < len(website_list):    # 서비스센터는 모두 다 else 조건
            store_info['newaddr'] = '';
            strtemp = "".join(addr_list[i].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['newaddr'] = strtemp

            store_info['pn'] = ''
            strtemp = pn_list[i]
            if strtemp != None:
                strtemp = strtemp.replace('tel:', '').replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['pn'] = strtemp

            store_info['ot'] = '';
            strtemp = "".join(ot_list[i].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['ot'] = strtemp

            store_info['website'] = '';
            strtemp = "".join(website_list[i].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['website'] = strtemp

            store_list += [store_info]

        else:  # 서비스센터
            #store_info['subname'] = store_info['subname'].replace('전시장', '공식인증/중고차/전사장')

            store_info['newaddr'] = ''
            strtemp = addr_list[i].text
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                store_info['newaddr'] = strtemp

            store_info['pn'] = ''
            store_info['website'] = '';
            store_info['ot'] = '';

            strtemp = "".join(addr_list[i].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                idx = strtemp.find('Tel')
                if idx != -1: strtemp = strtemp[:idx].rstrip()
                idx = strtemp.find('월~')
                if idx != -1: store_info['ot'] = strtemp[idx:]
                else:
                    idx = strtemp.find('평일')
                    if idx != -1: store_info['ot'] = strtemp[idx:]

            temp_list = addr_list[i].xpath('.//a/@href')
            if len(temp_list) >= 1: store_info['pn'] = temp_list[0].replace('tel:', '')
            if len(temp_list) >= 2: store_info['website'] = temp_list[1]

            store_list += [store_info]

    return store_list


# v1.0
def getStores(type_info):
    url = 'http://benzfs.com'
    api = '/locations/'
    data = {
     }
    params = urllib.urlencode(data)

    try:
        urls = url + api
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
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//div[@class="wpb_wrapper"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 4: continue     # 최소 항목 수 체크

        strtemp = "".join(info_list[0].itertext()).lstrip().rstrip()
        if strtemp == '명칭': continue

        store_info = {}
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = '';
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            store_info['newaddr'] = strtemp.rstrip().lstrip()

            store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            store_info['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
