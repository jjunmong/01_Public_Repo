# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
import random
import requests
import bs4
#import json
from lxml import html
import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context()
sido_list = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list2 = {
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

    outfile = codecs.open('kicaca_utf8.txt', 'w', 'utf-8')
    #outfile.write("##NAME|SUBNAME|ETCNAME|TELNUM|NEWADDR|SIZE|SINCE|WEBSITE|SOURCE2@@대형예술센터\n")
    outfile.write("##NAME|SUBNAME|ETCNAME|TELNUM|NEWADDR|SINCE|WEBSITE|SOURCE2@@대형예술센터\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['etcname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            #outfile.write(u'%s|' % store['size'])
            outfile.write(u'%s|' % store['since'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s\n' % u'한국문화예술회관연합회')

        page += 1

        if page == 2: break     # 한번 호출로 전체 정보 얻을 수 있음
        elif len(store_list) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'http://www.kocaca.or.kr/Pages/Member/OrgInformation.aspx'
    url = 'https://www.kocaca.or.kr'
    api = '/Pages/Member/OrgInformation.aspx'
    data = {}
    #params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        #urls = url + api + '?' + params
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls, context = context)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)

    id_list = tree.xpath('//div[@class="tbl_list"]//table//tbody//td//a/@idorg')

    store_list = []
    for i in range(len(id_list)):
        id = id_list[i]

        try:
            suburls = 'http://www.kocaca.or.kr/Pages/Member/Popup/OrgDetail.aspx?IdOrg=' + id
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburls)
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

        name_list = subtree.xpath('//div[@class="postcode_title"]//p[@class="postcode"]')
        info_list = subtree.xpath('//table[@class="post_privacy_tbl member_pop_tbl"]//tbody//tr')

        if len(name_list) < 1: continue

        organization_name = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            strtemp = strtemp.replace('(재)', '')
            if strtemp.endswith(')'):
                idx = strtemp.find('(')
                if idx != -1:
                    organization_name = strtemp[:idx].rstrip()
                    strtemp = strtemp[idx+1:-1].lstrip().rstrip()

        if strtemp == '평택시 남부, 북부, 서부문화예술회관':   # 데이터가 부정확하게 입력되어 있는 경우 ㅠㅠ
            organization_name = '평택시'
            strtemp = '남부문화예술회관'

        hallname_list = strtemp.split(',')

        for j in range(len(hallname_list)):
            hall_name = hallname_list[j].lstrip().rstrip()

            store_info = {}

            store_info['name'] = hall_name
            store_info['subname'] = ''
            store_info['etcname'] = organization_name

            store_info['newaddr'] = ''
            store_info['pn'] = ''
            store_info['size'] = ''
            store_info['since'] = ''
            store_info['website'] = ''

            for k in range(len(info_list)):
                tag_list = info_list[k].xpath('.//th')
                value_list = info_list[k].xpath('.//td')

                if len(tag_list) < 1 or len(value_list) < 1: continue

                tag = "".join(tag_list[0].itertext())
                value = "".join(value_list[0].itertext())

                if tag == None or value == None: continue

                tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

                if tag == '위치':
                    store_info['newaddr'] = value
                elif tag == '개관일':
                    store_info['since'] = value
                elif tag == '전화번호':
                    store_info['pn'] = value
                elif tag == '홈페이지':
                    store_info['website'] = value
                elif tag == '규모':
                    store_info['size'] = value

            store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
