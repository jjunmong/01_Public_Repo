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
    '부산': '26',
}

sido_list = {       # 특이하게 pnucode값 앞자리를 사용
    '서울': '11',
    '광주': '29',
    '대구': '27',
    '대전': '30',
    '부산': '26',
    '울산': '31',
    '인천': '28',
    '경기': '41',
    '강원': '42',
    '경남': '48',
    '경북': '47',
    '전남': '46',
    '전북': '45',
    '충남': '44',
    '충북': '43',
    '제주': '50',
    '세종': '36'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('insurance_dongyanglife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|TELNUM|NEWADDR@@동양생명\n")

    for sido_name in sorted(sido_list):
        store_list = getStores(sido_list[sido_name])

        if store_list == None: continue

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s\n' % store['newaddr'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(sido_code):
    url = 'https://www.myangel.co.kr'
    api = '/process/WE_AC_WECRHF040000L'
    data = {
        '_biz_op_code': 'IQY_S2',
        'SGNG_COD': '',
        'OFC_GB': '',
    }
    data['SIDO_COD'] = sido_code    # 광역시도 코드
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
        req = urllib2.Request(url + api, params)
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
    entity_list = tree.xpath('//div[@id="mapList"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '동양생명'

        store_info['type'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['subname'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if store_info['type'] == '지점' or store_info['type'] == '다이렉트센터' or store_info['type'] == '하이브리드센터':
                if not strtemp.endswith('지점'): strtemp += '지점'
            elif store_info['type'] == '고객창구':
                if strtemp.find('센터') != -1: pass
                elif strtemp.find('고객') != -1: pass
                elif strtemp.find('창구') != -1: pass
                else: strtemp += '고객센터'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[5].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            idx = strtemp.find('(')
            if idx >= 5: strtemp = strtemp[:idx].rstrip()   # 포맷이 다음과 같은 경우 괄호안의 팩스번호 제거, 02-999-4532(02-900-7639)
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        # 'https://www.myangel.co.kr/customer/find/map_server2.jsp' url을 POST 방식으로
        # 'addr:서울특별시 강남구 테헤란로 329 삼흥빌딩 7층 (705-9번지)' 파라미터로 호출하면 x,y 좌표값은 추가로 얻을 수 있음 (필요할 때 추출할 것!)
        # 주소를 잘못 기재한 경우에는 좌표값 얻을 수 없음 (네이버 지도에 주소 문자열 그대로 전달하는 방식, 네이버의 지도코딩 결과로 x,y 좌표값을 얻는 방식)

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
