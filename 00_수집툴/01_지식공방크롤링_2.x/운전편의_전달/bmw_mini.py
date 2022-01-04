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

    outfile = codecs.open('bmwmini_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|SUBNAME2|OT|XCOORD|YCOORD@@BMW\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['subname2'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전체 점포 정보 모두 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'https://kr.mini.co.kr'
    api = '/mini/showroom/maporder.json'
    try:
        urls = url + api
        print(urls)
        req = urllib2.Request(urls, '')
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads('{"dealers": ' + response + '}')
    entity_list = response_json['dealers']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}
        store_info['name'] = 'BMW미니'
        store_info['subname'] = ''
        strtemp = entity_list[i]['showRoomName']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            if strtemp.startswith('MINI'): strtemp = strtemp[4:].lstrip()
            if not strtemp.endswith('전시장'): strtemp += '전시장'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['subname2'] = ''
        strtemp = entity_list[i]['blog_url']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            idx = strtemp.find('<br>')
            if idx != -1: strtemp = strtemp[:idx].rstrip()
            store_info['subname2'] = strtemp.replace(' ', '/')

        store_info['newaddr'] =entity_list[i]['addrArray'].replace('<br>', '')
        store_info['ot'] = entity_list[i]['doc'].replace('<br>', ';').replace(' ', '')

        store_info['pn'] = entity_list[i]['telNumber'].replace(' ', '').replace('.', '-').replace(')', '-')

        store_info['xcoord'] = entity_list[i]['y']
        store_info['ycoord'] = entity_list[i]['x']

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
