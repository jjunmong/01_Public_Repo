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

    outfile = codecs.open('hanwhastock_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ORGNAME|ID|TELNUM|ADDR|NEWADDR|ETCADDR|XCOORD|YCOORD@@한화투자증권\n")

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
            outfile.write(u'%s|' % store['etcaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 49: break
        elif len(store_list) < 4: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.hanwhawm.com'
    api = '/main/hanwha/hws/CP130_1pc.cmd'
    data = {
        'basicRows': '4',
        'VC_GROUPCODE': '',
        'h_scno': 'H0006',
        'h_scid': '',
    }
    data['nowPage'] = intPageNo
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
    temp_list = tree.xpath('//a/@href')

    store_list = []
    for i in range(len(temp_list)):
        strtemp = temp_list[i]
        if strtemp == None: continue

        idx = strtemp.find('branchMap(\'')
        if idx == -1: continue

        strtemp = strtemp[idx+11:]
        idx = strtemp.find('\'')
        store_id  = strtemp[:idx]

        subdata = {
            'h_scno': 'H0006',
            'h_scid': '',
        }
        subdata['NN_CLUB_ID'] = store_id
        subparams = urllib.urlencode(subdata)
        print(subparams)

        try:
            time.sleep(random.uniform(0.3, 0.9))
            suburl = 'https://www.hanwhawm.com/main/hanwha/hws/CP130_1pe.cmd'
            subreq = urllib2.Request(suburl, subparams)
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the subAPI');      continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);     continue

        subresponse = subresult.read()
        #print(subresponse)

        response_json = json.loads(subresponse)
        entity_list = response_json['result']['block1']

        for j in range(len(entity_list)):
            store_info = {}

            store_info['name'] = '한화투자증권'
            store_info['id'] = entity_list[j]['NN_CLUB_ID']
            store_info['subname'] = ''
            store_info['orgname'] = ''
            strtemp = entity_list[j]['VC_BRANCH_NAME']
            if strtemp != None:
                strtemp = strtemp.lstrip().rstrip()
                store_info['orgname'] = strtemp
                store_info['subname'] = strtemp.replace(' ', '/')

            store_info['addr'] = entity_list[j]['VC_ADDR1'] + ' ' + entity_list[j]['VC_ADDR2'] + ' ' + entity_list[j]['VC_ADDR3'] + ' ' + entity_list[j]['VC_ADDR4']
            store_info['newaddr'] = entity_list[j]['VC_ADDR1_NEW'] + ' ' + entity_list[j]['VC_ADDR2_NEW'] + entity_list[j]['VC_ADDR3_NEW'] + ' ' + entity_list[j]['VC_ADDR4_NEW']
            store_info['etcaddr'] = entity_list[j]['VC_ADDR4']
            store_info['pn'] = entity_list[j]['CC_BRANCH_TEL'].lstrip().rstrip().replace(')', '-')
            store_info['xcoord'] = entity_list[j]['VC_LNG']
            store_info['ycoord'] = entity_list[j]['VC_LAT']

            store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
