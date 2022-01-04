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

    outfile = codecs.open('wedding_hall_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|OT|FEAT|COST|PARKING|WEBSITE|SOURCE2@@결혼식장\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['cost'])
            outfile.write(u'%s|' % store['parking'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s\n' % u'웨딩포털웨버')

        page += 1

        if page == 79: break        # 2018년5월 52까지 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.wever.co.kr'
    api = '/v/weddinghall/index.html'
    data = {
        'do': '',
        'si': '',
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

    entity_list = tree.xpath('//div[@class="iWdhallInfo"]//ul')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//li')
        if len(info_list) < 1: continue  # 최소 1개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['pn'] = ''
        store_info['addr'] = ''
        store_info['ot'] = ''
        store_info['feat'] = ''
        store_info['cost'] = ''
        store_info['website'] = ''
        store_info['parking'] = ''

        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['name'] = strtemp.replace(' ', '/')


        temp_list = info_list[0].xpath('./@onclick')
        if len(temp_list) < 1: continue

        strtemp = temp_list[0]
        idx = strtemp.find('layerControl(event')
        if idx == -1: continue
        strtemp = strtemp[idx+18:]
        idx = strtemp.find('\'')
        if idx == -1: continue
        strtemp = strtemp[idx+1:].lstrip()
        idx = strtemp.find('\'')
        if idx == -1: continue
        strtemp = strtemp[:idx].rstrip()

        suburls = 'http://www.wever.co.kr/v/weddinghall/layer_pop.html?a=' + strtemp

        try:
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        # print(subresponse)
        #subtree = html.fromstring(subresponse)
        subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)

        subinfo_list = subtree.xpath('//div[@class="puHallInfo"]//tbody//tr')

        for j in range(len(subinfo_list)):
            tag_list = subinfo_list[j].xpath('.//th')
            value_list = subinfo_list[j].xpath('.//td')
            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            value = "".join(value_list[0].itertext())

            if tag == None:
                temp_list = subinfo_list[j].xpath('.//th//img/@alt')
                if len(temp_list) > 0:
                    tag = temp_list[0]
            elif tag == "":
                temp_list = subinfo_list[j].xpath('.//th//img/@alt')
                if len(temp_list) > 0:
                    tag = temp_list[0]

            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').rstrip().lstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if tag.find('운영시간') != -1: store_info['ot'] = value
            elif tag.find('전화') != -1: store_info['pn'] = value
            elif tag.find('소재지') != -1: store_info['addr'] = value
            elif tag.find('홈페이지') != -1:
                if value.endswith(')'):
                    idx = value.rfind('(')
                    if idx != -1:
                        value = value[idx+1:-1].lstrip().rstrip()
                store_info['website'] = value
            elif tag.find('홀/연회장') != -1:
                store_info['feat'] = value
            elif tag.find('가격') != -1:
                store_info['cost'] = value
            elif tag.find('주차') != -1:
                store_info['parking'] = value

            # 기타 정보도 있음 (필요하면 추출할 것)

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
