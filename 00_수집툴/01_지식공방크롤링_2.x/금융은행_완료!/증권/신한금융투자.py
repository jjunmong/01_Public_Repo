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

    outfile = codecs.open('shinhaninvest_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR@@신한금융투자\n")

    # 지점 정보 얻기
    store_list = getStores('B')
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

    time.sleep(random.uniform(0.3, 0.9))

    # PWM센터 정보 얻기
    store_list = getStores('W')
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

    time.sleep(random.uniform(0.3, 0.9))

    # PWM 라운지 정보 얻기
    store_list = getStores('I')
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

    outfile.close()


def getStores(store_type):
    url = 'http://bbs2.shinhaninvest.com'
    api = '/branch/list.do'
    data = {
        'gubun': 'new_ir',
    }
    data['variableField1'] = store_type        # W, B, I
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        urls = url + api + '?' + params
        print(urls)  # for debugging
        result = urllib.urlopen(urls)
        # urllib2 로 호출하면 'W', "B', 'I'로 호출했는데 'B'만 3번 호출됨 (???)
        #req = urllib2.Request(url + api, params, headers=hdr)
        #req = urllib2.Request(url + api, params)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue  # 최소 필드 수 체크

        base_idx = 0
        if len(info_list) == 5: base_idx = 1

        store_info = {}
        store_info['name'] = '신한금융투자'

        store_info['subname'] = ''
        strtemp = "".join(info_list[base_idx+0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if store_type == 'B':   # 지점
                if strtemp.endswith('센터'): pass
                elif strtemp.endswith('본사'): pass
                elif not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[base_idx+1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[base_idx+2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = info_list[base_idx+0].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('net/')
            if idx != -1:
                strtemp = strtemp[idx+4:]
                idx = strtemp.find('\'')
                strtemp = strtemp[:idx]
                idx = strtemp.find('mapid=')
                if idx != -1: strtemp = strtemp[idx+6:]
                store_info['id'] = strtemp

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
