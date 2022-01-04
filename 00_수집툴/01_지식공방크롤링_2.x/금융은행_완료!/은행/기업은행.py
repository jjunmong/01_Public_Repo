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
    '부산': '051',
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

    outfile = codecs.open('ibkbank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDRSUB|NEWADDR@@IBK기업은행\n")

    for sido_name in sorted(sido_list):

        page = 1
        sentinel_pn = '999-999-9999'
        while True:
            store_list = getStores(sido_name, page)
            if store_list == None: break;

            count =0;   exit_flag=0
            for store in store_list:
                if count == 0:
                    if store['pn'] == sentinel_pn:  # 마지막 페이지 이후에도 계속 같은 내용을 반환해서... (지점이름으로 비교할까???)
                        exit_flag = 1;  break
                    else: sentinel_pn = store['pn']

                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['newaddr'])
                count += 1

            page += 1

            if exit_flag == 1: break
            elif page == 99: break
            elif len(store_list) < 8: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

def getStores(sido_name, intPageNo):
    url = 'http://kiupbank.tritops.co.kr'
    api = '/list.jsp'

    data = {
        'seq_no': '',
        'search_type': 2,
        'menu': 1,
        's_menu': 1,
        'sigungu': '',
        'poi_pg': 1,
        'poi_nm': '',
        'poi_x': '',
        'poi_y': '',
        'prev_url': '/main.jsp',
        'search_cond': 1,
        'search_txt': '',
    }
    data['pg'] = intPageNo
    data['sido'] = sido_name
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
        urls = url + api
        req = urllib2.Request(urls, params, headers=hdr)
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

    entity_list = tree.xpath('//div[@class="tblist"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = 'IBK기업은행'
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.endswith('(출)'): strtemp = strtemp[:-3].rstrip() + '출장소'
            elif strtemp.endswith('(출장소)'): strtemp = strtemp[:-5].rstrip() + '출장소'
            elif strtemp.endswith('출장소'): pass
            elif strtemp.endswith('센터'): pass
            elif strtemp.endswith('본점'): pass
            elif not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = '';     store_info['addr'] = ''
        strtemp = "".join(info_list[2].itertext())
        strtemp2 = info_list[2].text
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp2 != None:
                strtemp2 = strtemp2.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['newaddr'] = strtemp2
                idx = strtemp.find(strtemp2)
                if idx != -1:
                    strtemp = strtemp[len(strtemp2):].lstrip()
                    store_info['addr'] = strtemp
            else:
                idx = strtemp.rfind(sido_name)
                if idx > 0:
                    store_info['newaddr'] = strtemp[:idx].rstrip()
                    store_info['addr'] = strtemp[idx:]
                else: store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['id'] = ''
        temp_list = info_list[0].xpath('.//input/@value')
        if len(temp_list) > 0:
            store_info['id'] = temp_list[0]

        #if store_info['id'] != '' and (store_info['newaddr'].find('...') != -1 or store_info['addr'].find('...') != -1):
        if store_info['id'] != '':
            subdata = {
                'seq_no': '',
                'search_type': 2,
                'menu': 1,
                's_menu': 1,
                'sigungu': '',
                'poi_pg': 1,
                'poi_nm': '',
                'poi_x': '',
                'poi_y': '',
                'prev_url': '/list.jsp',
                'search_cond': 1,
                'search_txt': '',
            }
            subdata['seq_no'] = store_info['id']
            subdata['pg'] = intPageNo
            subdata['sido'] = sido_name
            subparams = urllib.urlencode(subdata)
            print(subparams)

            try:
                time.sleep(random.uniform(0.3, 0.9))
                suburls = 'http://kiupbank.tritops.co.kr/content.jsp'
                subreq = urllib2.Request(suburls, subparams, headers=hdr)
                subreq.get_method = lambda: 'POST'
                subresult = urllib2.urlopen(subreq)
            except:
                print('Error calling the API');
                store_list += [store_info];     continue

            code = result.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code);
                store_list += [store_info];     continue

            subresponse = subresult.read()
            # print(subresponse)
            subtree = html.fromstring(subresponse)

            subinfo_list = subtree.xpath('//table[@class="detail_tb"]//tr')
            for j in range(len(subinfo_list)):
                tag_list = subinfo_list[j].xpath('.//th')
                value_list = subinfo_list[j].xpath('.//td')

                if len(tag_list) < 1 or len(value_list) < 1: continue

                tag = "".join(tag_list[0].itertext())
                value = "".join(value_list[0].itertext())

                if tag == None or value == None: continue

                tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

                if tag == '도로명 주소' and value != '':
                    store_info['newaddr'] = value
                elif tag == '지번 주소' and value != '':
                    store_info['addr'] = value

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
