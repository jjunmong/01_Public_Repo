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

    outfile = codecs.open('kyungnambank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|ETCADDR|XCOORD|YCOORD@@경남은행\n")

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
            outfile.write(u'%s|' % store['etcaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전국 경남은행 점포 다 얻을 수 있음
        elif len(store_list) < 12: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.knbank.co.kr'
    api = '/ib20/act/BHPADSA00MIXA00P?ib20_cur_mnu=BHPADS040000000&ib20_cur_wgt=BHPADSA00MIXV00P'
    data = {}
    params = urllib.urlencode(data)
    #print(params)
    params = 'BR_ADV_DIS_CD=01&BHP_ACTION_TYPE=R&SEL_TYPE=&BR_ID_NO=&BR_CD=&GO_PRINT=&SIDO_NM2=&action_type=act&ib20_action=%2Fib20%2Fact%2FBHPADSA00MIXA00P&ib20_cur_mnu=BHPADS040000000&ib20_cur_wgt=BHPADSA00MIXV00P&ib20_change_wgt=&CHK_BR_ADV_DIS_01=0&INP_TEXT1=&SIDO_NM=&ADM_SGG_NM=&INP_TEXT2=&REQUEST_TOKEN_KEY=BHP0401000157742_0&CHECK_TRAN_KEY=20170419230442326&b_page_id='

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)
        req = urllib2.Request(url + api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #response = unicode(response, 'euc-kr')
    print(response)
    response = urllib.unquote(response).decode('utf8').replace('+', ' ')        # urlencode된 값이 반환되므로 다시 decode해 주어야 함
    response_json = json.loads(response)

    entity_list = response_json['_msg_']['_body_']['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '경남은행'
        store_info['id'] = entity_list[i]['BR_CD']
        store_info['subname'] = entity_list[i]['BR_NM'].lstrip().rstrip().replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = entity_list[i]['BR_BAS_AD']
        if strtemp != None:
            store_info['newaddr'] = strtemp.lstrip().rstrip()

        store_info['etcaddr'] = ''
        strtemp = entity_list[i]['BR_DTL_AD']
        if strtemp != None:
            store_info['etcaddr'] = strtemp.lstrip().rstrip()

        store_info['pn'] = entity_list[i]['BR_ADV_TEL_NO'].replace(')', '-')

        store_info['xcoord'] = entity_list[i]['BR_YCRD']
        store_info['ycoord'] = entity_list[i]['BR_XCRD']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
