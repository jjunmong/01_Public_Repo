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

    outfile = codecs.open('momcare_center_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|WEBSITE|XCOORD|YCOORD@@산후조리원\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['url'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break    # 2018년5월 기준 50까지 있음
        elif len(store_list) < 12: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.momlog.co.kr'
    api = '/cares/careList.html'
    data = {
        'search_text': '',
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="bbs_list"]//ul//li//span[@class="wrap"]')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//strong')
        subapi_list = entity_list[i].xpath('.//a/@href')
        if len(name_list) < 1 or len(subapi_list) < 1: continue  # 최소 필드 수 체크

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        store_info['pn'] = ''
        store_info['url'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        subapi = subapi_list[0].lstrip().rstrip()

        try:
            suburls = url + '/cares/' + subapi
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="contact"]//p')

        for j in range(len(subinfo_list)):
            feature_name = ''
            temp_list = subinfo_list[j].xpath('./@class')
            if len(temp_list) > 0: feature_name = temp_list[0]
            strtemp = "".join(subinfo_list[j].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if feature_name == 'tel':
                    store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')
                elif feature_name == 'adress':
                    store_info['newaddr'] = strtemp

        urlinfo_list = subtree.xpath('//div[@class="contact"]//span[@class="url"]//a/@href')
        if len(urlinfo_list) > 0:
            store_info['url'] = urlinfo_list[0]

        # 좌표정보 추출
        idx = subresponse.find('google.maps.LatLng(')
        if idx != -1:
            strtemp = subresponse[idx+19:]
            idx = strtemp.find(')')
            if idx != -1 and idx < 50:
                coord_list = strtemp[:idx].split(',')
                if len(coord_list) == 2:
                    store_info['xcoord'] = coord_list[1].replace('lng=', '').lstrip().rstrip()
                    store_info['ycoord'] = coord_list[0].replace('lat=', '').lstrip().rstrip()

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
