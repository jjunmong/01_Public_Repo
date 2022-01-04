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

    outfile = codecs.open('shinhanbank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|ORGNAME|TELNUM|NEWADDR|FEAT@@신한은행\n")

    for sido_name in sido_list:

        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['orgname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['feat'])

            page += 1
            if page == 2: break     # 한번 호출로 광역시도내 전체 점포 정보 얻을 수 있음

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    urls = 'https://www.shinhan.com/comjsp/dataProcess.jsp?svr_type=TG&svr_code=THO0128'
    data = {"root_info": {"serviceType": "TG", "serviceCode": "THO0128", "nextServiceCode": "", "pkcs7Data": "",
                           "signCode": "", "signData": "", "useSign": "", "useCert": "", "permitMultiTransaction": "",
                           "keepTransactionSession": "", "skipErrorMsg": "", "mode": "", "language": "ko", "exe2e": "",
                           "hideProcess": "", "clearTarget": "data:json,{\"id\":\"dl_R_THO0128_1\",\"key\":\"SEARCH\"}",
                           "callBack": "shbObj.fncDoTHO0128callback", "exceptionCallback": "", "requestMessage": "",
                           "responseMessage": "", "serviceOption": "", "pcLog": "", "preInqForMulti": "", "makesum": "",
                           "removeIndex": "", "redirectUrl": "", "preInqKey": "", "_multi_transfer_": "",
                           "_multi_transfer_count_": "", "_multi_transfer_amt_": "", "userCallback": ""},
             "S_THO0128": {"BRA_ADDR1": "서울", "BRA_ADDR2": "%%", "BRA_ADDR3": "%%", "BRA_USE": "0", "page": 1,
                           "pageSize": 10, "pageCount": 5}}
    data['S_THO0128']['BRA_ADDR1'] = sido_name
    params = json.dumps(data)
    print(params)  # for debugging

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.888',
        'Accept': 'application/json',
        #'Accept-Encoding': 'gzip, deflate, br',    # 이렇게 지정하면 압축된 결과를 제공하므로 'Accept-Encoding' 값은 지정하지 않는다.
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset="UTF-8',
        #'Upgrade-Insecure-Requests': '1',
    }

    try:
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)
    response_json = json.loads(response)

    store_list = []
    entity_list = response_json['SEARCH']
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '신한은행'
        store_info['subname'] = ''
        strtemp = entity_list[i]['BRA_NAME'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        if strtemp == '본점': pass
        elif strtemp.endswith('금융센터'): pass
        elif strtemp.endswith('기업영업부'): pass
        elif strtemp.endswith('(출)'):
            strtemp = strtemp.replace('(출)', '출장소')
        elif not strtemp.endswith('지점'): strtemp += '지점'
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['BRA_BRAID']

        store_info['newaddr'] = ''
        if entity_list[i].get('BRA_ADDR1'): store_info['newaddr'] = entity_list[i]['BRA_ADDR1']
        if entity_list[i].get('BRA_ADDR2'): store_info['newaddr'] += ' ' + entity_list[i]['BRA_ADDR2']

        store_info['pn'] = ''
        if entity_list[i].get('BRA_TELNO'): store_info['pn'] = entity_list[i]['BRA_TELNO'].lstrip().rstrip().replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['feat'] = ''
        if entity_list[i].get('BRA_VIP'):
            if entity_list[i].get('BRA_VIP') == 'Y':
                store_info['feat'] = 'VIP'

        # 결과값에 기타 부가정보 많음 (필요할 때 추출해 사용할 것!!!)

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
