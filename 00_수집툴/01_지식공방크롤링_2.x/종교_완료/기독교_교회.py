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
    '서울': '02',
}

sido_list = {
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

    outfile = codecs.open('church_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|TYPE|SUBNAME|TELNUM|ADDR|FATHER|SOURCE2@@교회\n")

    for sido_name in sorted(sido_list):
        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['father'])
                outfile.write(u'%s\n' % u'한국컴퓨터선교회')

            page += 1

            if page == 1999: break
            elif len(store_list) < 30: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'http://kcm.kr'
    api = '/search_address.php'
    data = {
        'f': 'address',
        #'kword': '',
        'u_sort': '',
        'u_order': '',
        'map_area1': '0',
        'map_area2': '0',
    }
    data['kword'] = sido_name.encode('euc-kr')      # 파라미터를 euc-kr로 변환해서 지정한 다음 urlencode해야 함
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #'Content-Length': '30',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'Cookie': 'session_cookie=db340ce2fcdeabf9fda2b50c14d35a3ced533934ae2ef2df2ba70f5719e62fba768bca163cdc6f186b42ca30473008ea83d3c21215bac42720189bb3c6d890e0c9c2461b3afd3b0590afbac66f34624887df20bb8e50e7bcbbc8356a6002a3e5; JSESSIONID=B4M8dBc7PW15pk9J3rfkkl4EJhdfuKAql12KGmvFvr1OqOfGMxRnQMOown5SlS6z.etwas2_servlet_engine1; XTVID=A180501152249739329; _ga=GA1.3.1159740144.1525155770; _gid=GA1.3.393662324.1525155770; _gat_gtag_UA_111271396_1=1; xloc=2560X1440; UID=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
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

    entity_list = tree.xpath('//td[@style="padding:0 0 0 20"]//table[@width="100%"]//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 6개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '') \
                .replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').rstrip().lstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['type'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            strtemp = strtemp.replace('[', '').replace(']', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['father'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['father'] = strtemp

        store_info['addr'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp[0] >= '0' and strtemp[0] <= '9':  # 우편번호 정보 제거
                idx = strtemp.find(' ')
                if idx != -1: strtemp = strtemp[idx + 1:].lstrip()

            store_info['addr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[5].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('('): strtemp = strtemp[1:].lstrip()
            idx = strtemp.find('(')
            if idx >=9: strtemp = strtemp[:idx].rstrip()
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')

        if store_info['name'].find('...') != -1:
            subapi_list = info_list[1].xpath('.//a/@href')
            if len(subapi_list) > 0:
                subapi = subapi_list[0]
                suburls = url + '/' + subapi
                print(suburls)

                try:
                    time.sleep(random.uniform(0.3, 0.9))
                    subresult = urllib.urlopen(suburls)
                except:
                    print('Error calling the subAPI');
                    store_list += [store_info];
                    continue

                subcode = subresult.getcode()
                if subcode != 200:
                    print('HTTP request error (status %d)' % code);
                    store_list += [store_info];
                    continue

                subresponse = subresult.read()
                # print(subresponse)
                subtree = html.fromstring(subresponse)

                subinfo_list = subtree.xpath('//div[@align="center"]//table[@cellspacing="1"]//tr')

                for j in range(len(subinfo_list)):
                    item_list = subinfo_list[j].xpath('.//td')
                    if len(item_list) < 2: continue  # 최소 2개 필드 있어야 함

                    str_key = "".join(item_list[0].itertext())
                    str_value = "".join(item_list[1].itertext())

                    if str_key != None and str_value != None:
                        str_key = str_key.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                        str_value = str_value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

                        if str_key == '교회명':
                            store_info['name'] = str_value.replace(' ', '/')
                        elif str_key == '교단':
                            store_info['type'] = str_value

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
