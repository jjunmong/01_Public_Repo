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
from selenium import webdriver
import bs4

sido_list2= {      # 테스트용 시도 목록
    '서울': '02',
}

sido_list = {
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
    '경상남도': '055',
    '경상북도': '054',
    '전남': '061',
    '전북': '063',
    '전라남도': '061',
    '전라북도': '063',
    '충남': '041',
    '충북': '043',
    '충청남도': '041',
    '충청북도': '043',
    '제주': '064',
    '세종': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    driver = webdriver.Chrome('C:\chromedriver.exe')

    outfile = codecs.open('nike_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@나이키\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            storeList = getStores(driver, sido_name, page)

            if storeList == None: break;
            elif len(storeList) == 0: break

            for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1
            if page == 99: break
            elif len(storeList) < 15: break

            time.sleep(random.uniform(0.3, 0.9))
            driver.close()
        time.sleep(random.uniform(1, 2))

    outfile.close()

# v3.0 (2018/9)
def getStores(browser_driver, sido_name, page_no):
    # 'https://www.nike.com/kr/ko_kr/store?_find=%EC%A0%9C%EC%A3%BC&_search=name&_condition=like
    url = 'https://www.nike.com'
    api = '/kr/ko_kr/store'
    data = {
        '_search': 'name',
        '_condition': 'like',
    }
    data['_find'] = sido_name
    if page_no != '1':
        data['page'] = page_no
    params = urllib.urlencode(data)
    print("%s %s" % (sido_name, page_no))

    #browser_driver = webdriver.Chrome('C:\Python27\chromedriver.exe')
    urls = url + api + '?' + params
    browser_driver.get(urls)
    delay = 1
    browser_driver.implicitly_wait(delay)

    response = browser_driver.page_source
    #print(response)
    tree = html.fromstring(response)

    temp_list = tree.xpath('//div[@class="location-map"]/@data-store-list')
    if len(temp_list) == 0: return None

    strtemp = temp_list[0].replace('&quot;', '"')
    entity_list = json.loads(strtemp)

    strtemp2 = ''

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}
        store_info['name'] = '나이키'

        store_info['subname'] = ''
        if entity_list[i].get('name'):
            strtemp = convert_full_to_half_string(entity_list[i]['name'])
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.lstrip().rstrip().replace(' ', '/')

        store_info['id'] = ''
        if entity_list[i].get('id'):
            store_info['id'] = entity_list[i]['id']

        store_info['newaddr'] = ''
        if entity_list[i].get('address1'):
            store_info['newaddr'] = entity_list[i]['address1']

        if entity_list[i].get('address2'):
            store_info['newaddr'] += ' ' + entity_list[i]['address2']

        store_info['pn'] = ''
        if entity_list[i].get('phone'):
            store_info['pn'] = entity_list[i]['phone']

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if entity_list[i].get('longitude'):
            store_info['xcoord'] = entity_list[i]['longitude']
        if entity_list[i].get('latitude'):
            store_info['ycoord'] = entity_list[i]['latitude']

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

'''
# v1.0
def getStores(strSidoName):
    url = 'http://lecs.nike.co.kr'
    api = '/findstore/findStoreListAjax.lecs'
    data = {
        'searchStoreStep': '',
        'mapXposVal': '',
        'mapYposVal': '',
        'leftMapXyVal': '126.9740319,37.5364839',
        'rightMapXyVal': '127.0779131,37.4683993',
        'shopSn': '',
    }

    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)        # for debugging

    receivedData = json.loads(response)  # json 포맷으로 결과값 반환

    storeList = receivedData
    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
