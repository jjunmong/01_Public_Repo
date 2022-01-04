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
#import json
from lxml import html

sido_list2 = {      # 테스트용 시도 목록
    '서울': '37.566535|126.97796919999996',
}

sido_list = {
    '서울': '37.566535|126.97796919999996',
    '부산': '35.1795543|129.07564160000004',
    '대구': '35.8714354|128.601445',
    '대전': '36.3504119|127.38454750000005',
    '광주': '35.1595454|126.85260119999998',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('porsche_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|SUBNAME2|XCOORD|YCOORD@@포르쉐\n")

    for sido_name in sido_list:
        store_list = getStores(sido_name, sido_list[sido_name])
        if store_list == None: continue

        for store in store_list:
            outfile.write(u'포르쉐센터|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['subname2'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.4, 1.2))

    outfile.close()

def getStores(sido_name, sido_coord):
    url = 'http://www.porsche.com'
    api = '/all/dealer2/GetLocationsWebService.asmx/GetLocationsInStateSpecialJS'
    data = {
        # 'searchKey': '37.566535|126.97796919999996',
        'maxnumtries': '',
        'siteId': 'korea',
        'maxproximity': '',
        # 'address': '서울',
        'market': 'korea',
        'language': 'ko',
        '_locationType': 'Search.LocationTypes.Dealer',
        'maxresults': '',
        'searchMode': 'proximity',
        'state': '',
    }
    # data = {
    #     'market': 'korea',
    #     'siteId': 'korea',
    #     'language': 'ko',
    #     'state': '',
    #     '_locationType': 'Search.LocationTypes.Dealer',
    #     'searchMode': 'proximity',
    #     'maxproximity': '',
    #     'maxnumtries': '',
    #     'maxresults': '',
    # }
    data['address'] = sido_name
    data['searchKey'] = sido_coord
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

    entity_list = tree.xpath('//location')

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}
        store_info['subname'] = '';     store_info['subname2'] = ''

        name_list = entity_list[i].xpath('.//name')
        name_list2 = entity_list[i].xpath('.//name2')
        if len(name_list) > 0:
            strtemp = name_list[0].text
            if strtemp != None:
                strtemp = strtemp.replace('포르쉐 센터', '').replace('포르쉐센터', '').replace('Porsche Centre', '').lstrip().rstrip()
                strtemp = strtemp.replace('Daechi', '대치').replace('Seocho', '서초').replace('Incheon', '인천').replace('Daegu', '대구').replace('Busan', '부산')
                store_info['subname'] = strtemp.replace(' ', '/')

        if len(name_list2) > 0:
            strtemp = name_list2[0].text
            if strtemp != None:
                strtemp = strtemp.lstrip().rstrip()
                store_info['subname2'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        city_list = entity_list[i].xpath('.//city')
        street_list = entity_list[i].xpath('.//street')
        if len(city_list) > 0 and len(street_list) > 0:
            store_info['newaddr'] = city_list[0].text + ' ' + street_list[0].text

        store_info['pn'] = ''
        temp_list = entity_list[i].xpath('.//phone')
        if len(temp_list) > 0:
            store_info['pn'] = temp_list[0].text.lstrip().rstrip().replace(' ', '').replace('.', '-').replace('+82-', '0')

        store_info['xcoord'] = ''
        temp_list = entity_list[i].xpath('.//lng')
        if len(temp_list) > 0:
            store_info['xcoord'] = temp_list[0].text.lstrip().rstrip()

        store_info['ycoord'] = ''
        temp_list = entity_list[i].xpath('.//lat')
        if len(temp_list) > 0:
            store_info['ycoord'] = temp_list[0].text.lstrip().rstrip()

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
