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

sido_list2 = {      # 테스트용 시도 목록
    '세종': '36'
}

sido_list = {
    '서울': '11',
    '광주': '29',
    '대구': '27',
    '대전': '30',
    '부산': '26',
    '울산': '31',
    '인천': '28',
    '경기': '41',
    '강원': '42',
    '경남': '48',
    '경북': '47',
    '전남': '46',
    '전북': '45',
    '충남': '44',
    '충북': '43',
    '제주': '50',
    '세종': '36'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('real_estate_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ID|STATUS@@부동산\n")

    for sido_name in sorted(sido_list):

        # get sub district code info
        sub_district_list = getSubDistrictInfo(sido_list[sido_name])
        print(sub_district_list)
        print('sub district info collected!')

        for sub_district_code in sorted(sub_district_list):
            page = 1
            retry_count = 0
            while True:
                store_list = getStores(sido_list[sido_name], sub_district_code, page)
                if store_list == None:
                    if retry_count > 3: break
                    else: retry_count += 1; continue

                retry_count = 0

                for store in store_list:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['subname'])
                    outfile.write(u'%s|' % store['pn'])
                    outfile.write(u'%s|' % store['newaddr'])
                    outfile.write(u'%s|' % store['id'])
                    outfile.write(u'%s\n' % store['status'])

                page += 1

                if page == 3999: break    # 2101까지 있음
                elif len(store_list) < 50: break

                time.sleep(random.uniform(0.3, 0.9))

            time.sleep(random.uniform(1, 2))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_code, sgg_code, intPageNo):
    url = 'http://www.nsdi.go.kr'
    api = '/lxportal/?menuno=4085&pageIndex=' + str(intPageNo)
    data = {
        'shInit': 'N',
        'pageIndex': '1',
        #'shSido': '11',
        #'shSigungu': '11680',
        'shDong': '',
        'shSelect': '1',
        'shWord': '',
        'shWord1': '',
        'shWord2': '',
        'shSelect3': '',
        'orderSelect': '1',
        'orderSelect1': '0',
        #'shSelect2': '1',
        #'shCondi': '',
        'pageSize': '50',
    }
    data['shSido'] = sido_code
    data['shSigungu'] = sgg_code
    params = urllib.urlencode(data)
    print(url+api)
    #print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req, timeout=30)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    try:
        response = result.read()
        #print(response)
        #tree = html.fromstring(response)
        tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)
    except:
        print('err_sggcode = ' + sgg_code)
        print('no return value');     return None

    entity_list = tree.xpath('//table[@class="bl_list"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 8: continue  # 최소 8개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            strtemp = strtemp.replace('(주)', '').replace('(유)', '').replace('(사)', '').replace('(공동)', '').rstrip().lstrip()
            strtemp = strtemp.replace('(합동)', '').replace('(단지)', '').replace('(단지내)', '').replace('(단지입구)', '').rstrip().lstrip()
            store_info['name'] = strtemp    # 명칭 정규화는 별도 프로그램으로 수행...
            #store_info['name'] = strtemp.replace(' ', '/')

        store_info['id'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['id'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[5].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('(') and strtemp.endswith(')'): strtemp = strtemp[1:-1].rstrip().lstrip()
            store_info['pn'] = strtemp.replace('.', '-').replace(', ', '/').replace(',', '/').replace(' ', '/').replace('//', '/').replace('//', '/')

        store_info['status'] = ''
        temp_list = info_list[7].xpath('./@title')
        if len(temp_list) > 0:
            store_info['status'] = temp_list[0]

        store_list += [store_info]

    return store_list

def getSubDistrictInfo(sido_code):
    url = 'http://www.nsdi.go.kr/lxportal/zcms/nsdi/land/searchSigungu.html'
    params = 'sido=' + sido_code

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url, params)
        req = urllib2.Request(url, params, headers=hdr)     # header값 잘못 지정되어 있으면 전국 시군구 코드가 한꺼번에 모두 반환됨
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);
        return None

    response = result.read()
    response_json = json.loads(response)
    entity_list = response_json['sigunguList']

    district_list = []
    for i in range(len(entity_list)):
        district_list.append(entity_list[i]['sggCd'])

    return district_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
