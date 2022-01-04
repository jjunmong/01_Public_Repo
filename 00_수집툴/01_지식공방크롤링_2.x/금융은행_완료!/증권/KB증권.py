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
#import json
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

    outfile = codecs.open('kbstock_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|XCOORD|YCOORD@@KB증권\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 49: break
        elif len(store_list) < 5: break

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.kbsec.com'
    api = '/go.able?linkcd=m06030020'
    data = {
        'sidoName': '',
        'gugunName': '',
        'branchName': '',
    }
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #'Content-Length': '42',
        #'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'WMONID=s1Ls3dgQj1-; JSESSIONID=7J6I9oYFxBOIDCRFpcaVlL0Bc6ei0a94i0H0zOmNynN7YNY9MPTwX7U7n5HokEfl.d1wasla02_servlet_engine1; HostName=[R]; UserType=; _ga=GA1.2.1877976194.1510220198; _gid=GA1.2.2098217139.1510220198',
        # 2017년7월에 Cookie값 Header에 추가함, Cookie값 갱신해 주어야 함, 커멘트 처리한 값들은 header에 모두 추가하면 api 호출 오류 발생
        #'Host': 'www.kbsec.com',
        #'Origin:': 'https://www.kbsec.com',
        #'Referer': 'https://www.kbsec.com/go.able?linkcd=m06030020',
        #'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    }

    try:
        req = urllib2.Request(url + api, params, headers=hdr)
        #req = urllib2.Request(url + api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)
    #tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@class="tbData tbEven"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = 'KB증권'

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.endswith('센터'): pass
            elif not strtemp.endswith('지점') and strtemp != '본점': strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = info_list[4].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('viewMap(')
            if idx != -1:
                strtemp = strtemp[idx+8:]
                idx = strtemp.find(')')
                coord_list = strtemp[:idx].split(',')
                if len(coord_list) >= 2:
                    store_info['xcoord'] = coord_list[1].lstrip().rstrip()[1:-1]
                    store_info['ycoord'] = coord_list[0].lstrip().rstrip()[1:-1]

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
