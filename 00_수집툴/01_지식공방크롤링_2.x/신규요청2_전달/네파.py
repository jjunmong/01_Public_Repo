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

    outfile = codecs.open('nepa_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@네파\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'네파|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전국 점포정보 모두 얻을 수 있음
        #elif len(storeList) < 10: break

        #time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.nepamall.com'
    api = '/customer/shopList.do'
    #data = {}
    #params = urllib.urlencode(data)

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
    entity_list = tree.xpath('//div[@class="rs-list"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//span')
        if len(info_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '네파'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = '';          store_info['ot'] = ''
        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = entity_list[i].xpath('.//a/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('fncShopInfoView(')
            if idx != -1:
                strtemp = strtemp[idx+16:]
                idx = strtemp.rfind(')')
                subinfo_list = strtemp[:idx].split(',')
                if len(subinfo_list) >= 3:
                    store_info['pn'] = subinfo_list[2].replace('\'', '').lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

                if len(subinfo_list) >= 8:
                    store_info['xcoord'] = subinfo_list[len(subinfo_list)-1].replace('\'', '').lstrip().rstrip()
                    store_info['ycoord'] = subinfo_list[len(subinfo_list)-2].replace('\'', '').lstrip().rstrip()
                    store_info['ot'] = subinfo_list[len(subinfo_list) - 4].replace('\'', '').replace(' ', '').lstrip().rstrip()

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
