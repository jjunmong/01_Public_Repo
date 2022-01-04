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

    outfile = codecs.open('audi_svc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|SUBNAME2|TELNUM|NEWADDR|FEAT@@아우디서비스\n")

    while True:
        storeList = getStores('S')
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['dealer'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        break     # 한 페이지에 모든 정보 다 있음

    outfile.close()

def getStores(type_info):
    url = 'http://www.audi.co.kr'
    api = '/kr/web/ko/service/service-center.html'
    data = {}
    params = urllib.urlencode(data)

    try:
        # result = urllib.urlopen(url + api, params)
        result = urllib.urlopen(url + api)
    except:
        print('Error calling the API');
        return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    subapi_list = tree.xpath('//a[@class="nm-layerLink nm-link nm-el-lk nm-el-lk-01 nm-at-lk-b nm-el-lk-ast"]/@href')

    storeList = []
    for i in range(len(subapi_list)):
        suburl = url + subapi_list[i]

        try:
            print(suburl)
            time.sleep(random.uniform(0.3, 0.7))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the subAPI');  continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % subcode);  continue

        subresponse = subresult.read()
        # print(subresponse)
        subtree = html.fromstring(subresponse)

        temp_list = subtree.xpath('//div[@class="nm-content-paragraph__text-container"]')
        if len(temp_list) < 1: continue

        info_entity = temp_list[0]
        subname_list = info_entity.xpath('.//h3')
        info_list = info_entity.xpath('.//div[@class="audi-copy-m nm-content-paragraph__text"]')
        dealername_list = info_entity.xpath('.//span[@class="audi-link-m__text"]')

        if len(subname_list) < 1: continue
        if len(info_list) < 1: continue  # 최소 1개 필드 있어야 함

        storeInfo = {}
        storeInfo['name'] = '아우디서비스';     storeInfo['feat'] = ''
        subname = subname_list[0].text.lstrip().rstrip().replace(' ', '')
        if subname.startswith('아우디'): subname = subname[3:].lstrip()
        if subname.startswith('서비스'): subname = subname[3:].lstrip()
        if subname.startswith('센터'):
            subname = subname[2:].lstrip()
            storeInfo['feat'] = '센터'
        if subname.startswith('익스프레스'):
            subname = subname[5:].lstrip()
            storeInfo['feat'] = '익스프레스'

        if not subname.endswith('센터'): subname += '서비스센터'
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['newaddr'] = '';  storeInfo['pn'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp == None: continue
        strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        idx = strtemp.find('주 소 :')
        if idx == -1: continue
        strtemp = strtemp[idx+5:].lstrip()

        idx = strtemp.find('T e l :')
        if idx == -1: continue
        storeInfo['newaddr'] = strtemp[:idx].rstrip()
        strtemp = strtemp[idx + 7:].lstrip()

        idx = strtemp.find('E-mail')
        if idx != -1:
            storeInfo['pn'] = strtemp[:idx].rstrip()
        else:
            idx = strtemp.find(' ')
            if idx != -1:
                storeInfo['pn'] = strtemp[:idx]

        storeInfo['dealer'] = ''
        if len(dealername_list) > 0:
            storeInfo['dealer'] = dealername_list[0].text

        storeList += [storeInfo]

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
