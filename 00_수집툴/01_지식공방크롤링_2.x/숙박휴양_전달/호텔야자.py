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

sido_list = ['경기','광주','대구','대전','부산','서울','세종','울산','인천','충남','충북','강원']
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

    outfile = codecs.open('hotelyaja_all_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|WEBSITE|FEAT@@호텔야자\n")

    outfile2 = codecs.open('hotelyaja_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|ADDR|WEBSITE|FEAT@@호텔야자\n")

    outfile3 = codecs.open('yammotel_all_utf8.txt', 'w', 'utf-8')
    outfile3.write("##NAME|SUBNAME|TELNUM|ADDR|WEBSITE|FEAT@@얌모텔\n")

    for sido in sido_list:
        page = 1
        while True:
            store_list = getStores(sido,page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['website'])
                outfile.write(u'%s\n' % store['feat'])

                if store['name'] == '호텔야자':
                    outfile2.write(u'%s|' % store['name'])
                    outfile2.write(u'%s|' % store['subname'])
                    outfile2.write(u'%s|' % store['pn'])
                    outfile2.write(u'%s|' % store['addr'])
                    outfile2.write(u'%s|' % store['website'])
                    outfile2.write(u'%s\n' % store['feat'])

                if store['name'] == '얌모텔':
                    outfile3.write(u'%s|' % store['name'])
                    outfile3.write(u'%s|' % store['subname'])
                    outfile3.write(u'%s|' % store['pn'])
                    outfile3.write(u'%s|' % store['addr'])
                    outfile3.write(u'%s|' % store['website'])
                    outfile3.write(u'%s\n' % store['feat'])

            page += 1

            if page == 49: break
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()
    outfile3.close()


def getStores(sido,intPageNo):
    # 'http://www.hotelyaja.com/src/map_list.php'
    url = 'https://www.yanoljalab.com'
    api = '/src/map_list.php'
    data = {
        'sigun': '',
        'b_brand_code': '',
        'searchText': '',
        'search_make': '',
    }
    data['page'] = intPageNo
    data['sido'] = sido
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
    entity_list = response_json['msg']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = ''
        strtemp = entity_list[i]['tm_name']
        if strtemp.find('YAJA') != -1: store_info['name'] = '호텔야자'
        elif strtemp.find('YAM') != -1: store_info['name'] = '얌모텔'
        else: store_info['name'] = strtemp

        store_info['subname'] = entity_list[i]['bm_name'].replace(' ', '/')

        store_info['addr'] = entity_list[i]['b_group_addr'].lstrip().rstrip()
        store_info['pn'] = entity_list[i]['b_group_tel'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['website'] = entity_list[i]['b_link']

        store_info['feat'] = ''
        strtemp = entity_list[i]['b_group_park_yn']
        if strtemp == 'Y':
            store_info['feat'] = '주차가능'

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
