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
    '부산': '02',
}

sido_list = {
    '서울': '01',
    '부산': '02',
    '광주': '03',
    '대구': '04',
    '대전': '05',
    '울산': '06',
    '인천': '07',
    '경기': '08',
    '강원': '09',
    '경남': '10',
    '경북': '11',
    '전남': '12',
    '전북': '13',
    '충남': '14',
    '충북': '15',
    '제주': '16',
    '세종': '17'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('kyobolife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@교보생명\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            store_list = getStores(sido_list[sido_name], page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s\n' % store['newaddr'])

            page += 1

            if page == 2: break     # 광역시도마다 한번 호출로 광역시도 내 모든 지점 정보를 얻을 수 있음
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_code, intPageNo):
    url = 'https://www.kyobo.co.kr'
    #api = '/co/et/et/SCOETNLP012R02.ajax'
    api = '/cs/et/et/SCSETNLP009R01.ajax'

    data = {
        'devon.token.field': 'token',
        'token': 'CVB22Q20YQI5Q1UFPUEJHLEF133OKGQZ',
        'gungu': '',
        'tempSearchtype': '',
        'tempSubway1': '',
        'tempSubway2': '',
        'tempSearchtype2': '',
        'chkListValue:': '00',
        'orgCd': '',
        'devonRowSize': '5',
        'siDoCd': '',
        'siGuGunCd': '',
        'mapCdnX': '',
        'mapCdnY': '',
        'searchYn': 'N',
        'searchNm:': '',
        'task_sel:': '00',
        'search_type': '0',
        'step': 'stepTwo',
        'subway1': '',
        'selectedGroup': 'CS_SUW_LINE_',
        'subway2': '',
        'search_type_2:': '',
    }
    data['startCode'] = sido_code
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    #params = 'devon.token.field=token&token=CVB22Q20YQI5Q1UFPUEJHLEF133OKGQZ&startCode=&gungu=&tempSearchtype=&tempSubway1=&tempSubway2=&tempSearchtype2=&chkListValue=00&orgCd=&devonRowSize=5&siDoCd=&siGuGunCd=&mapCdnX=&mapCdnY=&searchYn=Y&searchNm=%EC%84%9C%EC%9A%B8&task_sel=00&search_type=0&step=stepTwo&startCode=01&gungu=134&subway1=&selectedGroup=CS_SUW_LINE_&subway2=&search_type_2=%EC%A7%80%ED%95%98%EC%B2%A0%EC%97%AD%EB%AA%85%EC%9D%84+%EC%9E%85%EB%A0%A5%ED%95%B4+%EC%A3%BC%EC%84%B8%EC%9A%94.'

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        #'Cookie': 'WMONID=5dB88Ezjber; PCID=14892376615322342935636; RC_RESOLUTION=2560*1440; RC_COLOR=24; strIconSet_SCOCONLM001_array=sr_0%2Csr_1%2Csr_2%2Csr_3%2Csr_4%2Csr_5%2Csr_6%2Csr_7%2Csr_8; JSESSIONID=0001VOQ-U1PoUB0JRAOwRmeKEdl:1796q62te; voiceStartX=stop; voiceStart=stop; voiceSpeed=3; voiceVolum=3',
        #'Upgrade-Insecure-Requests': '1',
    }

    try:
        urls = url + api
        req = urllib2.Request(urls, params)
        #req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['list']['rows']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '교보생명'
        store_info['subname'] = ''
        strtemp = entity_list[i]['orgNm']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').decode('utf-8')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] =''
        strtemp = convert_full_to_half_string(entity_list[i]['addr'])
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            # xxx 번지 yy 호 패턴 처리 'xxx-yy'로 변환
            idx = strtemp.find(' 번지 ')
            if idx != -1 and idx+8 <= len(strtemp):     # 최소한의 주소문자열 길이도 체크
                strtemp2 = strtemp[idx+4:].lstrip()
                if strtemp2[:1] >= '0' and strtemp2[:1] <= '9':
                    idx2 = strtemp2.find(' ')
                    if idx2 != -1:
                        strtemp3 = strtemp2[idx2+1:].lstrip()
                        if strtemp3.startswith('호 ') or strtemp3.startswith('호,'):
                            strtemp = strtemp[:idx].rstrip() + '-' + strtemp2[:idx2] + ' ' + strtemp3[2:].lstrip()

            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = entity_list[i]['homeTelNo1'] + '-' + entity_list[i]['homeTelNo2'] + '-' + entity_list[i]['homeTelNo3']
        if strtemp.startswith('-'): strtemp = strtemp[1:]
        store_info['pn'] = strtemp

        store_info['xcoord'] = entity_list[i]['mapCdnX']
        store_info['ycoord'] = entity_list[i]['mapCdnY']

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
