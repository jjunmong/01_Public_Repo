# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
import urllib2
import random
import json
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

    outfile = codecs.open('nhis_healthcheck_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OT|FEAT|XCOORD|YCOORD@@건강검진센터\n")

    page = 1
    retry_count = 0
    while True:
        store_list = getStores(page)
        if store_list == None:
            if retry_count > 3: break
            else:
                retry_count += 1
                continue

        retry_count  = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2999: break   # 2019년1월 2220 page까지
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://hi.nhis.or.kr/ca/ggpca001/ggpca001_p06.do'
    url = 'http://hi.nhis.or.kr'
    api = '/ca/ggpca001/ggpca001_p06.do'
    data = {
        'isMobile': '',
        'isParam': 'N',
        'searchType': 'examOrg',
        'pageFirst': 'N',
        'pageSize': '5',
        'viewType': '',
        'ykiho': '',
        'cur_sido_nm': '',
        'cur_sigungu_nm': '',
        'cur_emd_nm': '',
        'search_sido_nm': '',
        'search_sigungu_nm': '',
        'search_emd_nm': '',
        'latitude': '',
        'longitude': '',
        'lat': '',
        'lng': '',
        #'radius': '1000',
        'radius': '',
        'gpsYn': '',
        'search_sido': '',
        'search_sigungu': '',
        'search_emd_gubun': 'emd',
        'search_emd': '',
        'search_road': '',
        'search_name': '',
    }
    data['pageNum'] = intPageNo
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
        req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    try:
        response = result.read()
        # print(response)
        entity_list = json.loads(response)['list']
    except:
        print('invalid return value');      return None

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = entity_list[i]['HP_NAME']
        store_info['subname'] = ''

        store_info['newaddr'] = ''
        if entity_list[i].get('HP_ADDR'):
            store_info['newaddr'] = entity_list[i]['HP_ADDR'].lstrip().rstrip()

        store_info['pn'] = ''
        if entity_list[i].get('HP_TELNO'):
            store_info['pn'] = entity_list[i]['HP_TELNO'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = entity_list[i]['HP_KIHO']
        store_info['feat'] = entity_list[i]['TYPE_LIST']
        store_info['ot'] = entity_list[i]['HP_DESC']


        store_info['xcoord'] = entity_list[i]['LNG']
        store_info['ycoord'] = entity_list[i]['LAT']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
