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
    '경기': '01',
}

sido_list = {
    '서울': '01',
    '광주': '04',
    '대구': '06',
    '대전': '05',
    '부산': '03',
    '울산': '07',
    '인천': '02',
    '경기': '08',
    '강원': '09',
    '경남': '15',
    '경북': '14',
    '전남': '12',
    '전북': '13',
    '충남': '10',
    '충북': '11',
    '제주': '16',
    '세종': '17'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('insurance_hanwhalife_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@한화생명\n")

    for sido_name in sorted(sido_list2):    # 광역시도 이름 아무것이나 하나 지정하고 page 증가하면서 호출하면 전국 점포정보 다 얻을 수 있음

        page = 1
        sentinel_store_id = '999999'
        while True:
            store_list = getStores(sido_name, sido_list[sido_name], page)
            page += 1

            if store_list == None: break;
            elif len(store_list) > 0:
                if store_list[0]['id'] ==  sentinel_store_id: break
                else: sentinel_store_id = store_list[0]['id']

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                #outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            if page == 999: break
            elif len(store_list) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

# v2.0 (2017/11)
def getStores(sido_name, sido_code, intPageNo):
    url = 'https://www.hanwhalife.com'
    api = '/main/customerCenter/branch/getList.do'
    data = {
        'seq' : '',
        'FN_STR_001': '5',
        'addr': '',
        'check1Val': '',
        'check2Val': '',
        'check3Val': '',
        'check4Val': '',
        'check5Val': '',
        'srch_gubun': '1',
        'keyword': '',
        'check1': '',
        'check2': '',
        'check3': '',
        'check4': '',
        'check5': '',
        '__MENU_ID': 'MCU_BS00001',
        #'_r_': '',
        '_r_': 0.8434321346057192,
    }
    data['currentPage'] = intPageNo
    data['FN_STR_002'] = 'sido_name'
    data['addr1'] = 'sido_name'
    params = urllib.urlencode(data)
    print(params)
    params = 'currentPage=' + str(intPageNo) + '&seq=&FN_STR_001=5&FN_STR_002=%EA%B2%BD%EA%B8%B0&addr=&addr1=%EA%B2%BD%EA%B8%B0&check1Val=&check2Val=&check3Val=&check4Val=&check5Val=&srch_gubun=1&keyword=&check1=1&check2=1&check3=1&check4=1&check5=1&__MENU_ID=MCU_BS00001&_r_=0.8434321346057192'

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        #'Cookie': 'JSESSIONID=c58fc11b2d0744eda92bf39dc879be6742289270eaa84db15c65!-1154825719',
        'Connection': 'keep-alive',
    }

    try:
        req = urllib2.Request(url + api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #response = unicode(response, 'euc-kr')
    #print(response)
    response_json = json.loads(response)  # json 포맷으로 결과값 반환
    entity_list = response_json['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '한화생명'
        store_info['subname'] = ''
        strtemp = entity_list[i]['jpname'].lstrip().rstrip()
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        if entity_list[i].get('addrStr'): store_info['newaddr'] = entity_list[i]['addrStr']
        store_info['pn'] = ''
        if entity_list[i].get('telStr'): store_info['pn'] = entity_list[i]['telStr']
        store_info['id'] = ''
        if entity_list[i].get('jpcode'): store_info['id'] = entity_list[i]['jpcode']

        store_info['type'] = ''
        if entity_list[i].get('grocdn'):
            strtemp = entity_list[i]['grocdn']
            if strtemp == 'E1':
                store_info['type'] = '지점'
            elif strtemp == '04':
                store_info['type'] = '검진센터'
            elif strtemp == 'E4':
                store_info['type'] = '융자창구'
            elif strtemp == 'C1':
                store_info['type'] = '지원단'
            elif strtemp == 'A4':
                store_info['type'] = '대리점'
            else: store_info['type'] = strtemp

        store_info['xcoord'] = ''
        if entity_list[i].get('G_xPoint'): store_info['xcoord'] = entity_list[i]['G_xPoint']
        store_info['ycoord'] = ''
        if entity_list[i].get('G_yPoint'): store_info['ycoord'] = entity_list[i]['G_yPoint']

        store_list += [store_info]

    return store_list

"""
# v1.0
def getStores(sido_name, sido_code, intPageNo):
    url = 'http://www.hanwhalife.com'
    api = '/callcenter/gis/hanwhalife_search_list.asp'
    data = {
    }
    strtemp = sido_name.encode('euc-kr')
    params = 'search_chk1_checked=5,3,2,4,1,6&sido=' + urllib.quote(strtemp) + '&sigungu=&page_num=' + str(intPageNo) +'&tbl_nm=&search_cond=1&search_txt=%B0%CB%BB%F6%BE%EE%B8%A6%20%C0%D4%B7%C2%C7%CF%BC%BC%BF%E4.&search_chk2=1'

    params = 'page=' + str(intPageNo) + '&upmu=&sido=&sigungu=&search_sido_txt=' + urllib.quote(strtemp) + '&search_sigungu_txt=sigungu_x=&sigungu_y=&search_type=left&branch_code=&show_gb=&top_search_type=&top_search_text=&search_branch_nm='
    params += '&search_sido=' + sido_code + '&search_sigungu=&search_subway='
    #params = 'page=1&upmu=&sido=&sigungu=&search_sido_txt=%BC%AD%BF%EF&search_sigungu_txt=%BC%AD%C3%CA%B1%B8&sigungu_x=127032651&sigungu_y=37483552&search_type=left&branch_code=&show_gb=&top_search_type=&top_search_text=&search_branch_nm=&search_sido=01&search_sigungu=%BC%AD%C3%CA%B1%B8%7C127032651%7C37483552&search_subway='

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
        #req = urllib2.Request(url + api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
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

    entity_list = tree.xpath('//div[@class="list_box"]//table//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 6: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '한화생명'

        store_info['subname'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['type'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_info['id'] = ''
        temp_list = info_list[5].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('BranchInfo(')
            if idx != -1:
                strtemp = strtemp[idx+11:].lstrip()
                idx = strtemp.find(')')
                store_info['id'] = strtemp[:idx].rstrip()[1:-1]

        store_info['ot'] = '';  store_info['xcoord'] = '';  store_info['ycoord'] = ''
        if store_info['id'] != '':
            try:
                suburls = 'http://www.hanwhalife.com/callcenter/gis/hanwhalife_content.asp'
                subparams = params.replace('branch_code=', 'branch_code='+store_info['id'])
                print (subparams)

                time.sleep(random.uniform(0.3, 0.9))
                # req = urllib2.Request(url + api, params, headers=hdr)
                subreq = urllib2.Request(suburls, subparams)
                subreq.get_method = lambda: 'POST'
                subresult = urllib2.urlopen(subreq)
            except:
                print('Error calling the sub-API');
                store_list += [store_info];     continue

            code = subresult.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code);
                store_list += [store_info];     continue

            subresponse = subresult.read()
            subresponse = unicode(subresponse, 'euc-kr')
            # print(response)
            subtree = html.fromstring(subresponse)

            idx = subresponse.find('mapX =')
            if idx != -1:
                strtemp = subresponse[idx+6:].lstrip()
                idx = strtemp.find(';')
                strtemp = strtemp[:idx].rstrip()[1:-1]
                store_info['xcoord'] = strtemp[:3] + '.' + strtemp[3:]

            idx = subresponse.find('mapY =')
            if idx != -1:
                strtemp = subresponse[idx+6:].lstrip()
                idx = strtemp.find(';')
                strtemp = strtemp[:idx].rstrip()[1:-1]
                store_info['ycoord'] = strtemp[:2] + '.' + strtemp[2:]

            subinfo_list = subtree.xpath('//div[@class="detail_wrap"]//table//tr//td[@class="detail_tx"]')

            if len(subinfo_list) < 2:      # 최소 필드 수 체크
                store_list += [store_info];     continue

            strtemp = "".join(subinfo_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['ot'] = strtemp

            strtemp = "".join(subinfo_list[1].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('null', '').rstrip().lstrip()
                store_info['newaddr'] = strtemp

            if len(subinfo_list) >= 3:
                strtemp = "".join(subinfo_list[2].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_list += [store_info]

    return store_list
"""

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
