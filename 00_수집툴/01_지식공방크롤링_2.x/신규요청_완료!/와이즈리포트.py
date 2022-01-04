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

    outfile = codecs.open('company_kospi_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|WEBSITE@@일반상장기업\n")

    outfile2 = codecs.open('company_kosdaq_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|WEBSITE@@코스닥기업\n")

    outfile3 = codecs.open('company_konex_utf8.txt', 'w', 'utf-8')
    outfile3.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|WEBSITE@@코넥스기업\n")


    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            if store['type'] == u'유가증권시장':
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['website'])
            elif store['type'] == u'코스닥':
                outfile2.write(u'%s|' % store['name'])
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['id'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s\n' % store['website'])
            else:
                outfile3.write(u'%s|' % store['name'])
                outfile3.write(u'%s|' % store['subname'])
                outfile3.write(u'%s|' % store['id'])
                outfile3.write(u'%s|' % store['pn'])
                outfile3.write(u'%s|' % store['newaddr'])
                outfile3.write(u'%s\n' % store['website'])

        page += 1

        if page == 17: break

        time.sleep(random.uniform(1, 2))

    outfile.close()
    outfile2.close()
    outfile3.close()

def getStores(intPageNo):
    url = 'https://comp.wisereport.co.kr'
    api = '/addinfo/getAddInfoData.aspx'
    data = {
        'gubun': '2',
    }
    data['param1'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
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
    entity_list = json.loads(response)['data']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        strtemp = entity_list[i]['CMP_KOR'].lstrip().rstrip()
        store_info['name'] = strtemp.replace(' ', '/')
        store_info['subname'] = ''

        store_info['id'] = entity_list[i]['CMP_CD']
        store_info['type'] = entity_list[i]['MKT_NM']

        store_info['pn'] = ''
        if entity_list[i].get('TEL'):
            store_info['pn'] = entity_list[i]['TEL'].lstrip().rstrip().replace(')', '-')
        store_info['newaddr'] = ''
        if entity_list[i].get('ADDR'):
            store_info['newaddr'] = entity_list[i]['ADDR']
        store_info['website'] = ''
        if entity_list[i].get('URL'):
            store_info['website'] = entity_list[i]['URL']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
