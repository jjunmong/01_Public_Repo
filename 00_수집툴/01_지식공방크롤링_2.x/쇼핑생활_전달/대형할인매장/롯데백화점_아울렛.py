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

    outfile = codecs.open('lotte_department_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR@@롯데백화점\n")

    outfile2 = codecs.open('lotte_outlet_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|MTYPE@@롯데아울렛\n")

    page = 1
    while True:
        store_list = getStores2(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['newaddr'])

            if store['name'].find('아울렛') != -1:
                outfile2.write(u'%s|' % store['name'])
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['addr'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s\n' % u'아울렛')

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()

# v2.0 (2019/1)
def getStores2(intPageNo):
    url = 'https://www.lotteshopping.com'
    api = '/common/sitemap'
    data = {}
    params = urllib.urlencode(data)
    # print(params)

    try:
        urls = url + api
        #urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    brand_list = tree.xpath('//ul[@class="sitemap_list03"]//li[@class="one"]')
    brand_list += tree.xpath('//ul[@class="sitemap_list03"]//li[@class="two"]')

    result_list = []
    for i in range(len(brand_list)):
        brandname_list = brand_list[i].xpath('.//p//img/@alt')
        if len(brandname_list) < 1: continue
        brandname = brandname_list[0]
        korean_brandname = '롯데백화점'

        if brandname == 'LOTTE DEPARTMENT STORE':
            korean_brandname = '롯데백화점'
        elif brandname == 'AVENUEL':
            korean_brandname = '롯데에비뉴엘'
        elif brandname == 'LOTTE young PLAZA':
            korean_brandname = '롯데영플라자'
        elif brandname == 'LOTTE PREMIUM OUTLETS':
            korean_brandname = '롯데프리미엄아울렛'
        elif brandname == 'LOTTE OUTLETS':
            korean_brandname = '롯데아울렛'
        elif brandname == 'elCUBE':
            korean_brandname = '롯데엘큐브'

        temp_list = brand_list[i].xpath('.//ul[@class="list"]//li//a')
        for j in range(len(temp_list)):

            store_info = {}
            store_info['name'] = korean_brandname
            store_info['subname'] =''
            store_info['pn'] = ''
            store_info['addr'] = '';            store_info['newaddr'] = '';
            store_info['ot'] = ''

            strtemp = "".join(temp_list[j].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['subname'] = strtemp

            if store_info['name'] == '롯데아울렛' and store_info['subname'].startswith('팩토리'):
                store_info['name'] = '롯데팩토리아울렛'
                store_info['subname'] = store_info['subname'][3:].lstrip()

            # '/branchShopGuide/floorGuideSub?cstr=0343'
            suburl_list = temp_list[j].xpath('./@href')
            if len(suburl_list) < 1:
                result_list += [store_info];    continue

            suburl = suburl_list[0]
            try:
                suburl = url + suburl
                print(suburl)  # for debugging
                time.sleep(random.uniform(0.3, 0.9))
                subresult = urllib.urlopen(suburl)
            except:
                print('Error calling the suburl');
                result_list += [store_info]
                continue

            code = subresult.getcode()
            if code != 200:
                print('suburl HTTP request error (status %d)' % code);
                result_list += [store_info]
                continue

            subresponse = subresult.read()
            #print(subresponse)
            #subtree = html.fromstring(subresponse)
            subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + subresponse)

            pn_list = subtree.xpath('//div[@class="contact"]//p[@class="tel"]')
            if len(pn_list) > 0:
                strtemp = "".join(pn_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    store_info['pn'] = strtemp

            addr_list = subtree.xpath('//div[@class="info_box"]//p[@class="addr"]')
            if len(pn_list) > 0:
                strtemp = "".join(addr_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('�', ' ').replace('null', '').rstrip().lstrip()
                    store_info['newaddr'] = strtemp

            # 결과 문자열에서 x, y 좌표값도 얻을 수 있음
            # var latitude    = parseFloat("36.307803");
            # var longitude   = parseFloat("126.901332");

            result_list += [store_info]

    return result_list

# v1.0
def getStores(intPageNo):
    url = 'http://store.lotteshopping.com'
    api = '/handler/Main-Start'
    data = {
        'subBrchCd': '001',
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

    entity_list = tree.xpath('//dl[@class="dropdown dropleft"]//li/button')

    result_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('./@value')
        if len(temp_list) == 0: continue

        strtemp = temp_list[0]
        subname = entity_list[i].text

        data['subBrchCd'] = strtemp
        params = urllib.urlencode(data)

        try:
            suburl = url + '/handler/publicCtr_F-mapstart' + '?' + params
            print(suburl)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
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
        store_info['name'] = '롯데백화점'
        store_info['subname'] = subname.lstrip().rstrip()

        store_info['pn'] = ''
        store_info['addr'] = '';     store_info['newaddr'] = '';   store_info['ot'] = ''

        info_node = subtree.xpath('//div[@class="map_api map_api_new"]/div[@class="info"]')
        desc_node = subtree.xpath('//div[@class="bn_info"]//dl//dd')
        if len(info_node) > 0:
            info_list = info_node[0].xpath('.//p')

            if len(info_list) < 3: continue  # 최소 3개 필드 있어야

            if len(desc_node) > 0:
                strtemp = "".join(desc_node[0].itertext())
                if strtemp != None:
                    if strtemp.find('프리미엄 아울렛') != -1 or strtemp.find('프리미엄 롯데 아울렛') != -1:
                        store_info['name'] = '롯데프리미엄아울렛'
                    elif strtemp.find('아울렛') != -1 or strtemp.find('롯데몰 진주점') != -1:
                        store_info['name'] = '롯데아울렛'
                    elif strtemp.find('아울렛') != -1 or strtemp.find('롯데몰 군산점') != -1:
                        store_info['name'] = '롯데아울렛'
                    elif strtemp.find('영플라자') != -1:
                        store_info['name'] = '롯데영플라자'
                    elif strtemp.find('에비뉴엘') != -1 or strtemp.find('애비뉴엘') != -1:
                        store_info['name'] = '롯데에비뉴엘'
                        if store_info['subname'] == '에비뉴엘' or store_info['subname'] == '애비뉴엘':
                            store_info['subname'] = '본점'
                    # 에비뉴엘 잠실점은 크롤링되지 않음(별도 사이트로 운영), 센트럴스퀘어 팩토리아울렛은 사이트에 없음 ㅠㅠ
                    elif strtemp.find('el cube') != -1 or strtemp.find('elcube') != -1 or strtemp.find('엘큐브') != -1:
                        store_info['name'] = '롯데엘큐브'

            if store_info['name'] == '롯데아울렛' and store_info['subname'].startswith('팩토리'):
                store_info['name'] = '롯데팩토리아울렛'
                store_info['subname'] = store_info['subname'][3:].lstrip()

            store_info['subname'] = store_info['subname'].replace(' ', '/')

            strtemp = "".join(info_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('대표번호 : '): strtemp = strtemp[7:].lstrip()
                idx = strtemp.find('(')
                if idx != -1: strtemp = strtemp[:idx].rstrip()
                store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')

            strtemp = "".join(info_list[1].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('주 소'): strtemp = strtemp[3:].lstrip()
                store_info['newaddr'] = strtemp

            strtemp = "".join(info_list[2].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('지번주소'): strtemp = strtemp[4:].lstrip()
                store_info['addr'] = strtemp

        result_list += [store_info]

    return result_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
