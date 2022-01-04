# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import random
import codecs
import urllib
#import json
from lxml import html

area2 = {
    '서울특별시': '02'
}

area = {
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
    '경상북도': '054',
    '전라남도': '061',
    '전라북도': '063',
    '충청남도': '041',
    '충청북도': '043',
    '제주특별자치도': '064',
    '세종특별자치시': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('pb_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ID|NEWADDR|XCOORD|YCOORD@@파리바게뜨\n")

    for areaname in sorted(area):

        page = 1
        while True:
            storeList = getStores2(areaname, page)
            if storeList == None: break
            elif len(storeList) == 0: break

            for store in storeList:
                outfile.write(u'파리바게뜨|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 2: break     # 한번 호출로 광역시도내 점포 모두 얻을 수 있음

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2019/1)
def getStores2(areaname, intPageNo):
    # 'https://www.paris.co.kr/shop/search.jsp'
    url = 'https://www.paris.co.kr'
    api = '/shop/search.jsp'
    data = {
        's_gugun': '',
        's_name': ''
    }
    data['s_sido'] = areaname
    #data['page'] = intPageNo


    params = urllib.urlencode(data)
    #print(params)

    try:
        #result = urllib.urlopen(url + api, params)

        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="shop_list_box"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//strong')
        if len(name_list) < 1: continue

        store_info = {}

        store_info['name'] = '파리바게뜨'
        store_info['subname'] = ''

        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find("파리바게뜨")
            if(idx != -1): strtemp = strtemp[idx+5:].lstrip()
            if strtemp.startswith('PB'): strtemp = strtemp[2:].lstrip()
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = ''
        temp_list = entity_list[i].xpath('.//hidden//idx')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['id'] = strtemp

        store_info['newaddr'] = ''
        temp_list = entity_list[i].xpath('.//hidden//addr')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        temp_list = entity_list[i].xpath('.//hidden//tel')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['pn'] = strtemp

        store_info['xcoord'] = ''
        temp_list = entity_list[i].xpath('.//hidden//lng')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['xcoord'] = strtemp

        store_info['ycoord'] = ''
        temp_list = entity_list[i].xpath('.//hidden//lat')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['ycoord'] = strtemp

        store_list += [store_info]

    return store_list


# v1.0
def getStores(areaname, intPageNo):
    url = 'http://www.paris.co.kr'
    api = '/store/store_list.jsp'
    data = {
        'sido': '',
        'gugun': '',
        's_gugun': '',
        's_name': ''
    }
    data['s_sido'] = areaname
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    #print(params)

    try:
        #result = urllib.urlopen(url + api, params)

        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    tableSelector = '//table[@class="StoreList_type"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if(len(infoList) < 3):
            continue

        strtemp = infoList[0].text
        idx = strtemp.find("파리바게뜨")
        if(idx != -1): strtemp = strtemp[idx+5:].lstrip()
        if strtemp.startswith('PB'): strtemp = strtemp[2:].lstrip()
        strtemp = strtemp.lstrip().rstrip()
        if not strtemp.endswith('점'): strtemp += '점'
        strtemp = strtemp.replace(' ', '/')
        storeInfo['subname'] = strtemp

        storeInfo['newaddr'] = infoList[1].xpath('.//a')[0].text
        storeInfo['pn'] = infoList[2].text

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
