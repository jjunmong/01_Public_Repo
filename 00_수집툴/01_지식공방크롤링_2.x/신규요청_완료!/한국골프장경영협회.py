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

    outfile = codecs.open('kgba_new_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|OFFDAY@@골프장\n")

    page = 1
    while True:
        storeList = getStoresNew(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            if store.get('size'):
                outfile.write(u'%s|' % store['size'])
            elif store.get('feat'):
                outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s\n' % store['offday'])

        page += 1

        if page == 2: break     # 한번 호출로 다 얻어옴
        elif len(storeList) < 7: break

        time.sleep(random.uniform(0.5, 1.5))

    outfile.close()


def getStores(intPageNo):
    url = 'http://www.kgba.co.kr'
    api = '/GolfCourse/Index.asp'
    data = {
    }
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//table[@width="478"]//td')

    store_list = []
    for i in range(len(entity_list)):
        info_node = entity_list[i].xpath('.//a')
        if len(info_node) < 1: continue

        temp_list = info_node[0].xpath('./@onclick')
        name = info_node[0].text

        if len(temp_list) < 1 or name == None: continue
        strtemp  = temp_list[0]
        if strtemp.find('id=') == -1: continue      # 골프장 정보를 수록한 노드인지 체크

        store_info = {}
        store_info['size'] = ''
        name = name.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
        idx = name.find('(')
        if idx != -1:
            store_info['size'] = name[idx+1:-1]
            name = name[:idx].rstrip()
        store_info['name'] = name.rstrip().lstrip().replace(' ', '/')
        store_info['subname'] = ''

        store_info['pn'] = ''
        store_info['newaddr'] = '';        store_info['offday'] = ''

        strtemp  = temp_list[0]
        idx = strtemp.find('id=')
        strtemp = strtemp[idx+3:]
        idx = strtemp.find('\'')
        strtemp = strtemp[:idx]

        subdata = {}
        subdata['id'] = strtemp
        subparams = urllib.urlencode(subdata)

        time.sleep(random.uniform(0.3, 1.1))
        try:
            suburl = url + '/GolfCourse/detail.asp' + '?' + subparams
            print(suburl)  # for debugging
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');
            store_list += [store_info];   continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);
            store_list += [store_info];            continue

        subresponse = subresult.read()
        subresponse = unicode(subresponse, 'euc-kr')
        #print(response)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//table[@width="393"]//tr[@height="27"]')
        for j in range(len(subinfo_list)):
            strtemp = "".join(subinfo_list[j].itertext())
            strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            if strtemp.find('연락처') != -1:   # '올드(033)245-7000 / 듄스(033)245-7100' 이렇게 기술된 경우 1건 있음
                idx = strtemp.find('연락처')
                strtemp = strtemp[idx+3:].lstrip()
                if strtemp.startswith('('): strtemp = strtemp[1:].lstrip()
                store_info['pn'] = strtemp.replace('.', '-').replace('(', '').replace(')', '-').replace(' ', '')
            elif strtemp.startswith('주소'):
                strtemp = strtemp[2:].lstrip()
                store_info['newaddr'] = strtemp
            elif strtemp.startswith('규모'):
                strtemp = strtemp[2:].lstrip()
                store_info['size'] = strtemp
            elif strtemp.startswith('정기휴장일'):
                strtemp = strtemp[5:].lstrip()
                store_info['offday'] = strtemp

            # 가격, 회원수 등 기타 정보 많음 (필요할 때 추출할 것!!)

        store_list += [store_info];

    return store_list

# 'http://www.kgba.co.kr/GolfCourse/Member.asp' 사이트에서 한번에 크롤링 가능...
def getStoresNew(intPageNo):
    url = 'http://www.kgba.co.kr'
    api = '/GolfCourse/Member.asp'
    data = {
    }
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//table[@style="word-break:break-all;"]//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 8: continue  # 최소 8개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''

        name_list = info_list[1].xpath('.//a')
        if len(name_list) < 1: continue

        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp == u'골프장명': continue

            store_info['name'] = strtemp.replace(' ', '/')

        store_info['feat'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp != '':
                store_info['feat'] += '회원제:' + strtemp

        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp != '':
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += '퍼블릭:' + strtemp

            if strtemp == u'골프장명': continue

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[6].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[7].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find('연락처')
            if strtemp.find('연락처') != -1:
                strtemp = strtemp[idx+3:].lstrip()

            # '올드(033)245-7000 / 듄스(033)245-7100' 이렇게 기술된 경우 1건 있음
            store_info['pn'] = strtemp.replace('.', '-').replace('(', '').replace(')', '-').replace(' ', '')

        store_info['offday'] = ''

        store_list += [store_info];

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
