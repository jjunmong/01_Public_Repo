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

    outfile = codecs.open('heungkuklife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR@@흥국생명\n")

    for i in range(0, 16, 1):
        page = 1
        while True:
            store_list = getStores(i, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s\n' % store['newaddr'])

            page += 1

            if page == 19: break
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_num, intPageNo):
    url = 'https://www.heungkuklife.co.kr'
    api = '/front/help/branchListAjax.do'
    data = {
        'sub_region_nm': '',
        'searchWord': '',
        'type_code': '',
    }
    data['region_num'] = sido_num
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    try:
        urls = url + api
        print(urls)
        req = urllib2.Request(urls, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@class="table_type01"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue

        store_info = {}

        store_info['name'] = '흥국생명'
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = '';
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace(' ', '').replace('.', '-').replace(')', '-')

        store_info['id'] = ''
        temp_list = info_list[4].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('doMapView(')
            if idx != -1:
                strtemp = strtemp[idx+10:].lstrip()
                idx = strtemp.find(');')
                if idx != -1:
                    store_info['id'] = strtemp[:idx][1:-1]

        if store_info['id'] != '':
            suburls = 'https://www.heungkuklife.co.kr/front/help/branchPlazaView.do?num_seq=' + store_info['id']

            try:
                print(suburls)      # for debugging
                time.sleep(random.uniform(0.3, 0.9))
                subresult = urllib.urlopen(suburls)
            except:
                print('Error calling the subAPI')
                store_list += [store_info];     continue

            code = subresult.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code);
                store_list += [store_info];     continue

            subresponse = subresult.read()
            subresponse = unicode(subresponse, 'euc-kr')
            # print(subresponse)
            subtree = html.fromstring(subresponse)
            subinfo_list = subtree.xpath('//table[@class="table_input"]//tbody//tr')
            for j in range(len(subinfo_list)):
                tag_list = subinfo_list[j].xpath('.//th')
                value_list = subinfo_list[j].xpath('.//td')

                if len(tag_list) < 1 or len(value_list) < 1: continue

                tag = "".join(tag_list[0].itertext())
                value = "".join(value_list[0].itertext())

                if tag == None or value == None: continue

                tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

                if tag.startswith('주소'):
                    store_info['newaddr'] = value

            # subresponse 문자열열에서 좌표값도 얻을 수 있음

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
