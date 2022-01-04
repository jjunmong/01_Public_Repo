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

area_list = {
    '인사동': '4',
    '북촌': '1',
    '광화문': '3',
    '평창동': '5',
    '홍대': '8',
    '청담동': '6',
    '신사동': '7',
    '삼성/역삼': '22',
    '용산': '23',
    '대학로': '21',
    '서초동': '9',
    '기타서울': '10',
    '헤이리': '11',
    '경기인천': '12',
    '부산': '13',
    '대구경상': '14',
    '대전충청': '15',
    '광주전라': '16',
    '강원': '17',
    '제주': '18',
    '한국': '19',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('gallery_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|WEBSITE|SOURCE2|XCOORD|YCOORD@@갤러리\n")

    for area_name in area_list:
        page = 1
        while True:
            store_list = getStores(area_list[area_name], page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['website'])
                outfile.write(u'%s|' % u'김달진미술연구소')
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 99: break
            elif len(store_list) < 20: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(area_code, intPageNo):
    # 'http://www.daljin.com/?WS=51&GNO=&area=4&BC=|5'
    url = 'http://www.daljin.com'
    api = '/'
    data = {
        'WS': '51',
        'GNO': '',
        'kind': '5',    # '갤러리'만 추출
    }
    data['area'] = area_code
    data['BC'] = '|' + str(intPageNo)
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

    entity_list = tree.xpath('//div[@class="thumbNail-list"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//span')
        if len(info_list) < 3: continue  # 최소 3개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['name'] = strtemp    # 후처리 모듈에서 이름 정규화
            #store_info['name'] = strtemp.replace(' ', '/').replace('⋅', '/')

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')

        store_info['newaddr'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        temp_list = info_list[0].xpath('.//a/@href')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        subapi = temp_list[0].lstrip().rstrip()
        suburls = url + api + subapi

        try:
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


        subinfo_list = subtree.xpath('//div[@class="detail-view type01"]//ul//li')

        for j in range(len(subinfo_list)):
            strtemp = "".join(subinfo_list[j].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if strtemp.startswith('홈페이지'):
                    store_info['website'] = strtemp[4:].lstrip()
                elif strtemp.startswith('주소'):
                    strtemp = strtemp[2:].lstrip()
                    if strtemp[0] >= '0' and strtemp[0] <= '9':  # 우편번호 정보 제거
                        idx = strtemp.find(' ')
                        if idx != -1: strtemp = strtemp[idx+1:].lstrip()
                        else:
                            idx = strtemp.find(',')
                            if idx != -1: strtemp = strtemp[idx+1:].lstrip()

                    store_info['newaddr'] = strtemp


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
