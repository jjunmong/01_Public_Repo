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

    outfile = codecs.open('etland_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|TYPE@@전자랜드\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['type'])

        page += 1

        if page == 49: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(intPageNo):
    # 'http://brand.etland.co.kr/info/branch/branchListAjax.do'
    url = 'http://brand.etland.co.kr'
    api = '/info/branch/branchListAjax.do'
    data = {
        'SHP_MST_AREA': '',
        'SHP_MST_AREA_SUB': '',
        'SEARCH_WORD': '',
    }
    data['cPage'] = intPageNo
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
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['resultMap']['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '전자랜드'
        store_info['subname'] = entity_list[i]['SHP_MST_NM'].replace(' ', '/')

        store_info['id'] = entity_list[i]['SHP_MST_IDX']

        store_info['newaddr'] = entity_list[i]['SHP_MST_ADDR'].lstrip().rstrip()
        store_info['pn'] = entity_list[i]['SHP_MST_TEL'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['type'] = entity_list[i]['SHP_MST_TYPE_NM']

        # suburl 호출로 영업시간 정보, 좌표 정보 추가로 얻을 수 있음

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
