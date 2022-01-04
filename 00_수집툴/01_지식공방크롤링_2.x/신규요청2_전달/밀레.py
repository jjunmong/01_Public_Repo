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

    outfile = codecs.open('millet_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|TELNUM|NEWADDR|FEAT@@밀레\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'밀레|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 99: break
        elif len(storeList) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # http://www.millet.co.kr/front/ctl_ridge_customer/offline_store?&pageNo=2
    url = 'http://www.millet.co.kr'
    api = '/front/ctl_ridge_customer/offline_store'
    data = {}
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)

    try:
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
    entity_list = tree.xpath('//table[@class="table text-center order-list store-list"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '밀레'

        store_info['type'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['subname'] = ''
        store_info['feat'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('['):
                strtemp = strtemp[1:].lstrip()
                idx = strtemp.find(']')
                if idx != -1:
                    store_info['type'] = strtemp[:idx].rstrip()
                    strtemp = strtemp[idx+1:].lstrip()

            if strtemp.startswith('밀레'): strtemp = strtemp[2:].lstrip()

            if strtemp.endswith('(원스톱)'):
                strtemp = strtemp[:-5].rstrip()
                store_info['feat'] = '원스톱'
            if strtemp.endswith('(신규)'):
                strtemp = strtemp[:-4].rstrip()
                store_info['feat'] = '신규대리점'
            if strtemp.endswith('(신)'):
                strtemp = strtemp[:-3].rstrip()
                store_info['feat'] = '신규대리점'

            if not strtemp.endswith('점'): strtemp += '점'

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        addr_list = info_list[2].xpath('.//p')
        if len(addr_list) > 0: store_info['newaddr'] = addr_list[0].text.lstrip().rstrip()

        store_info['pn'] = ''
        pn_list = info_list[2].xpath('.//small')
        if len(pn_list) > 0:
            strtemp = pn_list[0].text.lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')
            if strtemp.find('개설중') != -1: strtemp = ''
            store_info['pn'] = strtemp

        store_info['id'] = ''
        temp_list = info_list[3].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('shop_id=')
            if idx != -1:
                strtemp = strtemp[idx+8:]
                idx = strtemp.find('&')
                if idx != -1:
                    store_info['id'] = strtemp[:idx]

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
