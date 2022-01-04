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


    outfile = codecs.open('insurance_nhlife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|KATECX|KATECY@@농협생명\n")

    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores(page)
        page += 1

        if store_list == None: break;
        elif len(store_list) > 0:
            if store_list[0]['id'] ==  sentinel_store_id: break
            else: sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['katecx'])
            outfile.write(u'%s\n' % store['katecy'])

        if page == 999: break       # 948 페이지까지 있음 (2017년 5월 기준)
        elif len(store_list) < 5: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(intPageNo):
    url = 'https://www.nhlife.co.kr'
    api = '/ho/cc/HOCC0034P02.nhl'
    data = {
        'brofCd': '',
        'ctynm': '',
        'ccwnm': '',
        'searchProdGnntfMccd': '',
        'searchProdGnntfSmcd': '',
        'brofDcd': '',
        'srchCndnm': 'brofnm',
        'srchKywNm': '',
    }
    data['prsPagcn'] = intPageNo
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
        #req = urllib2.Request(url+api, None, headers=hdr)
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
    tree = html.fromstring(response)
    entity_list = tree.xpath('//div[@class="tblWrap headY"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        name_list = entity_list[i].xpath('.//th')
        info_list = entity_list[i].xpath('.//td')
        if len(name_list) < 1 or len(info_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '농협생명'
        store_info['type'] = '농협생명'

        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            # 브랜드명/지점명 교정
            if strtemp.startswith('NH농협생명'): strtemp = strtemp[6:].lstrip()
            else:
                idx = strtemp.find('농협')
                if idx != -1:
                    store_info['type'] = '농축협'
                    store_info['name'] = strtemp[:idx+2]
                    strtemp = strtemp[idx+2:].lstrip()
                else:
                    idx = strtemp.find('협 ')
                    if idx != -1:
                        store_info['type'] = '농축협'
                        store_info['name'] = strtemp[:idx+1]
                        strtemp = strtemp[idx+1:].lstrip()

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        store_info['katecx'] = ''
        store_info['katecy'] = ''

        store_info['pn'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = info_list[1].xpath('.//button/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('viewPage(')
            if idx != -1:
                strtemp = strtemp[idx+9:]
                idx = strtemp.find(');')
                store_info['id'] = strtemp[:idx].lstrip().rstrip()[1:-1]


        if store_info['id'] != '':
            subdata = {
                #'brofCd': '',
                'ctynm': '',
                'ccwnm': '',
                'searchProdGnntfMccd': '',
                'searchProdGnntfSmcd': '',
                'brofDcd': '',
                'srchCndnm': 'brofnm',
                'srchKywNm': '',
            }
            subdata['prsPagcn'] = intPageNo
            subdata['brofCd'] = store_info['id']
            subparams = urllib.urlencode(subdata)
            print(subparams)


            suburls = 'http://www.nhlife.co.kr/ho/cc/HOCC0034P01.nhl'
            print(suburls)

            try:
                time.sleep(random.uniform(0.3, 0.9))
                subreq = urllib2.Request(suburls, subparams)
                subreq.get_method = lambda: 'POST'
                subresult = urllib2.urlopen(subreq)
            except:
                print('Error calling the subAPI');
                store_list += [store_info];     continue

            code = subresult.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code);
                store_list += [store_info];      continue

            subresponse = subresult.read()
            #print(subresponse)

            subtree = html.fromstring(subresponse)
            subinfo_list = subtree.xpath('//div[@class="branchinfo"]//dd')

            idx = subresponse.find('.Point(')
            if idx != -1:
                strtemp = subresponse[idx+7:].lstrip()
                idx = strtemp.find(')')
                temp_list = strtemp[:idx].split(',')
                if len(temp_list) >= 2:
                    store_info['katecx'] = temp_list[0].lstrip().rstrip()[1:-1]
                    store_info['katecy'] = temp_list[1].lstrip().rstrip()[1:-1]

            if len(subinfo_list) < 1:
                store_list += [store_info];     continue

            strtemp = "".join(subinfo_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['newaddr'] = strtemp

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
