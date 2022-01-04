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
#import json
from lxml import html

sido_list2 = {      # 테스트용 시도 목록
    '대전': '042'
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

    outfile = codecs.open('emart_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|OFFDAY|FEAT|SIZE|PARKING|XCOORD|YCOORD@@이마트\n")

    page = 1
    while True:
        storeList = getStores2(page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['offday'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['size'])
            outfile.write(u'%s|' % store['parking'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 모든 점포 정보 얻을 수 있음
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0
def getStores2(intPageNo):
    url = 'http://store.emart.com'
    api = '/branch/list.do'
    data = {
    }
    data['startPage'] = intPageNo
    params = urllib.urlencode(data)

    try:
        print(url+api)
        result = urllib.urlopen(url+api)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    suburl_list = tree.xpath('//ul[@id="branchList"]//li/a/@onclick')

    storeList = []
    for i in range(len(suburl_list)):
        #if i > 10: break  # temporary for testing

        suburl_info = suburl_list[i]
        idx = suburl_info.find('storeView(')
        if idx == -1: continue

        strtemp = suburl_info[idx+10:]
        idx = strtemp.find(')')
        if idx == -1: continue
        shop_id = strtemp[:idx].replace('\'', '')

        subdata = {
            'id': shop_id,
            'culture': 'f',
            'year_code': '',
            'smst_code': '',
        }

        # shop_id 정보도 인쇄할까???

        try:
            suburl = url + '/branch/view.do' + '?' + urllib.urlencode(subdata)
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
        subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + subresponse)

        storeInfo = {}
        storeInfo['name'] = '이마트';   storeInfo['subname'] = '';     storeInfo['feat'] = ''
        storeInfo['addr'] = '';     storeInfo['newaddr'] = '';      storeInfo['pn'] = ''
        storeInfo['ot'] = '';       storeInfo['size'] = '';          storeInfo['parking'] = ''
        storeInfo['offday'] = ''

        subname_info = subtree.xpath('//div[@class="store-header"]//h2')
        subname = "".join(subname_info[0].itertext()).lstrip().rstrip()
        if subname.startswith('SSG'):
            storeInfo['name'] = 'SSG'
            subname = subname[3:].lstrip()
        elif subname.startswith('스타슈퍼'):
            storeInfo['name'] = '스타슈퍼'
            subname = subname[4:].lstrip()
        elif subname.endswith('T'):
            storeInfo['name'] = '이마트트레이더스'
            subname = subname[:-1].rstrip()
        elif subname.startswith('PK PEACOCK'):
            storeInfo['name'] = 'PK PEACOCK'
            subname = subname[10:].lstrip()
        elif subname.startswith('노브랜드'):
            storeInfo['name'] = '노브랜드'
            subname = subname[4:].lstrip()
        elif subname == '센텀점':
            storeInfo['name'] = '이마트더라이프'
        elif subname == 'SF 하남점':
            storeInfo['name'] = '이마트일렉트로마트'

        storeInfo['subname'] = subname.lstrip().rstrip().replace(' ', '/')


        feat_list = subtree.xpath('//div[@class="store-header"]//ul[@class="list-sort"]//li')
        for j in range(len(feat_list)):
            strtemp = "".join(feat_list[j].itertext())
            if strtemp == None: continue

            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if storeInfo['feat'] != '': storeInfo['feat'] += ';'
            storeInfo['feat'] += strtemp.replace(' ', '')


        subinfo_list = subtree.xpath('//div[@class="intro-wrap"]//li')
        for j in range(len(subinfo_list)):
            tag_info = subinfo_list[j].xpath('.//strong')
            value_info = subinfo_list[j].xpath('.//p')

            if len(tag_info) < 1 or len(value_info) < 1: continue

            tag = "".join(tag_info[0].itertext())
            value = "".join(value_info[0].itertext())
            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if tag == '쇼핑시간':
                storeInfo['ot'] = value
            elif tag == '휴점일':
                storeInfo['offday'] = value.replace(' ', '')
            elif tag == '고객센터':
                storeInfo['pn'] = value
            elif tag == '주차시설':
                storeInfo['parking'] = value


        addrinfo_list = subtree.xpath('//dl[@class="paper-data paper-address-paired c-clearfix"]')
        if len(addrinfo_list) > 0:
            tag_info = addrinfo_list[0].xpath('.//dt')
            value_info = addrinfo_list[0].xpath('.//dd')

            for j in range(len(tag_info)):
                tag = "".join(tag_info[j].itertext())
                value = ''
                if j < len(value_info): value = "".join(value_info[j].itertext())

                if tag == None or value == None: continue
                tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                value = value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

                if tag == '도로명':
                    storeInfo['newaddr'] = value
                elif tag == '지번':
                    storeInfo['addr'] = value


        storeInfo['xcoord'] = '';        storeInfo['ycoord'] = ''
        # x,y 값 거꾸로 들어가 있음
        temp_list = subtree.xpath('//div[@class="map"]/@data-x')
        if len(temp_list) > 0: storeInfo['ycoord'] = temp_list[0]
        temp_list = subtree.xpath('//div[@class="map"]/@data-y')
        if len(temp_list) > 0: storeInfo['xcoord'] = temp_list[0]

        storeList += [storeInfo]

    return storeList

# v1.0
def getStores(intPageNo):
    url = 'http://store.emart.com'
    api = '/branch/list.do'
    data = {
    }
    data['startPage'] = intPageNo
    params = urllib.urlencode(data)

    try:
        print(url+api)
        result = urllib.urlopen(url+api)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    suburl_list = tree.xpath('//div[@class="img_map"]//li/a/@href')

    storeList = []
    for i in range(len(suburl_list)):

        suburl_info = suburl_list[i]
        idx = suburl_info.find('?id=')
        if idx == -1: continue

        shop_id = suburl_info[idx+4:]
        subdata = {
            'id': shop_id,
            'culture': 'f',
            'year_code': '',
            'smst_code': '',
        }

        # shop_id 정보도 인쇄할까???

        try:
            suburl = url + '/branch/view.do' + '?' + urllib.urlencode(subdata)
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
        subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + subresponse)

        storeInfo = {}
        storeInfo['name'] = '이마트';   storeInfo['subname'] = '';     storeInfo['feat'] = ''
        storeInfo['addr'] = '';     storeInfo['newaddr'] = '';      storeInfo['pn'] = ''
        storeInfo['ot'] = '';       storeInfo['size'] = '';          storeInfo['parking'] = ''

        subname_info = subtree.xpath('//div[@class="store_intro "]//h2')
        subname = "".join(subname_info[0].itertext()).lstrip().rstrip()
        if subname.startswith('SSG'):
            storeInfo['name'] = 'SSG'
            subname = subname[3:].lstrip()
        elif subname.startswith('스타슈퍼'):
            storeInfo['name'] = '스타슈퍼'
            subname = subname[4:].lstrip()
        elif subname.endswith('T'):
            storeInfo['name'] = '이마트트레이더스'
            subname = subname[:-1].rstrip()
        elif subname == '센텀점':
            storeInfo['name'] = '이마트더라이프'
        elif subname == 'SF 하남점':
            storeInfo['name'] = '이마트일렉트로마트'

        storeInfo['subname'] = subname.lstrip().rstrip().replace(' ', '/')

        subinfo_list = subtree.xpath('//div[@class="intro_wrap"]//li')

        for j in range(len(subinfo_list)):
            subinfo = subinfo_list[j]
            subinfo_attr = subinfo.attrib['class']

            if subinfo_attr == 'num':
                tag_info = subinfo.xpath('.//dt')
                value_info = subinfo.xpath('.//dd')

                if len(value_info) > 0:
                    storeInfo['pn'] = value_info[0].text.replace('.', '-').replace(')', '-')

                for k in range(len(tag_info)):
                    tag = tag_info[k].text.replace(' ', '')
                    value = value_info[k].text

                    if tag == '일렉트로마트':
                        if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                        storeInfo['feat'] += '일렉트로마트'
                    elif tag == '문화센터':
                        if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                        storeInfo['feat'] += '문화센터'
                    elif tag == '더라이프':
                        if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                        storeInfo['feat'] += '더라이프'
                    elif tag == '몰리스펫샵':
                        if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                        storeInfo['feat'] += '몰리스펫샵'

            elif subinfo_attr == 'addr':
                strtemp = subinfo.text
                if strtemp != None:
                    storeInfo['newaddr'] = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                temp_list = subinfo.xpath('//div[@class="layer_addr none"]')
                if len(temp_list) > 0:
                    strtemp = temp_list[0].text
                    if strtemp != None:
                        storeInfo['addr'] = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            elif subinfo_attr == 'time':
                tag_info = subinfo.xpath('.//dt')
                value_info = subinfo.xpath('.//dd')

                if len(value_info) > 0:
                    storeInfo['ot'] = value_info[0].text.lstrip().rstrip()
            elif subinfo_attr == 'noti':
                tag_info = subinfo.xpath('.//dt')
                value_info = subinfo.xpath('.//dd')

                for k in range(len(tag_info)):
                    tag = tag_info[k].text
                    value = value_info[k].text

                    if tag == '매장규모':
                        storeInfo['size'] = value.replace(',', '').replace('㎡', '').lstrip().rstrip()
                    elif tag == '주차시설':
                        if value.startswith('총'): value = value[1:].lstrip()
                        storeInfo['parking'] = value

        storeInfo['xcoord'] = '';        storeInfo['ycoord'] = ''
        # x,y 값 거꾸로 들어가 있음
        temp_list = subtree.xpath('//div[@class="map"]/@data-x')
        if len(temp_list) > 0: storeInfo['ycoord'] = temp_list[0]
        temp_list = subtree.xpath('//div[@class="map"]/@data-y')
        if len(temp_list) > 0: storeInfo['xcoord'] = temp_list[0]

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
