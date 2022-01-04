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
import ast
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

    outfile = codecs.open('insurance_chubblife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@처브라이프생명\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 9: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.chubblife.co.kr'
    api = '/front/introduction/officeGuide/list.do'
    data = {
        'seqNum': '',
        'searchCondition': '',
        'searchKeyword': '',
    }
    data['pageNo'] = intPageNo
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

    tree = html.fromstring(response)
    entity_list = tree.xpath('//table[@class="defaultTable"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '처브라이프생명'

        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
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



        # 더이상 좌표정보 제공하지 않음 - 2021.02.09


        # store_info['id'] = '';      store_info['xcoord'] = '';      store_info['ycoord'] = ''
        # temp_list = info_list[4].xpath('.//a/@href')
        # if len(temp_list) > 0:
        #     strtemp = temp_list[0]
        #     idx = strtemp.find('goPopup(')
        #     if idx != -1:
        #         strtemp = strtemp[idx+8:]
        #         idx = strtemp.find(');')
        #         store_info['id'] = strtemp[:idx][1:-1]
        #
        # if store_info['id'] != '':
        #     suburls = 'https://www.chubblife.co.kr/front/introduction/officeGuide/viewAjax.do'
        #     subparams = 'seqNum=' + store_info['id']
        #     print(suburls)
        #
        #     try:
        #         time.sleep(random.uniform(0.3, 0.9))
        #         subreq = urllib2.Request(suburls, subparams)
        #         subreq.get_method = lambda: 'POST'
        #         subresult = urllib2.urlopen(subreq)
        #     except:
        #         print('Error calling the subAPI');
        #         store_list += [store_info];                continue
        #
        #     code = subresult.getcode()
        #     if code != 200:
        #         print('HTTP request error (status %d)' % code);
        #         store_list += [store_info];                continue
        #
        #     subresponse = subresult.read()
        #     #print(subresponse)
        #
        #     # 결과값의 포맷에 오류가 있어 아래와 같이 필요한 부분만 잘라내 사용함함
        #
        #     idx = subresponse.rfind('"mapCrdeY"')
        #     if idx == -1:
        #         store_list += [store_info];                continue
        #
        #     subresponse = '{' + subresponse[idx:]
        #     #response_json = json.load(subresponse)
        #     response_dict = ast.literal_eval(subresponse)
        #
        #     store_info['xcoord'] = response_dict['mapCrdeY']
        #     store_info['ycoord'] = response_dict['mapCrdeX']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
