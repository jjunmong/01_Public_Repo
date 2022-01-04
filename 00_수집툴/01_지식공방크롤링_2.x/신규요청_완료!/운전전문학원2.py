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

    outfile = codecs.open('driving_school2_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@자동차운전학원\n")

    suburl_list = getSubUrlList()


    for suburl in sorted(suburl_list):
        page = 1
        while True:
            storeList = getStores(suburl, page)
            if storeList == None: break;

            for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['feat'])

            page += 1

            if page == 99: break
            elif len(storeList) < 15: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getSubUrlList():
    url = 'http://driveworld.kr/bbs/board.php?bo_table=seoul_list'

    try:
        print(url)     # for debugging
        result = urllib.urlopen(url)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    suburl_list = tree.xpath('//ul[@id="gnb_1dul"]//ul[@class="gnb_2dul"]//a/@href')

    return suburl_list


def getStores(suburl, intPageNo):
    # 'http://driveworld.kr/bbs/board.php?bo_table=gyeonggi_list&page=2'
    url = 'http://driveworld.kr' + suburl + '&page=' + str(intPageNo)

    try:
        print(url)     # for debugging
        result = urllib.urlopen(url)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//div[@class="contents"]')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//div')
        if len(info_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = ''
        store_info['subname'] = ''

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('학원위치'): strtemp = strtemp[4:].lstrip()
            if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''

        store_info['feat'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['feat'] = strtemp

        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find('학원(')
            if idx != -1 and strtemp.endswith(')'):     # '서울자동차운전전문학원(1종대형, 1종보통, 2종보통)'
                str_tempinfo = strtemp[idx+3:-1].replace(' ', '').replace(',', ':').replace('/', ':')
                strtemp = strtemp[:idx+2]
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += str_tempinfo

            store_info['name'] = strtemp

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
