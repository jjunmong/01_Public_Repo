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

    outfile = codecs.open('malja_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@말자싸롱\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/9)
def getStores(intPageNo):
    url = 'http://www.malja.co.kr'
    api = '/bbs/board.php'
    data = {
        'bo_table': 'store',
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
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@class="table"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 6개 필드 있어야 함

        store_info = {}

        store_info['name'] = '말자싸롱'
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('['):     # '[강원도]  삼척점'에서 '[강원도]' 제거
                idx = strtemp.find(']')
                if idx != -1:
                    strtemp = strtemp[idx+1:].lstrip()

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['ot'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['ot'] = strtemp

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        temp_list = info_list[5].xpath('.//a/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('viewMap(')
            if idx != -1:
                strtemp = strtemp[8:].lstrip()
                idx = strtemp.find(')')
                if idx != -1:
                    temp_list = strtemp[:idx].rstrip().split(',')
                    if len(temp_list) == 2:
                        store_info['xcoord'] = temp_list[0]
                        store_info['ycoord'] = temp_list[1]

        store_list += [store_info]

    return store_list


'''
def getStores(intPageNo):
    # 'http://www.malja.co.kr/get.do?callback=jQuery112403180777914312909_1525159319719&id=Store&ac=select_store&rowcnt=10&page=3&_=1525159319724'
    url = 'http://www.malja.co.kr'
    api = '/get.do'
    data = {
        'callback': 'jQuery112403180777914312909_1525159319719',
        'id': 'Store',
        'ac': 'select_store',
        'rowcnt': '10',
        #'_': '1525159319724',
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
    #print(response)
    idx = response.find('([')
    if idx == -1: return None
    response = response[idx+1:-1]
    entity_list = json.loads(response)

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '말자싸롱'
        strtemp = entity_list[i]['store_name'].lstrip().rstrip()
        if not strtemp.endswith('점'): strtemp += '점'
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['seq']

        store_info['newaddr'] = entity_list[i]['addr_road'].lstrip().rstrip()
        store_info['addr'] = entity_list[i]['addr_jibun'].lstrip().rstrip()
        store_info['pn'] = entity_list[i]['store_tel'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['ot'] = entity_list[i]['open_tm'] + entity_list[i]['wd_open_time'] + '~' + entity_list[i]['close_tm'] + entity_list[i]['wd_close_time']

        store_info['xcoord'] = entity_list[i]['point_x']
        store_info['ycoord'] = entity_list[i]['point_y']

        # suburl 호출로 영업시간 정보, 좌표 정보 추가로 얻을 수 있음

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
