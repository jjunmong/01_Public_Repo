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

    page = 1

    outfile = ''
    if page == 1:
        outfile = codecs.open('knto_tour_utf8.txt', 'w', 'utf-8')
        outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|TYPE|FEAT|PARKING|COST|OT|DATE|ID|XCOORD|YCOORD|SOURCE2@@관광지\n")
    else:
        outfile = codecs.open('knto_tour_utf8.txt', 'a', 'utf-8')

    while True:
        store_list = getStore(page)
        if store_list == None: break

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['type'])
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

        if page == 2499: break      # 2018년12월 19,679건 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/12)
def getStore(intPageNo):
    url = 'https://korean.visitkorea.or.kr'
    api = '/call'

    data = {
        'cmd': 'TOUR_CONTENT_LIST_VIEW',
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
        store_info['feat'] = ''

        if entity_list[i].get('title'):
            strtemp = entity_list[i]['title'].lstrip().rstrip()
            if strtemp.endswith(']'):   # '부산 참앤참[한국관광품질인증/Korea Quality]'와 같은 경우 처리
                idx = strtemp.rfind('[')
                if idx > 0:
                    store_info['feat'] = strtemp[idx+1:-1].lstrip().rstrip().replace(' /', '/').replace('/ ', '/')
                    strtemp = strtemp[:idx].rstrip()
            store_info['name'] = strtemp

        store_info['id'] = ''
        if entity_list[i].get('cotId'):
            store_info['id'] = entity_list[i]['cotId']

        store_info['newaddr'] = ''
        if entity_list[i].get('addr1'):
            store_info['newaddr'] = entity_list[i]['addr1']

        store_info['type'] = ''
        if entity_list[i].get('tagName'):
            if store_info['feat'] != '': store_info['feat'] += ';'
            if entity_list[i]['tagName'] != '':
                strtemp = entity_list[i]['tagName']
                store_info['feat'] += strtemp.replace('|', ';')
                strtemp = '|' + strtemp + '|'
                if strtemp.find('|관광지|') != -1:
                    store_info['type'] = '관광지'
                if strtemp.find('|문화시설|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '문화시설'
                if strtemp.find('|레포츠|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '레포츠'
                if strtemp.find('|쇼핑|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '쇼핑'
                if strtemp.find('|숙박|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '숙박'
                if strtemp.find('|음식|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '음식'
                if strtemp.find('|실내여행지|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '실내여행지'
                if strtemp.find('|체험|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '체험'
                if strtemp.find('|역사|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '역사'
                if strtemp.find('|자연|') != -1:
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += '자연'

        store_info['pn'] = ''
        if entity_list[i].get('telNo'):
            store_info['pn'] = entity_list[i]['telNo'].replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

        store_info['cost'] = ''
        store_info['ot'] = ''
        store_info['date'] = ''
        store_info['parking'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        # store_list += [store_info]
        # continue

        suburl = 'https://korean.visitkorea.or.kr/call'
        subparams = 'cmd=TOUR_CONTENT_BODY_VIEW&cotid=' + store_info['id'] + '&locationx=0&locationy=0'

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
                store_info['parking'] = info_list[0]['parking'].replace('\r', '').replace('\t', '').replace('\n', '').replace('<br>', '').replace('<br />', '').lstrip().rstrip()

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
