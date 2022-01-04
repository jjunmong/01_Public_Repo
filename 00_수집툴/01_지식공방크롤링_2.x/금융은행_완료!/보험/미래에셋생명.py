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

sido_list2 = {      # 테스트용 광역시도 목록
    '부산': '부산광역시',
}

sido_list = {
    '서울': '서울특별시',
    '광주': '광주광역시',
    '대구': '대구광역시',
    '대전': '대전광역시',
    '부산': '부산광역시',
    '울산': '울산광역시',
    '인천': '인천광역시',
    '경기': '경기도',
    '강원': '강원도',
    '경남': '경상남도',
    '경북': '경상북도',
    '전남': '전라남도',
    '전북': '전라북도',
    '충남': '충청남도',
    '충북': '충청북도',
    '제주': '제주특별자치도',
    '세종': '세종특별자치시'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('insurance_miraeassetlife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR@@미래에셋생명\n")

    page = 1
    sentinel_store_id = '999999'
    while True:
        store_list = getStores(page)
        page += 1

        if store_list == None: break;
        # elif len(store_list) > 0:
        #     if store_list[0]['id'] ==  sentinel_store_id: break
        #     elif store_list[0]['id'] != '': sentinel_store_id = store_list[0]['id']

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://life.miraeasset.com'
    api = '/html/customer/branch_search/branch_list.jsp'
    data = {
        'txtKeyField': 'work_gubun',
        'txtKeyWord': '',
        'txtKeyWord3': '',
        'txtKeyWord4': '',
        'kind': '',
    }
    data['page'] = intPageNo
    data['txtKeyWord2'] = ''    # 지명
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url + api, params)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
        result = urllib.urlopen(url+api+'?'+params)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = unicode(response, 'euc-kr')
    #print(response)
    tree = html.fromstring(response)
    entity_list = tree.xpath('//div[@id="branchList"]//tbody//tr')
    print(entity_list)
    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 10: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '미래에셋생명'

        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.find('행복센터') != -1: pass
            elif strtemp.startswith('본점'): pass
            elif not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = info_list[9].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('ocd=')
            if idx != -1:
                store_info['id'] = strtemp[idx+4:].lstrip()

        # info_list[4]~info_list[8]에 처리가능업무 정보도 있음 (필요하면 추출할 것)
        # 상세페이지에 x,y 좌표값 있음 (필요할 때 추출할 것!) 'http://life.miraeasset.com/html/customer/branch_search/imagemap.jsp?ocd=000012'

        store_list += [store_info]

    return store_list


def convert_full_to_half_char(ch):
    codeval = ord(ch)
    if 0xFF00 <= codeval <= 0xFF5E:
        ascii = codeval - 0xFF00 + 0x20;
        return unichr(ascii)
    else:
        return ch


def convert_full_to_half_string(line):
    output_list = [convert_full_to_half_char(x) for x in line]
    return ''.join(output_list)


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
