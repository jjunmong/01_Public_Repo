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

    outfile = codecs.open('bonobono_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ORGNAME|ID|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@보노보노\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전체 점포 정보 얻을 수 있음

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.shinsegaefood.com'
    api = '/bonobono/store/store.sf'
    data = {}
    params = urllib.urlencode(data)
    #print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)

        print(url+api)  # for debugging
        req = urllib2.Request(url+api, None)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    idx = response.find('var storelist =')
    if idx == -1: return None

    response = response[idx+15:].lstrip()
    idx = response.find('}]')
    response = response[:idx+2]
    entity_list = json.loads(response)

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '보노보노'
        strtemp = entity_list[i]['title']
        store_info['orgname'] = strtemp
        strtemp = strtemp.replace('보노보노', '').lstrip().rstrip()
        if strtemp.startswith('스시'):
            store_info['name'] = '보노보노스시'
            strtemp = strtemp[2:].lstrip()
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['seq']

        strtemp = entity_list[i]['brandDesc']   # 이 필드에 온갖 정보 다 들어가 있음 ㅠㅠ
        strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

        idx = strtemp.find('<br />')
        str_header = strtemp[:idx]
        if str_header.find('<strong>보노보노') != -1:
            strtemp = strtemp[idx+6:].lstrip()
            idx = strtemp.find('<br />')

        store_info['newaddr'] = strtemp[:idx].rstrip()
        strtemp = strtemp[idx+6:].lstrip()
        idx = strtemp.find('<br />')
        store_info['pn'] = strtemp[:idx].replace('예약문의', '').replace('문의', '').replace(':', '').replace(' ', '').replace(')', '-').lstrip().rstrip()
        strtemp = strtemp[idx+6:].lstrip()
        strtemp = strtemp.replace('<br />', '-').replace('&nbsp;', '-').replace('ㅣ', '/').lstrip().rstrip()
        idx = strtemp.find('--')
        if idx != -1: strtemp = strtemp[:idx]
        idx = strtemp.find('지하철')
        if idx != -1: strtemp = strtemp[:idx]
        store_info['ot'] = strtemp.replace('-', ' ').lstrip().rstrip()

        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        strtemp = entity_list[i]['imgUrl']
        idx = strtemp.find(',')
        if idx != -1:
            store_info['xcoord'] = strtemp[:idx].lstrip().rstrip()
            store_info['ycoord'] = strtemp[idx+1:].lstrip().rstrip()

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
