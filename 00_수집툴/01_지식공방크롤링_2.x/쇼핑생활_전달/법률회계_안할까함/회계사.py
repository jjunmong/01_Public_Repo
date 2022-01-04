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
    '강원': '033',
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

    outfile = codecs.open('accountant_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OWNER|SOURCE2@@회계사\n")

    for sido_name in sorted(sido_list):
        page = 1
        retry_count = 0

        while True:
            store_list = getStores(sido_name, page)
            if store_list == None:
                if retry_count > 3:
                    break
                else:
                    retry_count += 1
                    continue

            retry_count = 0

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['owner'])
                outfile.write(u'%s\n' % u'한국공인회계사회')

            page += 1

            if page == 2: break      # 한번 호출로 모든 정보 다 얻을 수 있음
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        break      # 한번 호출로 모든 정보 다 얻을 수 있음
        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    # 'http://www.kicpa.or.kr/home/audtTaxAttrnGnrl/accCoReList.face'
    url = 'http://www.kicpa.or.kr'
    api = '/home/audtTaxAttrnGnrl/accCoReList.face'
    data = {}
    #params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        #urls = url + api + '?' + params
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)     # 인코딩 정보가 반환값에 없어서...

    entity_list = tree.xpath('//table[@class="table_st02"]//tbody//tr//td')

    store_list = []
    for i in range(len(entity_list)):

        param_tag_list = entity_list[i].xpath('.//input/@class')
        param_value_list = entity_list[i].xpath('.//input/@value')
        if len(param_tag_list) < 4 or len(param_value_list) < 4: continue  # 최소 4개 필드 있어야 함

        subdata = {}
        strtemp = param_value_list[0]
        if strtemp.endswith('00'): strtemp = strtemp[:-2]
        if len(strtemp) >= 6: strtemp = strtemp[:-2]
        subdata['aciGamIdCode'] = strtemp
        subdata[param_tag_list[1]] = param_value_list[1]
        subdata[param_tag_list[2]] = param_value_list[2]
        subdata[param_tag_list[3]] = param_value_list[3]
        subparams = urllib.urlencode(subdata)
        #print(subparams)

        try:
            time.sleep(random.uniform(0.3, 0.9))
            # result = urllib.urlopen(url + api, params)
            suburls = 'http://www.kicpa.or.kr/home/audtTaxAttrnGnrl/aciGamIdInfoLoad.face' + '?' + subparams
            print(suburls)  # for debugging
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');     continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);     continue

        subresponse = subresult.read()
        #subtree = html.fromstring(subresponse)
        subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)     # 인코딩 정보가 반환값에 없어서...

        info_list = subtree.xpath('//table[@class="table_st02 table_st02_write"]//tr')

        #if len(info_list) < 4: continue
        store_info = {}
        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['id'] = ''
        store_info['owner'] = ''
        store_info['newaddr'] = ''
        store_info['pn'] = ''

        for j in range(len(info_list)):
            tag_list = info_list[j].xpath('.//th')
            value_list = info_list[j].xpath('.//td')

            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag_name = "".join(tag_list[0].itertext())
            if tag_name == None: continue
            tag_name = tag_name.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if tag_name == '법인명':
                strtemp = "".join(value_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['name'] = strtemp.replace(' ', '/')
            elif tag_name == '등록번호':
                strtemp = "".join(value_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['id'] = strtemp.replace(' ', '')
            elif tag_name == '대표이사':
                strtemp = "".join(value_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['owner'] = strtemp
            elif tag_name == '주사무소':
                extra_info_list = value_list[0].xpath('.//ul//li')
                if len(extra_info_list) > 1:
                    strtemp = "".join(extra_info_list[0].itertext())
                    if strtemp != None:
                        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
                        if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                        store_info['newaddr'] = strtemp
                if len(extra_info_list) > 2:
                    strtemp = "".join(extra_info_list[1].itertext())
                    if strtemp != None:
                        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        if strtemp.startswith('전화'): strtemp = strtemp[2:].lstrip()
                        if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                        store_info['pn'] = strtemp

                store_info['subname'] = ''
                store_list += [store_info]
            elif tag_name == '분사무소':
                extra_store_info = {}
                extra_store_info['name'] = store_info['name']
                extra_store_info['subname'] = store_info['subname']
                extra_store_info['id'] = store_info['id']
                extra_store_info['owner'] = store_info['owner']

                extra_info_list = value_list[0].xpath('.//ul//li')
                if len(extra_info_list) > 1:
                    strtemp = "".join(extra_info_list[0].itertext())
                    if strtemp != None:
                        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
                        if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                        extra_store_info['newaddr'] = strtemp
                if len(extra_info_list) > 2:
                    strtemp = "".join(extra_info_list[1].itertext())
                    if strtemp != None:
                        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        if strtemp.startswith('전화'): strtemp = strtemp[2:].lstrip()
                        if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                        extra_store_info['pn'] = strtemp

                extra_store_info['subname'] = '분사무소'
                store_list += [extra_store_info]
            elif tag_name == '분실':
                extra_store_info = {}
                extra_store_info['name'] = store_info['name']
                extra_store_info['subname'] = store_info['subname']
                extra_store_info['id'] = store_info['id']
                extra_store_info['owner'] = store_info['owner']

                extra_info_list = value_list[0].xpath('.//ul//li')
                if len(extra_info_list) > 1:
                    strtemp = "".join(extra_info_list[0].itertext())
                    if strtemp != None:
                        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
                        if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                        extra_store_info['newaddr'] = strtemp
                if len(extra_info_list) > 2:
                    strtemp = "".join(extra_info_list[1].itertext())
                    if strtemp != None:
                        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        if strtemp.startswith('전화'): strtemp = strtemp[2:].lstrip()
                        if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                        extra_store_info['pn'] = strtemp

                extra_store_info['subname'] = '분실'
                store_list += [extra_store_info]

        #store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
