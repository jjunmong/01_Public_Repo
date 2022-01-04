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

    outfile = codecs.open('gosione_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|COST|FEAT|SOURCE2@@고시원\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['cost'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s\n' % u'고시원닷넷')

        page += 1

        if page == 49: break     # 2018년5월 기준 20까지
        elif len(store_list) < 25: break    # 30개씩 반환하는데 중간에 불량 데이터가 있어서 2개 정도의 오차는 허용

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.gosione.net'
    api = '/board/list_nation_seoul.php'
    data = {
        'table': 'member',
        'field': '',
        'keyword': '',
        'address': '',
    }
    data['start'] = (intPageNo-1)*30
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
    #response = unicode(response, 'euc-kr')     # 'euc-kr'로 선언되어 있는데 utf8코드값으로 반환 (2019/1)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)

    entity_list = tree.xpath('//table[@bgcolor="#EAEAEA"]//tr[@bgcolor="#CCCCCC"]')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 6개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['feat'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('♥', '').replace('★', '').replace('◆', '').replace('▣', '')\
                .replace('<', '(').replace('>', ')').rstrip().lstrip()   # '♥신설오픈♥탑리빙텔 ★★★' <= 이런 이름도 있음 ㅠㅠ
            if strtemp.find('(신설)') != -1:
                store_info['feat'] = '신설'
                strtemp = strtemp.replace('(신설)', '').rstrip().lstrip()
            elif strtemp.find('신설오픈') != -1:
                store_info['feat'] = '신설'
                strtemp = strtemp.replace('신설오픈', '').rstrip().lstrip()

            if strtemp.endswith(')'):
                idx = strtemp.rfind('(')
                if idx >= 4:
                    strtail = strtemp[idx+1:-1].lstrip().rstrip()
                    strhead = strtemp[:idx].rstrip()
                    if strhead.endswith('점'):
                        if store_info['feat'] != '': store_info['feat'] += ';'
                        store_info['feat'] = strtail
                        strtemp = strhead
                    elif strtail.endswith('점'):
                        strtemp = strhead + ' ' + strtail
                    else:
                        if store_info['feat'] != '': store_info['feat'] += ';'
                        store_info['feat'] = strtail
                        strtemp = strhead

            if strtemp.endswith('점'):
                idx = strtemp.rfind(' ')
                if idx != -1:
                    store_info['subname'] = strtemp[idx+1:].lstrip()
                    strtemp = strtemp[:idx].rstrip()
                else:
                    idx = strtemp.rfind('텔')
                    if idx >= 5:
                        store_info['subname'] = strtemp[idx+1:].lstrip()
                        strtemp = strtemp[:idx].rstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['cost'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['cost'] = strtemp.replace(' ', '')

        # 기타 속성정보도 추출할 수 있음

        store_info['pn'] = ''
        store_info['addr'] = ''

        temp_list = info_list[1].xpath('.//a/@href')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        subapi = temp_list[len(temp_list)-1].lstrip().rstrip()     # 맨 뒤의 subapi가 상세정보페이지 subapi
        if subapi.find('sn=3389') != -1 or subapi.find('sn=3163') != -1:    # 불량 데이터 ㅠㅠ (이상한 문자가 결과에 포함되어 있어, 결과 문자열 utf8 변환과정에서 오류 발생하고 프로그램 종료됨...)
            store_list += [store_info];
            continue
        try:
            suburls = url + '/board/' + subapi
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
        subresponse = unicode(subresponse, 'euc-kr')
        #print(subresponse)
        subtree = html.fromstring(subresponse)
        #subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)

        subinfo_list = subtree.xpath('//table[@bordercolor="#FFFFFF"]//tr')
        for j in range(len(subinfo_list)):
            value_list = subinfo_list[j].xpath('.//td')

            if len(value_list) < 2: continue

            tag = "".join(value_list[0].itertext())
            value = "".join(value_list[1].itertext())

            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', ' ').lstrip().rstrip()

            if tag == '전화번호': store_info['pn'] = value.replace(' ', '')
            elif tag == '주소': store_info['addr'] = value
            elif tag == '주소명': store_info['addr'] = value
            elif tag.startswith('주소'): store_info['addr'] = value

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
