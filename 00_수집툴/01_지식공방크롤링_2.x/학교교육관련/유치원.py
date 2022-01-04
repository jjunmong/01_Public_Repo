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

    outfile = codecs.open('kindergarten_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@유치원\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 1499: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://e-childschoolinfo.moe.go.kr'
    api = '/kinderMt/combineFind.do'
    data = {
        'kinderSidoCode': '99',
        'kinderSggCode': '99',
        'kinderEstablishType': '99',
        'searchVal': '',
        'ittId': '',
        'tabNum': '3',
    }
    data['pageIndex'] = intPageNo
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
    entity_list = tree.xpath('//table[@class="horizon"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 7: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp == '기관명': continue
            store_info['name'] = strtemp
            #store_info['name'] = strtemp.replace(' ', '/')

        store_info['id'] = ''
        temp_list = info_list[2].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('fn_detail(')
            if idx != -1:
                strtemp = strtemp[idx+10:]
                idx = strtemp.find(');')
                subinfo_list = strtemp[:idx].split(',')
                if len(subinfo_list) >= 3:
                    store_info['id'] = subinfo_list[1].lstrip().rstrip()[1:-1]

        store_info['type'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = info_list[5].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('fn_panTo(')
            if idx != -1:
                strtemp = strtemp[idx+9:]
                idx = strtemp.find(');')
                subinfo_list = strtemp[:idx].split(',')
                if len(subinfo_list) >= 3:
                    store_info['xcoord'] = subinfo_list[2].lstrip().rstrip()
                    store_info['ycoord'] = subinfo_list[1].lstrip().rstrip()

        store_info['homepage'] = ''
        temp_list = info_list[6].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('validateURL(')
            if idx != -1:
                strtemp = strtemp[idx+12:]
                idx = strtemp.find(');')
                store_info['homepage'] = strtemp[:idx].lstrip().rstrip()[1:-1]

        store_info['pn'] = '';          store_info['ot'] = ''
        # 상세정보 페이지에서 전화번호 정보 얻을 수 있음
        if store_info['id'] != '':
            suburl = 'http://e-childschoolinfo.moe.go.kr/kinderMt/kinderSummary.do'
            subdata = {}
            subdata['ittId'] = store_info['id']
            subparams = urllib.urlencode(subdata)
            print(subparams)

            try:
                time.sleep(random.uniform(0.3, 0.9))
                subreq = urllib2.Request(suburl, subparams)
                subreq.get_method = lambda: 'POST'
                subresult = urllib2.urlopen(subreq)
            except:
                print('Error calling the subAPI')
                store_list += [store_info];     continue

            code = subresult.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code);
                store_list += [store_info];     continue

            subresponse = subresult.read()
            # print(subresponse)
            subtree = html.fromstring(subresponse)
            subinfo_list = subtree.xpath('//div[@class="content"]//tbody//tr')
            for j in range(len(subinfo_list)):
                tag_list = subinfo_list[j].xpath('.//th')
                value_list = subinfo_list[j].xpath('.//td')

                if len(tag_list) < 1 or len(value_list) < 1: continue

                tag = "".join(tag_list[0].itertext())
                value = "".join(value_list[0].itertext())

                if tag == None or value == None: continue

                tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

                if tag == '전화번호':
                    if value.startswith('('): value = value[1:].lstrip()    # '(031)311-2234' 이렇게 표기한 경우 있음
                    store_info['pn'] = value.replace(' ', '').replace('.', '-').replace(')', '-')
                elif tag == '운영시간': store_info['ot'] = value

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
