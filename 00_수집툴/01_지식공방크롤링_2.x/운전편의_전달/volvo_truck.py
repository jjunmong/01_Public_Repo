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

    outfile = codecs.open('volvo_truck_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 2: break     # 한번 호출로 전국 점포정보 다 얻어옴
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.volvotrucks.kr'
    api = '/ko-kr/dealer-locator.html'
    data = {}
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="third-level-item"]/a/@href')
    entity_list += ['https://www.volvotrucks.kr/ko-kr/dealer-locator/bibong_truck.html']    # 지점 한 곳의 url이 잘못 들어가 있음 (수정한 url 강제로 추가함) (2018/6)

    store_list = []
    for i in range(len(entity_list)):
        suburl = entity_list[i]
        if suburl.find('/dealer-locator/') == -1: continue

        try:
            print(suburl)  # for debugging
            time.sleep(random.uniform(0.3, 1.1))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');            continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);            continue

        subresponse = subresult.read()
        # print(response)
        subtree = html.fromstring(subresponse)

        subentity_list = subtree.xpath('//div[@class="padding-container"]')
        for j in range(len(subentity_list)):
            name_list = subentity_list[j].xpath('.//span')
            subinfo_list = subentity_list[j].xpath('.//p')

            if len(subinfo_list) < 5:
                if len(subinfo_list) < 4 or len(name_list) == 0:
                    continue

            store_info = {}
            store_info['name'] = '볼보트럭'
            store_info['subname'] = ''

            next_idx = 1
            if len(name_list) > 0:
                strtemp = name_list[0].text
                if strtemp != None:
                    strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                    if strtemp.startswith('볼보트럭'):
                        strtemp = strtemp[4:].lstrip()
                        if strtemp.startswith('센터'):
                            strtemp = strtemp[2:].lstrip() + ' 센터'
                        store_info['subname'] = strtemp.replace(' ', '/')
                        next_idx = 0

            if next_idx == 1:   # name_list에서 지점 이름을 못 찾았으면
                strtemp = "".join(subinfo_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                    if strtemp.startswith('볼보트럭'): strtemp = strtemp[4:].lstrip()
                    if strtemp.startswith('센터'):
                        strtemp = strtemp[2:].lstrip() + ' 센터'
                    store_info['subname'] = strtemp.replace(' ', '/')

            store_info['newaddr'] = ''
            strtemp = "".join(subinfo_list[next_idx].itertext())
            if strtemp != None:     # 중간에 아무 내용도 없이 <p>가 한번 더 있는 경우가 있어서... 다음과 같이... '<p><p style="word-break:keep-all; padding:10px 0 0 0; ">경기도 화성시 비봉면 푸른들판로 1255 (비봉사업소 내 )</p>'
                if strtemp.find('전화') != -1:
                    next_idx += 1;      strtemp = "".join(subinfo_list[next_idx].itertext())
                elif strtemp == '':
                    next_idx += 1;      strtemp = "".join(subinfo_list[next_idx].itertext())

            if strtemp != None:
                strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['newaddr'] = strtemp

            next_idx += 1
            store_info['pn'] = ''
            strtemp = "".join(subinfo_list[next_idx].itertext())
            if strtemp != None:  # 중간에 구주소 정보가 추가로 있는 경우가 있어서...
                if strtemp.find('구주소') != -1:
                    next_idx += 1;      strtemp = "".join(subinfo_list[next_idx].itertext())

            if strtemp != None:
                strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                idx = strtemp.find('팩스')
                if idx != -1: strtemp = strtemp[:idx].rstrip()
                idx = strtemp.find(',')
                if idx != -1: strtemp = strtemp[:idx].rstrip()
                if strtemp.startswith('대표전화'): strtemp = strtemp[5:].lstrip()
                if strtemp.startswith('전화번호'): strtemp = strtemp[5:].lstrip()
                if strtemp.startswith('전화'): strtemp = strtemp[2:].lstrip()
                if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
                store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')

            if len(store_list) != 0:
                if store_list[0]['pn'] == store_info['pn']:
                    return store_list

            store_list += [store_info];

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
