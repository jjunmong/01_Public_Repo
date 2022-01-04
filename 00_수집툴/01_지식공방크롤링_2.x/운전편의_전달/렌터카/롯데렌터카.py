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

sido_list2 = {      # 테스트용 시도 목록
    '대전': '170'
}

sido_list = {
    '서울': '100',
    '광주': '200',
    '대구': '220',
    '대전': '170',
    '부산': '240',
    '울산': '250',
    '인천': '110',
    '경기': '120',
    '강원': '130',
    '경남': '230',
    '경북': '210',
    '전남': '190',
    '전북': '180',
    '충남': '160',
    '충북': '140',
    '제주': '260',
    '세종': '140'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('lotterentacar_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|NEWADDR|OT|MTYPE|XCOORD|YCOORD@@롯데렌터카\n")

    for sido_name in sorted(sido_list):
        store_list = getStores(sido_list[sido_name])
        if store_list == None: continue

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % u'렌터카')
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_code):
    url = 'https://www.lotterentacar.net'
    api = '/kor/info/CsAreaMapGuide2Ajax.do'
    data = {}
    data['areacode'] = sido_code
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        urls = url + api
        req = urllib2.Request(urls, params, headers=hdr)
        #req = urllib2.Request(urls, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response_json = json.loads(response)     # json 포맷으로 결과값 반환

    entity_list = response_json['resultList']

    store_list = []
    for i in range(len(entity_list)):

        store_info = {}
        store_info['name'] = '롯데렌터카'
        store_info['subname'] = ''

        strtemp = entity_list[i]['NAME_KOR']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['BRANCHCODE']

        store_info['addr'] = ''
        store_info['newaddr'] = ''
        store_info['pn'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        store_info['ot'] = ''

        subdata = {}
        subdata['branchcode'] = store_info['id']
        subparams = urllib.urlencode(subdata)
        print(subparams)

        try:
            time.sleep(random.uniform(0.3, 0.9))
            suburl = 'https://www.lotterentacar.net/kor/info/CsAreaMapGuideAjax.do'
            subreq = urllib2.Request(suburl, subparams, headers=hdr)
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the suburl');      store_list += [store_info];         continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);      store_list += [store_info];         continue

        subresponse = subresult.read()
        subresponse_json = json.loads(subresponse)  # json 포맷으로 결과값 반환

        subinfo_list = subresponse_json['resultList']
        if len(subinfo_list) > 0:
            store_info['addr'] = subinfo_list[0]['ADDR_KOR']
            if subinfo_list[0].get('ADDR_KOR2'):
                store_info['newaddr'] = subinfo_list[0]['ADDR_KOR2']
            store_info['pn'] = subinfo_list[0]['TEL']
            store_info['xcoord'] = subinfo_list[0]['LNG_POINT']
            store_info['ycoord'] = subinfo_list[0]['LTI_POINT']
            store_info['ot'] = subinfo_list[0]['BUSINESSHOUR_KOR']

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
