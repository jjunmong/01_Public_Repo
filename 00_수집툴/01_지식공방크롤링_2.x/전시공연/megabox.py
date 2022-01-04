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

    outfile = codecs.open('megabox_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|XCOORD|YCOORD\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'메가박스|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.megabox.co.kr/theater/list'
    # api = '/'
    # data = {
    #     'menuId': 'theater',
    # }
    # params = urllib.urlencode(data)
    # print(params)

    try:
        urls = url
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response = response.replace('-- >', '-->')  # 반환값에 구문 오류 있음 ㅠㅠ (2018/8)
    tree = html.fromstring(response)

    temp_list = tree.xpath('//div[@class="theater-list"]')
    entity_list = None
    if len(temp_list) == 2:
        entity_list = temp_list[1].xpath('.//ul//li/a')
    else:
        entity_list = tree.xpath('//div[@class="theater-list"]//ul//li/a')

    result_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('./@class')
        subname = entity_list[i].text

        if len(temp_list) == 0: continue
        strtemp = temp_list[0]

        if strtemp.find('theater_menu') == -1 or subname == None: continue

        store_info = {}
        store_info['subname'] = subname.lstrip().rstrip().replace(' ', '/')

        store_info['pn'] = '1544-0070';      store_info['addr'] = '';     store_info['newaddr'] = '';      store_info['feat'] = ''
        store_info['xcoord'] = '';  store_info['ycoord'] = ''
        idx = strtemp.find('theater_menu_')
        shop_id = strtemp[idx+13:].lstrip().rstrip()

        subapi = '/'
        subdata = {
            'menuId': 'theater-detail',
            'region': '',
        }
        subdata['cinema'] = shop_id
        subparams = urllib.urlencode(subdata)

        time.sleep(random.uniform(0.3, 0.9))
        try:
            suburl = url + api + '?' + subparams
            print(suburl)  # for debugging
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');
            result_list += [store_info]
            continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);
            result_list += [store_info]
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        info_node = subtree.xpath('//div[@class="section no4"]//div')
        script_node = subtree.xpath('//div[@class="section no4"]//script')

        if len(info_node) == 0:
            result_list += [store_info];    continue

        info_list = info_node[0].xpath('.//h4')
        if len(info_list) < 2:  # 최소 2개 필드 있어야 함
            result_list += [store_info];    continue

        strtemp = info_list[0].text
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            idx = strtemp.find(' : ')
            if idx != -1: strtemp = strtemp[idx+3:].lstrip()
            idx = strtemp.find('전화번호')
            if idx != -1:
                strtemp = strtemp[:idx].rstrip()
                if strtemp.endswith('/'): strtemp = strtemp[:-1].rstrip()
            store_info['newaddr'] = strtemp

        strtemp = info_list[1].text
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            idx = strtemp.find(' : ')
            if idx != -1: strtemp = strtemp[idx+3:].lstrip()
            store_info['addr'] = strtemp

        if len(script_node) == 0:
            result_list += [store_info];    continue

        strtemp = "".join(script_node[0].itertext())
        if strtemp != None:
            idx = strtemp.find('LatLng(')
            if idx != -1:
                strtemp = strtemp[idx+7:]
                idx = strtemp.find(')')
                strtemp = strtemp[:idx]
                idx = strtemp.find(',')
                store_info['ycoord'] = strtemp[:idx].lstrip().rstrip()
                store_info['xcoord'] = strtemp[idx+1:].lstrip().rstrip()

        result_list += [store_info]

    return result_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
