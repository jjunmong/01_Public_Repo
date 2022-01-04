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
import xml.etree.ElementTree as ElementTree

sido_list2 = {      # 테스트용 시도 목록
    #'대전': '042'
}

sido_list_new = {      # 테스트용 시도 목록
    '경기': '031',       # 경기도는 다른 방식으로 수집해야 함 ㅠㅠ (2018/8)
    '광주': '062',
}

sido_list = {
    '서울': '02',
    '광주': '062',
    '대구': '053',
    '대전': '042',
    '부산': '051',
    '울산': '052',
    '인천': '032',
    #'경기': '031',       # 경기도는 다른 방식으로 수집해야 함 ㅠㅠ (2018/8)
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

    outfile = codecs.open('nenechicken_new_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR@@네네치킨\n")

    for sido_name in sorted(sido_list):

        storeList = getStores(sido_name)
        if storeList == None: continue
        elif len(storeList) == 0: continue

        for store in storeList:
            outfile.write(u'네네치킨|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])

            strtemp = store['newaddr']
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '')
            strtemp = strtemp.replace('101호', ' 101호').replace('102호', ' 102호').replace('103호', ' 103호').replace('104호', ' 104호').replace('105호', ' 105호').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('106호', ' 106호').replace('107호', ' 107호').replace('108호', ' 108호').replace('109호', ' 109호').replace('110호', ' 110호').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('.1층', ' 1층').replace('.2층', ' 2층')
            outfile.write(u'%s\n' % strtemp)

        time.sleep(random.uniform(0.3, 1.1))

    for sido_name_new in sorted(sido_list_new):
        page = 1
        while True:
            store_list = getStoresNew(sido_name_new, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'네네치킨|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])

                strtemp = store['newaddr']
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '')
                strtemp = strtemp.replace('101호', ' 101호').replace('102호', ' 102호').replace('103호', ' 103호').replace('104호', ' 104호').replace('105호', ' 105호').replace('  ', ' ').lstrip().rstrip()
                strtemp = strtemp.replace('106호', ' 106호').replace('107호', ' 107호').replace('108호', ' 108호').replace('109호', ' 109호').replace('110호', ' 110호').replace('  ', ' ').lstrip().rstrip()
                strtemp = strtemp.replace('.1층', ' 1층').replace('.2층', ' 2층')
                outfile.write(u'%s\n' % strtemp)

            page += 1

            if page == 99: break
            elif len(store_list) < 24: break

            time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(sido_name):
    url = 'http://nenechicken.com'
    api = '/subpage/where_list.asp'
    data = {
        'proc_type': 'step2',
        'target_step2': 0,
    }
    data['target_step1'] = sido_name
    print(sido_name)

    params = urllib.urlencode(data)
    #print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API')
        return None

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    try:
        response = result.read()
        #print(response)
        root = ElementTree.fromstring(response)
        # root = tree.getroot()
    except:
        print('no return value')
        return None

    storeList = []
    for child in root:
        storeInfo = {}
        subname_info = child.find('aname1').text
        sgg_name =  child.find('aname3').text
        idx = subname_info.find(sgg_name)
        if idx != -1:
            subname_info = subname_info[idx+len(sgg_name):].lstrip()
        storeInfo['subname'] = subname_info
        addr_part1 = child.find('aname4').text
        addr_part2 = child.find('aname5').text
        jibun_part = ''

        idx = addr_part1.rfind(' ')
        if idx != -1:
            road_name = addr_part1[idx+1:]
            idy = addr_part2.rfind(road_name)
            if idy != -1:
                jibun_part = addr_part2[idy+len(road_name):].lstrip()
            else:
                addr_part1_wo_rdname = addr_part1[:idx].rstrip()
                idx = addr_part1_wo_rdname.rfind(' ')
                if idx != -1:
                    marker = addr_part1_wo_rdname[idx+1:]
                    idy = addr_part2.rfind(marker)
                    if idy != -1:
                        addr_part1 = addr_part1_wo_rdname
                        jibun_part = addr_part2[idy + len(marker):].lstrip()

        if jibun_part != '':
            storeInfo['newaddr'] = addr_part1 + ' ' + jibun_part
        else: storeInfo['newaddr'] = addr_part2

        storeInfo['pn'] = child.find('aname7').text

        storeList += [storeInfo]

    return storeList


def getStoresNew(sido_name, page_no):
    url = 'https://nenechicken.com'
    api = '/17_new/sub_shop01.asp'
    data = {
        'GUBUN': 'C',
        'ex_select': 1,
        'ex_select2': '',
    }
    data['IndexSword'] = sido_name
    data['page'] = page_no
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//table[@class="shopTable"]//tr')

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 3: continue  # 최소 3개 필드 있어야 함

        store_info = {}

        store_info['name'] = '네네치킨'
        store_info['subname'] = ''

        name_list = info_list[0].xpath('.//div[@class="shopName"]')
        addr_list = info_list[0].xpath('.//div[@class="shopAdd"]')
        if len(name_list) < 1 or len(addr_list) < 1: continue

        strtemp = "".join(addr_list[0].itertext())
        sggname = ''
        newaddr_header = ''
        rdname = ''
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            newaddr_header = strtemp
            addr_list = strtemp.split(' ')
            if len(addr_list) >= 2:
                sggname = addr_list[1]
                rdname = addr_list[len(addr_list)-1]

        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if sggname != '':
                idx = strtemp.find(sggname)
                if idx > 0:
                    strtemp = strtemp[idx+len(sggname):].lstrip()

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['pn'] = ''
        pn_list = info_list[1].xpath('.//span[@class="tooltiptext"]')
        if len(pn_list) > 0:
            strtemp = "".join(pn_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')

        store_info['newaddr'] = ''
        temp_list = info_list[2].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('codeAddress(')
            if idx != -1:
                strtemp = strtemp[idx+12:].lstrip()
                idx = strtemp.rfind(');')
                if idx != -1:
                    strtemp = strtemp[:idx].replace('\'', '').lstrip().rstrip()
                    if rdname != '':
                        idx = strtemp.rfind(rdname)
                        if idx != -1:
                            store_info['newaddr'] = newaddr_header + ' ' + strtemp[idx+len(rdname):].lstrip()
                        else:
                            store_info['newaddr'] = strtemp
                    else:
                        store_info['newaddr'] = strtemp

        store_list += [store_info];

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
