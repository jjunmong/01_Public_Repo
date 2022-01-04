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

    outfile = codecs.open('volvo_svc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@볼보서비스센터\n")

    page = 1
    for page in range(1,2,1):       # 한 페이지에 전체 센터 정보가 모두 있어 한번만 호출하면 됨
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    # 'https://www.volvocars.com/kr/own/own-and-enjoy/service-center'
    url = 'https://www.volvocars.com'
    #api = '/kr/services/services/service-center'
    #api = '/kr/services/explore/service-center'     # api 변경됨 (2017/12)
    api = '/kr/own/own-and-enjoy/service-center'     # api 변경됨 (2018/7)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control' : 'max-age=0',
        #'Cookie' : 'utag_main=v_id:015bdecbba0d00203974c61a068c04072003c06a00fb8$_sn:1$_ss:1$_pn:1%3Bexp-session$_st:1494091725101$ses_id:1494091545101%3Bexp-session; _ga=GA1.2.754271012.1494091545; _gid=GA1.2.1098272537.1494091545; _gat_new_site=1; ak_bmsc=5BC3B95F8E6B816A932B02C1CA9C199948F6675F1345000015070E597661D324~plPKDiDW7GcTyW0T5kxpvss1lOuFpsPbFA8woC3mITLu4GGPZyD4hQPef1py+C1auc6Uonc7YVRN0ZdOaRWjw5uuPZ2pJl1CdjkEIowjFPA4HMbQwVTzKRX1hCDjXPHmCXuh32yL9UkRjp4IgspB9ZUpblNgYXUM2yy1yDEHCBJ77JSTjXAVe6gQWBohlmprs4qacj5PhChjUTfnsqNaXQZQ==; ADRUM=s=1494091551848&r=http%3A%2F%2Fwww.volvocars.com%2Fkr%2Fservices%2Fservices%2Fservice-center%3F0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        urls = url + api
        print(urls)
        req = urllib2.Request(urls, None, headers=hdr)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="items-list "]//div[@class="il-medium     "]')     # 가끔씩 '@class'의 값이 변경됨 ㅠㅠ

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//p[@style="bold;font-size:25px"]')
        if len(info_list) < 1:
            info_list = entity_list[i].xpath('.//p[@style="bold;font-size:24px"]')      # '24px'인 항목도 있음 (added on 2017/12)
            if len(info_list) < 1:
                continue

        extra_info_list = entity_list[i].xpath('.//div[@class="inner-wrapper"]')

        store_info = {}

        store_info['name'] = '볼보서비스센터'
        store_info['subname'] = ''
        store_info['addr'] = '';     store_info['newaddr'] = '';        store_info['pn'] = ''
        str_orgname = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            str_orgname = strtemp
            store_info['subname'] = strtemp.replace('(주)', '').rstrip().lstrip().replace(' ', '/')

        strtemp = info_list[0].tail
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('TEL')
            if idx != -1:
                store_info['newaddr'] = strtemp[:idx].rstrip()
                strtemp = strtemp[idx+5:].lstrip()
                if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
            else:   # 정보가 다르게 들어가 있는 항목이 있어서 ㅠㅠ
                if len(extra_info_list) > 0:
                    strtemp2 = "".join(extra_info_list[0].itertext())
                    if strtemp2 != None:
                        strtemp2 = strtemp2.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        idx = strtemp2.find(str_orgname)
                        if idx != -1:
                            strtemp = strtemp2[idx+len(str_orgname):].lstrip()
                            idx = strtemp.find('TEL')
                            if idx != -1:
                                store_info['newaddr'] = strtemp[:idx].rstrip()
                                strtemp = strtemp[idx + 5:].lstrip()
                                if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()

            idx = strtemp.find('FAX')
            if idx != -1:
                store_info['pn'] = strtemp[:idx].rstrip().replace('.', '-').replace(')', '-')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
