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

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('insurance_aia_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@AIA생명\n")

    store_list = getStores()

    if store_list != None:
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

    outfile.close()

def getStores():
    url = 'https://www.aia.co.kr'
    api = '/content/dam/kr/ko/js/json/locations.json'
    data = {
        'n': '90',
        'e': '180',
        's': '-90',
        'w': '-180',
        '_': '1632463353576',       # '_' 파라미터 값 주기적으로 바뀌는 것 같음 (주기적으로 갱신 필요???)
    }
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        #'Accept-Encoding': 'gzip, deflate, br',    # 이렇게 설정하면 gzip 압축해서 보냄
        'Accept-Encoding': 'None',              # gzip 압축하지 않은 값을 받으려면 이렇게 해야 함
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        #'cookie': '_sdsat_landing_page=https://www.aia.co.kr/ko/index.html|1504803805283; _sdsat_session_count=1; AMCVS_E10E525A5481ADEC0A4C98C6%40AdobeOrg=1; mcvid.reset=1; _sdsat_traffic_source=http://cyber.aia.co.kr/eCustomer/web/cyber/inc/aia_stop.jsp; AMCV_E10E525A5481ADEC0A4C98C6%40AdobeOrg=1099438348%7CMCIDTS%7C17420%7CMCMID%7C20388171254751245271964821320717920234%7CMCAAMLH-1505408605%7C11%7CMCAAMB-1505631581%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1505033981s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17424%7CvVersion%7C2.1.0; _gat_f75867822a1671cb7fc0eb0f992f0885=1; _sdsat_lt_pages_viewed=6; _sdsat_pages_viewed=6; _ga=GA1.3.1335517501.1504803806; _gid=GA1.3.459090662.1505026782',
        # cookie값 없이 호출해도 결과값 반환함 (2017년9월에 확인함)
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        req = urllib2.Request(url+api, params, headers=hdr)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
        #result = urllib.urlopen(url+api+'?'+params)    # header 정보 없이 호출하면 403 오류 반환
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200 and code != 201:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    entity_list = json.loads(response)
    if entity_list == None: return None

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'AIA생명'
        store_info['id'] = entity_list[i]['id']

        strtemp = entity_list[i]['name'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        if strtemp.endswith('플라자'): pass
        elif not strtemp.endswith('지점'): strtemp += '지점'
        store_info['subname'] = strtemp.replace(' ', '/')

        strtemp = entity_list[i]['address']
        if strtemp.startswith('('):
            idx = strtemp.find(')')
            strtemp = strtemp[idx+1:].lstrip()
        store_info['newaddr'] = strtemp

        store_info['pn'] = entity_list[i]['phone'].replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['ot'] = ''
        if entity_list[i].get('hours'): store_info['ot'] = entity_list[i]['hours']

        store_info['xcoord'] = entity_list[i]['lng']
        store_info['ycoord'] = entity_list[i]['lat']

        store_list += [store_info]

    return store_list


def convert_full_to_half_char(ch):
    codeval = ord(ch)
    if 0xFF00 <= codeval <= 0xFF5E:
        ascii = codeval - 0xFF00 + 0x20;
        return unichr(ascii)
    else:
        return ch


def convert_full_to_half_string(line):
    output_list = [convert_full_to_half_char(x) for x in line]
    return ''.join(output_list)


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
