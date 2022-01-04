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

    outfile = codecs.open('nhstock_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ORGNAME|ID|TELNUM|NEWADDR|ETCADDR|XCOORD|YCOORD@@NH투자증권\n")

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
            outfile.write(u'%s|' % store['etcaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 29: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # https://ir.nhqv.com/ir/branch/ajaxGetBranchList.action
    url = 'https://ir.nhqv.com'     # https로 호출해야 동작함!!
    api = '/ir/branch/ajaxGetBranchList.action'
    data = {
        'output': 'json',
        'searchType': '1',
        'search_key': '',
        'mainS': '',
        'subS': '',
        'wm_menu_code': '',
    }
    data['iPg'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

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
    response = unicode(response, 'euc-kr')
    #print(response)
    response_json = json.loads(response)

    entity_list = response_json['DATA']['RESPONSE']['branchList']['ROW']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'NH투자증권'
        store_info['id'] = entity_list[i]['BI_CD']
        store_info['subname'] = ''
        store_info['orgname'] = ''
        strtemp = entity_list[i]['BI_KOR_NM']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            store_info['orgname'] = strtemp
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['BI_KOR_ADDR']
        store_info['etcaddr'] = entity_list[i]['BI_CONTACT_INFO']
        store_info['pn'] = entity_list[i]['BI_PHON_NO'].lstrip().rstrip().replace(')', '-')

        store_info['xcoord'] = entity_list[i]['BI_POINT_X']
        store_info['ycoord'] = entity_list[i]['BI_POINT_Y']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
