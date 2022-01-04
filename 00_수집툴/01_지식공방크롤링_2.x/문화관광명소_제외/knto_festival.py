# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import codecs
import time
import random
import urllib
import urllib2
import json
from lxml import html

area = {
    '서울특별시': 'seoul',
}

area2 = {
    '서울특별시': 'seoul',
    '광주광역시': 'kwangju',
    '대구광역시': 'daegu',
    '대전광역시': 'daejeon',
    '부산광역시': 'busan',
    '울산광역시': 'ulsan',
    '인천광역시': 'incheon',
    '경기도': 'gyenggi',
    '강원도': 'gangwon',
    '경상남도': 'kyungnam',
    '경상북도': 'kyungbuk',
    '전라남도': 'jeonnam',
    '전라북도': 'jeonbuk',
    '충청남도': 'chungnam',
    '충청북도': 'chungbuk',
    '제주특별자치도': 'jeju',
    '세종특별자치시': 'sejong',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('knto_festival_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|PARKING|COST|OT|DATE|ID|XCOORD|YCOORD|SOURCE2@@지역축제\n")

    page = 1
    while True:
        #store_list = getFestivals('2019', '04', page)
        store_list = getFestivals('2019', '', page)
        if store_list == None: break

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['parking'])
            outfile.write(u'%s|' % store['cost'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['date'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s|' % store['ycoord'])
            outfile.write(u'%s\n' % u'한국관광공사')

        page += 1

        if page == 299: break   # 2018년12월 기준 1639곳 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/12)
def getFestivals(req_year, req_month, intPageNo):
    url = 'https://korean.visitkorea.or.kr'
    api = '/call'

    data = {
        'cmd': 'FESTIVAL_CONTENT_LIST_VIEW',
        #'year': '2018',
        'month': 'All',
        'areaCode': 'All',
        'sigunguCode': 'All',
        'tagId': 'All',
        'locationx': '0',
        'locationy': '0',
        #'page': '1',
        'sortkind': '1',  # 최신순
        'cnt': '10',
    }
    data['year'] = req_year
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    # print(params)
    print('%d' % intPageNo)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'o-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,fr;q=0.5,it;q=0.4,zh-CN;q=0.3,zh;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url + api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');
        return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);
        return None

    response = result.read()

    response_json = json.loads(response)
    entity_list = response_json['body']['result']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}
        store_info['name'] = ''
        store_info['subname'] = ''

        if entity_list[i].get('title'):
            store_info['name'] = entity_list[i]['title']

        store_info['id'] = ''
        if entity_list[i].get('cotId'):
            store_info['id'] = entity_list[i]['cotId']

        store_info['newaddr'] = ''
        if entity_list[i].get('addr1'):
            store_info['newaddr'] = entity_list[i]['addr1']

        store_info['feat'] = ''
        if entity_list[i].get('tagName'):
            store_info['feat'] = entity_list[i]['tagName'].replace('|', ';')

        store_info['pn'] = ''
        if entity_list[i].get('telNo'):
            store_info['pn'] = entity_list[i]['telNo']

        store_info['cost'] = ''
        store_info['ot'] = ''
        store_info['date'] = ''
        store_info['parking'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        # store_list += [store_info]
        # continue

        suburl = 'https://korean.visitkorea.or.kr/call'
        subparams = 'cmd=FESTIVAL_CONTENT_BODY_VIEW&cotid=' + store_info['id'] + '&locationx=0&locationy=0'

        try:
            time.sleep(random.uniform(0.2, 0.5))
            print(store_info['id'])
            subreq = urllib2.Request(suburl, subparams)
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the suburl');
            store_list += [store_info];
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('suburl HTTP request error (status %d)' % subcode);
            store_list += [store_info];
            continue

        subresponse = subresult.read()

        subresponse = json.loads(subresponse)
        info_list = subresponse['body']['article']

        if len(info_list) > 0:
            if info_list[0].get('useTime'):
                store_info['ot'] = info_list[0]['useTime'].replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

            if info_list[0].get('useCash'):
                store_info['cost'] = info_list[0]['useCash'].replace('\r', '').replace('\t', '').replace('\n', '').replace('<br>', '').lstrip().rstrip()

            if info_list[0].get('startDate'):
                store_info['date'] = info_list[0]['startDate'] + '~'

            if info_list[0].get('endDate'):
                if store_info['date'] == '': store_info['date'] += '~'
                store_info['date'] += info_list[0]['endDate']

            if info_list[0].get('parking'):
                store_info['parking'] = info_list[0]['parking']

            if info_list[0].get('mapX'):
                store_info['xcoord'] = info_list[0]['mapX']

            if info_list[0].get('mapY'):
                store_info['ycoord'] = info_list[0]['mapY']

            # 기타 정보도 있음 (갱신일 등등)

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
