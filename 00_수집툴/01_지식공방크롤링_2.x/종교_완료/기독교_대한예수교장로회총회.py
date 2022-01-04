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
#import json
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

    outfile = codecs.open('church3_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|IDX|FATHER|WEBSITE|ORGNAME|SOURCE2@@교회\n")

    page = 1
    retry_count=0
    while True:
        #if page == 22: page += 1;   continue    # 사이트 오류로 22, 223, 260, 273, 278, 289페이지는 건너뛰어야 함 ㅠㅠ (2018/12)

        store_list = getStores(page)
        if store_list == 500:   # temporary for testing
            if page == 999: break
            retry_count = 0; page += 1; continue

        if store_list == None:
            if retry_count < 3: retry_count += 1;   continue
            else: break;
        elif len(store_list) == 0: break
        retry_count = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['idx'])
            outfile.write(u'%s|' % store['father'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s\n' % u'대한예수교장로회총회')

        page += 1

        if page == 999: break      # 2018년9월 기준 ???까지 있음
        elif len(store_list) < 1: break
        elif len(store_list) < 20:
            print('%d : %d' % (page-1, len(store_list)))

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.pck.or.kr'
    api = '/PckMypage/ChurchSearchResult.asp'
    data = {
        'flag': 'churchAddress',
        'searchWord': '',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code == 500:
        print('HTTP request error (status %d)' % code);
        return 500
    elif code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table[@width="600" and @cellpadding="3"]//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue

        store_info = {}

        store_info['idx'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['idx'] = strtemp

        store_info['name'] = ''
        store_info['subname'] = ''
        store_info['orgname'] = ''

        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['orgname'] = strtemp
            if not strtemp.endswith('교회'): strtemp += '교회'
            store_info['name'] = strtemp


        store_info['father'] = ''
        store_info['newaddr'] = ''
        store_info['pn'] = ''
        store_info['website'] = ''
        temp_list = info_list[2].xpath('.//a/@href')
        if len(temp_list) == 0: continue

        strtemp = temp_list[0]
        idx = strtemp.find('win_open(')
        if idx == -1: continue
        store_id = strtemp[idx+9:].replace(')', '').replace('\'', '').lstrip().rstrip()

        # 'http://www.pck.or.kr/PckMypage/ChurchInfo.asp?ChurchId=1958400173'
        suburl = 'http://www.pck.or.kr/PckMypage/ChurchInfo.asp?ChurchId=' + store_id

        try:
            #print(suburl)  # for debugging
            time.sleep(random.uniform(0.2, 0.4))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subtable_list = subtree.xpath('//table[@width="100%" and @height="30"]')

        if len(subtable_list) >= 2:
            subinfo_list = subtable_list[1].xpath('.//td')
            if len(subinfo_list) >= 3:
                strtemp = "".join(subinfo_list[2].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['father'] = strtemp

        if len(subtable_list) >= 3:
            subinfo_list = subtable_list[2].xpath('.//td')
            if len(subinfo_list) >= 3:
                strtemp = "".join(subinfo_list[2].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['pn'] = strtemp

        if len(subtable_list) >= 4:
            subinfo_list = subtable_list[3].xpath('.//td')
            if len(subinfo_list) >= 3:
                strtemp = "".join(subinfo_list[2].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['website'] = strtemp

        if len(subtable_list) >= 6:
            subinfo_list = subtable_list[5].xpath('.//td')
            if len(subinfo_list) >= 3:
                strtemp = "".join(subinfo_list[2].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['newaddr'] = strtemp

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
