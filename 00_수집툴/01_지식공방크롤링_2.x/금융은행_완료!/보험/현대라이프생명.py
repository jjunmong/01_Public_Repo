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
    '서울': '서울',
}

sido_list = {
    '서울': '서울',
    '경기': '경기',
    '강원': '강원',
    '경상': '경상',
    '전라': '전라',
    '충청': '충청',
    '제주': '제주',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('insurance_hyundailife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@현대라이프생명\n")

    for sido_name in sorted(sido_list):
        # 제지급업무 지점
        store_list = getStores(sido_name, 'PAYMENT')
        if store_list != None:
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 0.9))

        # 대출상담 지점
        store_list = getStores(sido_name, 'LOAN')
        if store_list != None:
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 0.9))

        # 거점업무 지점
        store_list = getStores(sido_name, 'INSU')
        if store_list != None:
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(sido_name, store_type):
    url = 'http://www.fubonhyundai.com'
    api = '/process/Hhpcs031.do'
    data = {
        '_biz_op_code': '_BQ',   # _BQ or _Q
        '_biz_dw_00': '',
        '_biz_dw_00_flag': 'biz_flag',
        'SEND_BRA_AREA': '',    # euc-kr로 광역시도명 지정해야 함
        'SEND_BRA_DIV': '',
        'CONSULT': 'INSU',      # LOAN 대출상담 PAYMENT 제지급 INSU 거점업무
    }
    data['CONSULT'] = store_type
    data['SEND_BRA_AREA']= sido_name.encode('euc-kr')

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
        req = urllib2.Request(url+api, params, headers=hdr)
        req.get_method = lambda: 'POST'
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
    entity_list = tree.xpath('//div[@class="tbs02 mt10"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '현대라이프생명'
        store_info['type'] = store_type

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('㈜', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = '';  store_info['xcoord'] = '';  store_info['ycoord'] = ''
        temp_list = info_list[3].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('setMapDtl(')
            if idx != -1:
                strtemp = strtemp[idx+10:]
                idx = strtemp.find(')')
                extrainfo_list = strtemp[:idx].split(',')
                if len(extrainfo_list) >= 4:
                    store_info['id'] = extrainfo_list[3].lstrip().rstrip()[1:-1]
                    store_info['xcoord'] = extrainfo_list[2].lstrip().rstrip()[1:-1]
                    store_info['ycoord'] = extrainfo_list[1].lstrip().rstrip()[1:-1]

        # info_list[4]에서 영업시간, 주차 관련 정보도 얻을 수 있음 (필요할 때 추출할 것!)

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
