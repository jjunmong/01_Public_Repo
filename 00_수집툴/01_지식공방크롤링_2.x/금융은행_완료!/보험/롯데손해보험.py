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

    outfile = codecs.open('insurance_lotte_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|TELNUM|ADDR|NEWADDR|OT|XCOORD|YCOORD@@롯데손해보험\n")

    for sido_name in sorted(sido_list):
        # 보험상담/가입 (본사, 금융센터, 지점 크롤링됨)
        store_list = getStores(sido_name, 'TYPE2')
        if store_list != None:
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['type'])
                #outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 0.9))

        # 보상지원단
        store_list = getStores(sido_name, 'TYPE8')
        if store_list != None:
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['type'])
                #outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStores(sido_name, job_type):
    url = 'http://www.lotteins.co.kr'
    api = '/CChannelSvl'
    data = {
        'rtnUri': '/web/C/D/I/resultSearchList.jsp',
        'tc': 'dfi.c.d.i.cmd.Cdi051Cmd',
        'title': '',
        'cityval': '',
        'jobval2': 'TYPE2',
        'injob': 'TYPE1',
        'task': 'searchListOfLoctoJob',
    }
    data['jobval2'] = job_type
    data['cityval2'] = sido_name.encode('euc-kr')
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
        time.sleep(random.uniform(0.3, 0.9))
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

    idx = response.find('.innerHTML =')
    if idx == -1: return None

    response = response[idx+12:].lstrip()
    idx = response.find('</table>"')
    response = response[:idx+8]
    #print(response)

    tree = html.fromstring(response)
    entity_list = tree.xpath('//table//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 3: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '롯데손해보험'

        store_info['type'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('㈜', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['subname'] = ''
        subname = "".join(info_list[1].itertext())
        strtemp = subname
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('㈜', '').rstrip().lstrip()
            if store_info['type'] == '본사': strtemp = '본사'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = '';     store_info['addr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = '';  store_info['ot'] = ''
        store_info['id'] = '';  store_info['xcoord'] = '';  store_info['ycoord'] = ''

        subdata = {
            'rtnUri': '/web/C/D/I/resultSearch.jsp',
            'tc': 'dfi.c.d.i.cmd.Cdi051Cmd',
            'cityval': '',
            'injob': 'TYPE1',
            'task': 'detailSearch',
        }
        subdata['title'] = subname.encode('euc-kr')
        subdata['jobval2'] = job_type
        subdata['cityval2'] = sido_name.encode('euc-kr')
        subparams = urllib.urlencode(subdata)
        print(subparams)

        try:
            subreq = urllib2.Request(url + api, subparams, headers=hdr)
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];     continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];     continue

        subresponse = subresult.read()
        subresponse = unicode(subresponse, 'euc-kr')
        #print(subresponse)

        idx = subresponse.find('w11").innerHTML =')
        if idx != -1:
            strtemp = subresponse[idx+17:].lstrip()
            idx = strtemp.find(';')
            strtemp = strtemp[:idx].rstrip()
            store_info['newaddr'] = strtemp[1:-1]

        idx = subresponse.find('d11").innerHTML =')
        if idx != -1:
            strtemp = subresponse[idx+17:].lstrip()
            idx = strtemp.find(';')
            strtemp = strtemp[:idx].rstrip()
            store_info['addr'] = strtemp[1:-1]

        idx = subresponse.find('t1").innerHTML =')
        if idx != -1:
            strtemp = subresponse[idx+16:].lstrip()
            idx = strtemp.find(';')
            strtemp = strtemp[:idx].rstrip()
            store_info['pn'] = strtemp[1:-1].replace(' ', '').replace(')', '-').replace('.', '-')

        idx = subresponse.find('o1").innerHTML =')
        if idx != -1:
            strtemp = subresponse[idx+16:].lstrip()
            idx = strtemp.find(';')
            strtemp = strtemp[:idx].rstrip()
            store_info['ot'] = strtemp[1:-1]

        idx = subresponse.find('detailmap(')
        if idx != -1:
            strtemp = subresponse[idx+10:].lstrip()
            idx = strtemp.find(';')
            temp_list = strtemp[:idx].rstrip().split(',')
            if len(temp_list) >= 2:
                store_info['xcoord'] = temp_list[1].lstrip().rstrip()[1:-1]
                store_info['ycoord'] = temp_list[0].lstrip().rstrip()[1:-1]

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
