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

    outfile = codecs.open('samsungstock_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ORGNAME|ID|TELNUM|ADDR|NEWADDR|OT|XCOORD|YCOORD@@삼성증권\n")

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
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 29: break
        elif len(store_list) < 9: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.samsungpop.com'
    api = '/ux/kor/customer/guide/workproductguide/domestic_branch_list.do'
    data = {
        'rowsPerPage': '9',
        'SearchText1': '',
        'seq': '',
        'sigun': '0',
        'gubun0': '',
        'gubun1': '',
        'gubun2': '',
        'gubun3': '',
        'gubun4': '',
        'gubun5': '',
        'gubun6': '',
        'gubun7': '',
        'gubun8': '',
        'gubun9': '',
        'gubun10': '',
        'gubun11': '',
        'gubun12': '',
        'gubun13': '',
        'gubun14': '',
        'gubun15': '',
        'gubun16': '',
        'SearchText': '',
        'siteGubun': 'KF',
        'af_auto_index': 'start',
        'ajaxQuery': '1',
    }
    data['currentPage'] = intPageNo
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
    #print(response)
    response_json = json.loads(response)

    entity_list = response_json['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '삼성증권'
        store_info['id'] = entity_list[i]['SetSeqNo']
        store_info['subname'] = ''
        store_info['orgname'] = ''
        strtemp = entity_list[i]['BrNm']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip()
            store_info['orgname'] = strtemp
            if strtemp.endswith('불가)'):
                idx = strtemp.rfind('(')
                strtemp = strtemp[:idx].rstrip()
            if strtemp.endswith('센터'): pass
            elif strtemp.endswith('출장소'): pass
            elif strtemp.endswith('브랜치'): pass
            elif not strtemp.endswith('지점') and strtemp != '본점': strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['BrRoadNmAddr']
        store_info['addr'] = entity_list[i]['Addr']
        store_info['pn'] = entity_list[i]['TelNo'].replace('(*)', '').lstrip().rstrip().replace(')', '-')

        store_info['ot'] = entity_list[i]['BrBizStartTime'] + '~' + entity_list[i]['BrBizEndTime']
        if store_info['ot'] == '-': store_info['ot'] = ''

        store_info['xcoord'] = '';     store_info['ycoord'] = ''
        strtemp = entity_list[i]['URLAddr']
        if strtemp != None:
            idx = strtemp.find('GISYCd=')
            if idx != -1:
                store_info['xcoord'] = strtemp[idx+7:].lstrip()
                strtemp = strtemp[:idx]
                idx = strtemp.find('GISXCd=')
                store_info['ycoord'] = strtemp[idx + 7:].replace('&', '').lstrip()

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
