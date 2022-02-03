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

sido_list2 = {      # 테스트용 광역시도 목록
    '경기도': '031',
}

sido_list = {
    '서울특별시': '02',
    '광주광역시': '062',
    '대구광역시': '053',
    '대전광역시': '042',
    '부산광역시': '051',
    '울산광역시': '052',
    '인천광역시': '032',
    '경기도': '031',
    '강원도': '033',
    '경상남도': '055',
    #'경상북도': '054',         # 남도, 북도 똑같은 결과값 반환하므로 한번만 호출해도 됨!!!
    '전라남도': '061',
    #'전라북도': '063',
    '충청남도': '041',
    #'충청북도': '043',
    '제주도': '064',
    '세종시': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('scbank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|CODE|XCOORD|YCOORD@@SC제일은행\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['code'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 99: break
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 1.1))

        time.sleep(random.uniform(1, 2))

    outfile.close()


def getStores(sido_name, intPageNo):
    url = 'http://biz.talkyple.com'
    api = '/scbank/map_renew/search_proc.jsp'

    data = {
        'type': '10',
        'type1': '',
        'listnum': '10',
    }
    data['pagenum'] = intPageNo
    data['type0'] = sido_name
    params = urllib.urlencode(data)
    params = params.replace('%', '%25')     # '%'문자도 인코딩 ('%'를 인코딩하면 '%25'가 된다고 함
    #print(params)

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
    response = unicode(response, 'euc-kr')
    response = response.replace('data:', '"data":').replace('name:', '"name":').replace('cms:', '"cms":').replace(',addr:', ',"addr":').replace(',raddr:', ',"raddr":')
    response = response.replace('x:', '"x":').replace('y:', '"y":').replace('code:', '"code":').replace('totalcount:', '"totalcount":').replace('pagenum:', '"pagenum":')
    response = response.replace('listnum:', '"listnum":').replace('type:', '"type":').replace('sql:', '"sql":')
    print(response)
    response_json = json.loads(response)

    entity_list = response_json['data']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'SC제일은행'
        store_info['subname'] = ''
        strtemp = entity_list[i]['name']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.endswith('(출)'): strtemp = strtemp[:-3].rstrip() + '출장소'
            elif strtemp.endswith('센터'): pass
            elif strtemp.endswith('본점'): pass
            elif not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['raddr']
        store_info['addr'] = entity_list[i]['addr']
        store_info['code'] = entity_list[i]['code']
        store_info['xcoord'] = entity_list[i]['x']
        store_info['ycoord'] = entity_list[i]['y']

        store_info['pn'] = ''

        store_list += [store_info]

    return store_list


def convert_full_to_half_char(ch):
    codeval = ord(ch)
    if 0xFF00 <= codeval <= 0xFF5E:
        ascii = codeval - 0xFF00 + 0x20
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
