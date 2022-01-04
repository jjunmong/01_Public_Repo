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

    outfile = codecs.open('modaoutlet_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|OT|MTYPE@@모다아울렛\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % u'아울렛')

        page += 1

        if page == 2: break     # 한번 호출로 전국 점포 정보 모두 얻을 수 있음
        elif len(store_list) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://www.modaoutlet.com/agency/?control=agency&method=main&BranchCode=2'
    url = 'http://www.modaoutlet.com'
    api = '/agency/'
    data = {
        'control': 'agency',
        'method': 'main',
        'BranchCode': '2',
    }
    data['page'] = intPageNo
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@id="container"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//img/@title')
        info_list = entity_list[i].xpath('.//dd')
        if len(name_list) < 1 or len(info_list) < 2: continue

        store_info = {}

        store_info['name'] = '모다아울렛'
        store_info['subname'] = name_list[0].lstrip().rstrip().replace(' ', '/')
        store_info['addr'] = '' ;    store_info['newaddr'] = ''
        store_info['id'] = ''
        store_info['ot'] = ''
        store_info['pn'] = ''

        temp_list = info_list[1].xpath('.//a/@href')
        if len(temp_list) < 1: continue

        strtemp = temp_list[0]
        idx = strtemp.find('BranchCode=')
        if idx == -1:
            if store_info['subname'] == '경주점':
                store_info['id'] = '7'
            elif store_info['subname'] == '진주점':
                store_info['id'] = '8'
            elif store_info['subname'] == '원주점':
                store_info['id'] = '10'
            elif store_info['subname'] == '오산동탄점':
                store_info['id'] = '11'
            else:
                continue
        else:
            store_info['id'] = strtemp[idx+11:]

        if store_info['subname'] == '천안점':
            store_info['subname'] == '천안/아산점'


        suburl = 'http://www.modaoutlet.com/agency/?control=agency&method=location&BranchCode=' +  store_info['id']
        print(suburl)  # for debugging

        try:
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="info"]//tbody//tr//td')

        strtemp = "".join(subinfo_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['addr'] = strtemp

        strtemp = "".join(subinfo_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['ot'] = strtemp

        strtemp = "".join(subinfo_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
