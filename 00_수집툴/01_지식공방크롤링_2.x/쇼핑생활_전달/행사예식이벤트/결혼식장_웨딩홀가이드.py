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
    '대전': '042'
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

    outfile = codecs.open('wedding_hall2_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|COST|COST2|SIZE|FEAT|SOURCE2@@결혼식장\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['cost'])
            outfile.write(u'%s|' % store['cost2'])
            outfile.write(u'%s|' % store['size'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s\n' % u'웨딩홀가이드')

        page += 1

        if page == 99: break        # 2018년5월 77까지 있음
        elif len(store_list) < 12: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.weddinghallguide.com'
    api = '/hall/ajax_hall_list.asp'
    data = {
        'page_sep': '0',
        'sido': '',
        'gugun': '',
        'wSub': '',
        'wSub1': '',
        'wType': '',
        'wFood': '',
        'wFoodMenu': '',
        'wHuman': '',
        'coupon': '',
        'gift': '',
        'wRelFlag': '',
        'eventView': '',
        'movie': '',
        'keyword': '',
        'pagesize': '',
        'order': '',
        'list_type': '',
    }
    data['gotopage'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #'Content-Length': '30',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'Cookie': 'session_cookie=db340ce2fcdeabf9fda2b50c14d35a3ced533934ae2ef2df2ba70f5719e62fba768bca163cdc6f186b42ca30473008ea83d3c21215bac42720189bb3c6d890e0c9c2461b3afd3b0590afbac66f34624887df20bb8e50e7bcbbc8356a6002a3e5; JSESSIONID=B4M8dBc7PW15pk9J3rfkkl4EJhdfuKAql12KGmvFvr1OqOfGMxRnQMOown5SlS6z.etwas2_servlet_engine1; XTVID=A180501152249739329; _ga=GA1.3.1159740144.1525155770; _gid=GA1.3.393662324.1525155770; _gat_gtag_UA_111271396_1=1; xloc=2560X1440; UID=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        #req.get_method = lambda: 'POST'
        #result = urllib2.urlopen(req)

        result = urllib.urlopen(url+api+'?'+params)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)

    entity_list = tree.xpath('//ul[@class="weddingHall_album"]//li')

    store_list = []
    for i in range(len(entity_list)):

        subapi_list = entity_list[i].xpath('.//a[@id="a_hall_view"]/@data')
        if len(subapi_list) < 1: continue

        suburls = url + subapi_list[0]

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
        #print(subresponse)
        subtree = html.fromstring(subresponse)
        #subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['pn'] = ''
        store_info['addr'] = ''
        store_info['newaddr'] = ''
        store_info['feat'] = ''
        store_info['cost'] = ''
        store_info['cost2'] = ''
        store_info['size'] = ''

        tag_list = subtree.xpath('//div[@class="info_area"]//dl//dt//img/@alt')
        value_list = subtree.xpath('//div[@class="info_area"]//dl//dd')

        for j in range(len(tag_list)):
            if len(value_list) < j: break   # for safety

            tag = tag_list[j]
            value = "".join(value_list[j].itertext())

            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').rstrip().lstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if tag.find('도로명주소') != -1: store_info['newaddr'] = value
            elif tag.find('주소') != -1: store_info['addr'] = value
            elif tag.find('웨딩홀명') != -1: store_info['name'] = value
            elif tag.find('연락처') != -1: store_info['pn'] = value
            elif tag.find('식사비용') != -1: store_info['cost'] = value
            elif tag.find('사용료') != -1: store_info['cost2'] = value
            elif tag.find('인원') != -1: store_info['size'] = value
            elif tag.find('메뉴종류') != -1:
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += value
            elif tag.find('예식형태') != -1:
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += value
            elif tag.find('가능행사') != -1:
                if store_info['feat'] != '': store_info['feat'] += ';'
                temp_list = value_list[j].xpath('.//em')
                for k in range(len(temp_list)):
                    if k != 0: store_info['feat'] += '/'
                    store_info['feat'] += temp_list[k].text

            # 기타 정보도 있음 (필요하면 추출할 것)

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
