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
import ast
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

    outfile = codecs.open('insurance_dgb_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@DGB생명\n")

    # 지점 정보
    store_list = getStores('https://www.dgbfnlife.com/BD/BD_A072.do')
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    time.sleep(random.uniform(0.3, 0.9))

    # 본사 정보
    store_list = getStores2('https://www.dgbfnlife.com/BD/BD_A070.do', '서울본사')
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    store_list = getStores2('https://www.dgbfnlife.com/BD/BD_A071.do', '부산본사')
    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    outfile.close()

def getStores(urls):
    try:
        print(urls)
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//div[@class="section"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = 'DGB생명'

        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = '';      store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = info_list[1].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('doDetail(')
            if idx != -1:
                strtemp = strtemp[idx+9:]
                idx = strtemp.find(')')
                store_info['id'] = strtemp[:idx][1:-1]

        if store_info['id'] != '':
            suburls = 'https://www.dgbfnlife.com/BD/BD_A073.do'
            subparams = 'branchcode=' + store_info['id']
            print(suburls + ' ' + subparams)

            try:
                time.sleep(random.uniform(0.3, 0.9))
                subreq = urllib2.Request(suburls, subparams)
                subreq.get_method = lambda: 'POST'
                subresult = urllib2.urlopen(subreq)
            except:
                print('Error calling the subAPI');
                store_list += [store_info];                continue

            code = subresult.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code);
                store_list += [store_info];                continue

            subresponse = subresult.read()
            #print(subresponse)

            idx = subresponse.find('.LatLng(')
            if idx != -1:
                strtemp = subresponse[idx+8:].lstrip()
                idx = strtemp.find(')')
                temp_list = strtemp[:idx].split(',')
                if len(temp_list) >= 2:
                    store_info['xcoord'] = temp_list[1].lstrip().rstrip()
                    store_info['ycoord'] = temp_list[0].lstrip().rstrip()

        store_list += [store_info]

    return store_list

# 본사 정보 수집
def getStores2(urls, store_subname):
    try:
        print(urls)
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    info_list = tree.xpath('//div[@class="section"]//ul[@class="blt_arrow"]//li')

    if len(info_list) < 2: return None

    store_list = []
    store_info = {}
    store_info['name'] = 'DGB생명'
    store_info['subname'] = store_subname.replace(' ', '/')

    store_info['newaddr'] = ''
    strtemp = "".join(info_list[0].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        idx = strtemp.find(':')
        if idx != -1: strtemp = strtemp[idx+1:]
        store_info['newaddr'] = strtemp

    store_info['pn'] = ''
    strtemp = "".join(info_list[1].itertext())
    if strtemp != None:
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
        idx = strtemp.find(':')
        if idx != -1: strtemp = strtemp[idx+1:]
        store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

    store_info['id'] = '';      store_info['xcoord'] = '';      store_info['ycoord'] = ''

    store_list += [store_info]
    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
