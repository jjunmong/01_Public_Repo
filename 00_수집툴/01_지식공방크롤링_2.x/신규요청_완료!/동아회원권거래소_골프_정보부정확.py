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

    outfile = codecs.open('donga_golf_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@GOLF\n")

    for area_code in range(1, 7):
        store_list = getStores(area_code)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(area_code):
    url = 'http://www.dongagolf.co.kr'
    api = '/inc/golfcf/list_golf_info1.php'
    data = {
        'cate1': 'golfcf',
        'cate2': 'golf_info',
    }
    data['area'] = area_code
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

    entity_list = tree.xpath('//table[@class="list"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')

        if len(info_list) < 2: continue  # 최소 2개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('[')
            if idx != -1:
                store_info['subname'] = strtemp[idx+1:-1].lstrip().rstrip()
                strtemp = strtemp[:idx].rstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''

        # 상세정보 페이지에서 퍼블릭골프장 여부 등의 정보도 얻을 수 있음
        strtemp  = info_list[0].xpath('.//a/@href')[0]      # 'http://www.dongagolf.co.kr/golfcf/golf_info?area=2&custid=10235
        idx = strtemp.find('custid=')
        if idx == -1:
            store_list += [store_info];     continue

        shop_id = strtemp[idx+7:]

        subdata = {
            'db': '',
            'area': '전체',
            'cust': '',
        }
        subdata['custid'] = shop_id
        subparams = urllib.urlencode(subdata)

        hdr = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            #'Referer': 'http://www.dongagolf.co.kr/golfcf/golf_info?area=2&custid=10235',
            #'Cookie': 'smtg_cKey=1489132181856019127; PHPSESSID=kf8vhdf4gqgv38gibdljs3bka5; smtg_fsID=1; wcs_bt=s_2200cba8d5:1489223776; _ga=GA1.3.1451156060.1489132181; smtg_sKey=1489221633253094194; smtg_sAd=0; smtg_vTime=1489223776',
        }

        try:
            suburl = url + '/inc/golfcf/golf_r_view.php'
            print(suburl)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            #subresult = urllib.urlopen(suburl + '?' + subparams)
            subreq = urllib2.Request(suburl, subparams, headers=hdr)
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the suburl');
            continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        #print(subresponse)
        #subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//table[@class="horizon"]//tbody//tr')
        for j in range(len(subinfo_list)):
            tag_list = subinfo_list[j].xpath('.//th')
            value_list = subinfo_list[j].xpath('.//td')

            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            if tag == None: continue
            tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            value = "".join(value_list[0].itertext())
            if value == None: continue
            value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if value == '-': continue

            if tag == '대표전화':
                strtemp = value.replace('.', '-').replace(')', '-')
                if strtemp.endswith('(0-'): strtemp = strtemp[:-3].rstrip()     # 잘못 기록된 정보 처리
                store_info['pn'] = strtemp

        store_list += [store_info];

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
