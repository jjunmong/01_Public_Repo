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

    outfile = codecs.open('taxaccountant_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ADDR|SUPERVISOR|SOURCE2@@세무사\n")

    for sido_name in sorted(sido_list):
        page = 1
        retry_count = 0

        while True:
            store_list = getStores(u'법인', page)
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
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['supervisor'])
                outfile.write(u'%s\n' % u'한국세무사회')

            page += 1

            if page == 2: break      # 한번 호출로 모든 정보 다 얻을 수 있음
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        break      # 한번 호출로 모든 정보 다 얻을 수 있음
        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(search_key, intPageNo):
    # 'http://www.kacpta.or.kr/kacpta_view/kac_taxbiz/taxAccountantSearch_n_Proc.asp'
    url = 'http://www.kacpta.or.kr'
    api = '/kacpta_view/kac_taxbiz/taxAccountantSearch_n_Proc.asp'
    data = {
        'keyfield': '2',
        'x': '28',
        'y': '10',
    }
    data['keyword'] = search_key.encode('euc-kr')
    params = urllib.urlencode(data)
    print(params)

    try:
        #result = urllib.urlopen(url + api, params)
        #urls = url + api + '?' + params
        #print(urls)     # for debugging
        #result = urllib.urlopen(urls)

        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'euc-kr')
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)     # 인코딩 정보가 반환값에 없어서...

    subapi_list = tree.xpath('//table[@width="81%"]//tr//td[@width="150"]//a/@href')

    store_list = []
    for i in range(len(subapi_list)):
        subapi = subapi_list[i]
        idx = subapi.rfind('beobin_nm=')
        if idx != -1:
            subdata = {}
            subdata['beobin_nm'] = subapi[idx+10:].encode('euc-kr')
            subparams = urllib.urlencode(subdata)

            subapi = subapi[:idx] + subparams   # 한글 파라미터는 인코딩하지 않으면 호출 오류 발생

        suburl = url + subapi

        try:
            time.sleep(random.uniform(0.3, 0.9))
            print(suburl)  # for debugging
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');     continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);     continue

        subresponse = subresult.read()
        subresponse = unicode(subresponse, 'euc-kr')
        subtree = html.fromstring(subresponse)
        #subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)     # 인코딩 정보가 반환값에 없어서...

        info_list = subtree.xpath('//table[@width="83%"]//tr')

        #if len(info_list) < 4: continue
        store_info = {}
        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['supervisor'] = ''
        store_info['newaddr'] = ''
        store_info['addr'] = ''
        store_info['pn'] = ''

        for j in range(len(info_list)):
            value_list = info_list[j].xpath('.//td')

            if len(value_list) < 2: continue

            tag = "".join(value_list[0].itertext())
            value = "".join(value_list[1].itertext())

            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if tag.find('법인명') != -1:
                store_info['name'] = value.replace(' ', '/')
            elif tag.find('사무소주소') != -1:
                idx = value.find(u'* 지 번')
                if idx != -1:
                    store_info['newaddr'] = value[:idx].rstrip()
                    value = value[idx+5:].lstrip()
                    if value.startswith(':'): value = value[1:].lstrip()
                    store_info['addr'] = value
                else: store_info['newaddr'] = value
            if tag.find('전화번호') != -1:
                store_info['pn'] = value.replace(')', '-').replace('(', '-')
            if tag.find('소속지방국세청') != -1:
                store_info['supervisor'] = value

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
