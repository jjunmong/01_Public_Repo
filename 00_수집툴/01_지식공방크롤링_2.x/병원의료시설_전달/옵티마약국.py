# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
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

    outfile = codecs.open('optimacare_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|X|Y@@옵티마약국\n")

    page = 1
    retry_count = 0
    while True:
        store_list = getStores(page)
        if store_list == None:
            if retry_count >= 3: break
            else: retry_count += 1; continue

        retry_count = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 199: break       # 2018년6월 41 있음
        elif len(store_list) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://www.optimacare.co.kr/Pharmacy/List'
    url = 'http://www.optimacare.co.kr'
    api = '/Pharmacy/List'
    data = {
        'PageSize': '15',
    }
    data['Page'] = intPageNo
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #response = unicode(response, 'euc-kr')
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)

    entity_list = tree.xpath('//table[@class="board-list"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith(')'):
                idx = strtemp.rfind('(')
                if idx != -1: strtemp = strtemp[:idx].rstrip()

            if strtemp.endswith('약국') and strtemp.find('옵티마') == -1:
                strtemp = strtemp[:-2] + ' 옵티마약국'
                strtemp = strtemp.replace('  ', ' ')
            elif strtemp.endswith('옵티마'):
                strtemp = strtemp[:-3] + ' 옵티마약국'
                strtemp = strtemp.replace('  ', ' ')
            elif strtemp.endswith('옵티마약국'):
                strtemp = strtemp[:-5] + ' 옵티마약국'
                strtemp = strtemp.replace('  ', ' ')

            store_info['name'] = strtemp.replace(' ', '/')

        store_info['addr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        # suburl에 WGS84 좌표정보 있음 (나중에 필요할 때 추출할 것!)
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
