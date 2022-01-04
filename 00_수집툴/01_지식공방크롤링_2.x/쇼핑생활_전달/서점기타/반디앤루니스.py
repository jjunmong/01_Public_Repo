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

    outfile = codecs.open('bandinlunis_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|OT\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'반디앤루니스|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['ot'])

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.bandinlunis.com'
    api = '/front/aboutBandi/aboutBandiMain.do'
    data = {
        'key': '50',
        'map': '170',
    }
    params = urllib.urlencode(data)
    # print(params)

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

    entity_list = tree.xpath('//dl[@class="gnb_layer_pop"]//a')

    result_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('./@href')
        if len(temp_list) == 0: continue

        strtemp = temp_list[0]
        subname = entity_list[i].text

        if strtemp.find('&map') == -1 or subname == None: continue

        time.sleep(random.uniform(0.3, 0.9))
        try:
            suburl = strtemp
            print(suburl)  # for debugging
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');      continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);      continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        store_info = {}
        store_info['subname'] = subname.lstrip().rstrip().replace(' ', '/')

        store_info['pn'] = ''
        store_info['addr'] = '';     store_info['ot'] = ''

        info_node = subtree.xpath('//div[@class="findmap"]/dl')
        if len(info_node) > 0:
            info_list = info_node[0].xpath('./dd')

            if len(info_list) < 3: continue  # 최소 3개 필드 있어야

            strtemp = "".join(info_list[1].itertext()).strip('\r\t\n')
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('('):
                    idx = strtemp.find(')')
                    strtemp = strtemp[idx+1:].lstrip()
                store_info['addr'] = strtemp

            strtemp = "".join(info_list[0].itertext()).strip('\r\t\n')
            if strtemp != None:
                idx = strtemp.find('/')
                if idx != -1: strtemp = strtemp[:idx].rstrip()
                store_info['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-').replace(' ', '')

            strtemp = "".join(info_list[2].itertext()).strip('\r\t\n')
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['ot'] = strtemp.replace(' ', '')

            result_list += [store_info]

    return result_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
