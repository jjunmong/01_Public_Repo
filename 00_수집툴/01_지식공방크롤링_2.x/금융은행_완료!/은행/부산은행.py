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

    outfile = codecs.open('busanbank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|CODE|XCOORD|YCOORD\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            for store in store_list:
                strtemp = store['newaddr']
                if strtemp == '': strtemp = store['addr']

                if strtemp != '' and not strtemp.startswith(sido_name): continue

                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['code'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 2: break     # 한 페이지에서 광역시도내 지점정보 모두 반환
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'https://www.busanbank.co.kr'
    api = '/ib20/act/BHPBKI445INQA1AM?ib20_cur_mnu=BHPBKI445001001&ib20_cur_wgt=BHPBKI445INQV1AM'

    data2 = {
        'action_type': 'act',
        'ib20_action': '/ib20/act/BHPBKI445INQA1AM',
        'ib20_cur_mnu': 'BHPBKI445001001',
        'ib20_cur_wgt': 'BHPBKI445INQV1AM',
        'ib20_change_wgt': '',
        'REQUEST_TOKEN_KEY': '3a594be5690962dde4890a35bce807a2',
        'action_type': 'act',
        'ib20_action': '/ib20/act/BHPBKI445INQA1AM',
        'ib20_cur_mnu': 'BHPBKI445001001',
        'ib20_cur_wgt': 'BHPBKI445INQV1AM',
        'INQ_CND': 1,
        'CUR_PAGE_NUM': 1,
        'ibs_current_page': 1,
        'SEL_TXT': 'selTxt1',
        'RDNM_DVCD:': 'undefined',
        'b_page_id': '',
    }
    data = {}
    data['INQ_CNTN'] = sido_name
    sub_params = urllib.urlencode(data)

    params2 = 'action_type=act&ib20_action=%2Fib20%2Fact%2FBHPBKI445INQA1AM&ib20_cur_mnu=BHPBKI445001001&ib20_cur_wgt=BHPBKI445INQV1AM&ib20_change_wgt=&REQUEST_TOKEN_KEY=3a594be5690962dde4890a35bce807a2&action_type=act&ib20_action=%2Fib20%2Fact%2FBHPBKI445INQA1AM&ib20_cur_mnu=BHPBKI445001001&ib20_cur_wgt=BHPBKI445INQV1AM&INQ_CND=1&CUR_PAGE_NUM=1&ibs_current_page=1'
    params2 += '&' + sub_params
    params2 += '&SEL_TXT=selTxt1&RDNM_DVCD=undefined&b_page_id='
    print(params2)

    #params = 'action_type=act&ib20_action=%2Fib20%2Fact%2FBHPBKI445INQA1AM&ib20_cur_mnu=BHPBKI445001001&ib20_cur_wgt=BHPBKI445INQV1AM&ib20_change_wgt=&REQUEST_TOKEN_KEY=3a594be5690962dde4890a35bce807a2&action_type=act&ib20_action=%2Fib20%2Fact%2FBHPBKI445INQA1AM&ib20_cur_mnu=BHPBKI445001001&ib20_cur_wgt=BHPBKI445INQV1AM&INQ_CND=1&CUR_PAGE_NUM=1&ibs_current_page=1'
    #params += '&INQ_CNTN=%EB%B6%80%EC%82%B0'
    #params += '&SEL_TXT=selTxt1&RDNM_DVCD=undefined&b_page_id='
    #print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        #'Cookie': 'WMONID=PsnebEu1acI; PCID=14908061670479879932543; BSIB_MAIN_FAST_MENU_RESET=Y; IB20SESSID=BHP0901||JyXttQYQUyeq53munksFORrPcWZDUSsNUP2Rxzd1tqqlkajbgrfvfXkyccf56sFB.UE5JQldTL3BpYmJocDkx; JSESSIONID=JyXttQYQUyeq53munksFORrPcWZDUSsNUP2Rxzd1tqqlkajbgrfvfXkyccf56sFB.UE5JQldTL3BpYmJocDkx; BSIB_BHP_HISTORY_MENU=BHPBKI445001001%3A%uC601%uC5C5%uC810%uC548%uB0B4%3ABHP%3BBHPBKI381001001%3A%uC740%uD589%uC18C%uAC1C%3ABHP',
        #'Referer': 'https://www.busanbank.co.kr/ib20/mnu/BHPBKI445000001',
    }

    try:
        urls = url + api
        req = urllib2.Request(urls, params2, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response = urllib.unquote(urllib.unquote(response))
    print(response)
    idx = response.find('[{')
    if idx == -1: return None
    response = response[idx:]
    idx = response.find('}]')
    if idx == -1: return None
    response = response[:idx+2]
    response = '{ "list": ' + response + '}'
    response_json = json.loads(response)
    entity_list = response_json['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '부산은행'
        store_info['subname'] = ''
        strtemp = entity_list[i]['HMPG_SLS_BRNM']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').decode('utf-8')
            if strtemp.endswith('(출)'): strtemp = strtemp[:-3].rstrip() + '출장소'
            elif strtemp.endswith('출장소'): pass
            elif strtemp.endswith('센터'): pass
            elif strtemp.endswith('본점'): pass
            elif not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['SLBR_RDNM_ADDR'].replace('+', ' ') + ' ' + entity_list[i]['SLBR_RDNM_DTL_ADDR'].replace('+', ' ')
        store_info['newaddr'] = store_info['newaddr'].lstrip().rstrip()
        store_info['addr'] = entity_list[i]['SLBR_PSNOAD'].replace('+', ' ') + ' ' + entity_list[i]['SLBR_DTL_ADDR'].replace('+', ' ')
        store_info['addr'] = store_info['addr'].lstrip().rstrip()
        store_info['code'] = entity_list[i]['SLBR_CD']

        store_info['pn'] = ''
        strtemp = entity_list[i]['HMPG_SLBR_TLNO']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-')

        store_info['xcoord'] = entity_list[i]['GDNC_ADDR_Y_CORD_VAL']
        store_info['ycoord'] = entity_list[i]['GDNC_ADDR_X_CORD_VAL']

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
