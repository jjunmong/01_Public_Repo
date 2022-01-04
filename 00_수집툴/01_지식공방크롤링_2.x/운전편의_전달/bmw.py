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

    outfile = codecs.open('bmw_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|SUBNAME2|URL|XCOORD|YCOORD@@BMW\n")

    outfile2 = codecs.open('bmw_svc_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|SUBNAME2|URL|XCOORD|YCOORD@@BMW서비스센터\n")

    while True:
        storeList = getStores('service_center')
        if storeList == None: break;

        for store in storeList:
            outfile2.write(u'BMW서비스센터|')
            outfile2.write(u'%s|' % store['name'].replace(' ', '/'))
            outfile2.write(u'%s|' % store['tel'].replace(')', '-'))
            outfile2.write(u'%s|' % store['address_jibun'])
            outfile2.write(u'%s|' % store['address_doro'])

            shop_ot =  store['operating_hour'].lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').replace('<br/>', '')
            outfile2.write(u'%s|' % shop_ot)

            outfile2.write(u'%s|' % store['dealer_name'].replace(' ', '/'))

            outfile2.write(u'%s|' % store['dealer_site'])
            outfile2.write(u'%s|' % store['longitude'])
            outfile2.write(u'%s\n' % store['latitude'])

        time.sleep(random.uniform(0.5, 2.5))
        storeList = getStores('show_room')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'BMW|')
            outfile.write(u'%s|' % store['name'].replace(' ', '/'))
            outfile.write(u'%s|' % store['tel'].replace(')', '-'))
            outfile.write(u'%s|' % store['address_jibun'])
            outfile.write(u'%s|' % store['address_doro'])

            shop_ot =  store['operating_hour'].lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').replace('<br/>', '')
            outfile.write(u'%s|' % shop_ot)

            outfile.write(u'%s|' % store['dealer_name'].replace(' ', '/'))

            outfile.write(u'%s|' % store['dealer_site'])
            outfile.write(u'%s|' % store['longitude'])
            outfile.write(u'%s\n' % store['latitude'])

        break

    outfile.close()
    outfile2.close()

def getStores(type_info):
    url = 'http://www.bmw-dealer-locator.co.kr'
    api = '/api/getList'
    data = {
        'area': 'all',
     }
    data['type'] = type_info
    params = urllib.urlencode(data)

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=sm7h8s2duqhbeq90qhdo1cp555; 2a0d2363701f23f8a75028924a3af643=MTI1LjEyOS4yNDIuMjI3; _gat=1; _ga=GA1.3.1065939222.1486961929'
    }
    try:
        req = urllib2.Request(url + api, params, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)
    storeList = json.loads(response)
    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
