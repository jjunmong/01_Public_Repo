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
import json
from lxml import html

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

    outfile = codecs.open('ypbooks_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'영풍문고|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.ypbooks.co.kr'
    api = '/helper.yp'
    data = {
        'targetpage': 'helper_branch',
        'template': 'branch',
        'pageflag': '1',
    }
    params = urllib.urlencode(data)
    # print(params)

    try:
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table/tr/td/a')

    result_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('./@href')
        if len(temp_list) == 0: continue

        strtemp = temp_list[0]
        subname = entity_list[i].text

        if strtemp.find('helper_branch') == -1 or subname == None: continue

        time.sleep(random.uniform(0.3, 0.9))
        try:
            suburl = url + strtemp
            print(suburl)  # for debugging
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');      continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);      continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        store_info = {}
        store_info['subname'] = subname.lstrip().rstrip().replace(' ', '/')

        store_info['pn'] = ''
        store_info['addr'] = '';     store_info['newaddr'] = ''

        addr_node = subtree.xpath('//em[@class="em mT10"]')
        if len(addr_node) > 0:
            strtemp = "".join(addr_node[0].itertext()).lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('도로명')
            if idx != -1:
                strtemp = strtemp[idx+3:].lstrip()
                idx = strtemp.find('지　번')
                if idx != -1:
                    store_info['newaddr'] = strtemp[:idx].rstrip()
                    store_info['addr'] = strtemp[idx+3:].lstrip()
                else:
                    store_info['newaddr'] = strtemp

                result_list += [store_info]
                continue

        info_node  = subtree.xpath('//div[@class="serviceInfo"]//li')
        for j in range(len(info_node)):
            strtemp = "".join(info_node[j].itertext())
            if strtemp == None: continue

            strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            #if strtemp.find('매장주소') == -1: continue

            idx = strtemp.find('도로명')
            if idx != -1:
                strtemp = strtemp[idx + 3:].lstrip()
                idx = strtemp.find('지　번')
                if idx != -1:
                    store_info['newaddr'] = strtemp[:idx].rstrip()
                    store_info['addr'] = strtemp[idx + 3:].lstrip()
                else:
                    store_info['newaddr'] = strtemp

                result_list += [store_info]

            idx = strtemp.find('연락처')
            idx2 = strtemp.find('대표번호')
            if idx != -1 or idx2 != -1:
                if idx != -1: strtemp = strtemp[idx+3:].lstrip().rstrip()
                elif idx2 != -1: strtemp = strtemp[idx2+4:].lstrip().rstrip()

                #store_info['pn'] = strtemp.replace('.', '-').replace(')', '-')     # 전화번호 기술에 규칙성이 너무나 없음 ㅠㅠ (나중에 정리하자!!)

            # 영업시간, 휴무일 정보도 같은 방식으로 추출할 수 있음 (필요할 때 추출할 것!!)

    return result_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
