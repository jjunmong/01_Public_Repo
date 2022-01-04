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

sido_list2 = {      # 테스트용 시도 목록
    '대전': 'kor_6',
}

sido_list = {
    '서울': 'kor_2',
    '광주': 'kor_11',
    '대구': 'kor_13',
    '대전': 'kor_6',
    '부산': 'kor_16',
    '울산': 'kor_15',
    '인천': 'kor_4',
    '경기': 'kor_1',
    '강원': 'kor_3',
    '경남': 'kor_14',
    '경북': 'kor_8',
    '전남': 'kor_10',
    '전북': 'kor_9',
    '충남': 'kor_5',
    '충북': 'kor_7',
    '제주': 'kor_12',
    #'세종': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('kswiss_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@케이스위스\n")

    page = 1
    for sido_name in sorted(sido_list):
        store_list = getStores(sido_list[sido_name])
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'케이스위스|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(sido_code):
    # 'https://www.k-swiss.co.kr/03stores/stores_listCall.asp'
    url = 'http://www.k-swiss.co.kr'    # 'https'로 호출하면 호출오류 발생 ㅠㅠ
    api = '/03stores/stores_listCall.asp'
    data = {}
    data['rq_sh_w1'] = sido_code
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Encoding': 'deflate, br',       # 'gzip' 옵션이 있으면 압축된 결과를 반환
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_ga=GA1.3.1839621454.1551863541; _gid=GA1.3.1142149256.1551863541; ASPSESSIONIDCUSRARBS=JONDCDMDHMOIOJBGDNNLBHBL',
        'Host': 'www.k-swiss.co.kr',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        #urls = url + api + '?' + params
        #print(urls)
        # result = urllib.urlopen(urls)

        req = urllib2.Request(url+api, params, headers=hdr)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response)
    entity_list = tree.xpath('//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '케이스위스'

        store_info['subname'] = ''
        store_info['type'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if not strtemp.endswith('점'): strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
