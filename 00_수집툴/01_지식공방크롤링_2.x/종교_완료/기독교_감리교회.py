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
    '서울': '02',
}

sido_list = {
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

    outfile = codecs.open('church4_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|FEAT|SUBNAME|TELNUM|NEWADDR|FATHER|ORGNAME|SINCE|SOURCE2@@교회\n")

    for idx in range(1, 12):
        page = 1
        while True:
            store_list = getStores(idx, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['father'])
                outfile.write(u'%s|' % store['orgname'])
                outfile.write(u'%s|' % store['since'])
                outfile.write(u'%s\n' % u'기독교대한감리회')

            page += 1

            if page == 199: break
            elif len(store_list) < 18: break
            elif len(store_list) < 20:
                print('%d : %d' % (page-1, len(store_list)))

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(region_code, intPageNo):
    url = 'https://his.kmc.or.kr'
    api = '/address/church'
    data = {}
    data['search_ac'] = region_code
    data['page'] = intPageNo
    params = urllib.urlencode(data)

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
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="table-responsive"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 9: continue

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['orgname'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['orgname'] = strtemp
            if strtemp.endswith(')'):
                idx = strtemp.rfind('(')
                if idx != -1: strtemp = strtemp[:idx].rstrip()

            if strtemp == '소속없음': pass
            elif not strtemp.endswith('교회'): strtemp += '교회'
            store_info['name'] = strtemp

        store_info['type'] = '기독교대한감리회'

        store_info['father'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['father'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[6].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp == '': pass
            elif strtemp[0] >= '0' and strtemp[0] <= '9':  # 우편번호 정보 제거
                idx = strtemp.find(' ')
                if idx != -1: strtemp = strtemp[idx + 1:].lstrip()

            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[5].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.endswith(')'):
                idx = strtemp.rfind('(')
                if idx != -1: strtemp = strtemp[:idx].rstrip()

            store_info['pn'] = strtemp.replace('.', '-').replace(' ', '')

        store_info['since'] = ''
        strtemp = "".join(info_list[8].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['since'] = strtemp

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
