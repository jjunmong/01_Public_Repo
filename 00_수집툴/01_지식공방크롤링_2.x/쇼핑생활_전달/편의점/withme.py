# -*- coding: utf8 -*-

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

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('withme_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|XCOORD|YCOORD@@이마트24\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break
        elif len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'이마트24|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 999:     # 2020년 1월 기준 907까지 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.emart24.co.kr'
    api = '/introduce2/findBranch.asp'      # '/introduce/findBranch.asp' 에서 '/introduce2/findBranch.asp'로 변경됨 (2018/5)
    data = {
        'wpsido': '',
        'spgugun': '',
        'service_cv': '',
        'stplacesido': '',
        'stplacegugun': '',
        'sText': ''
    }
    data['cpage'] = intPageNo

    params = urllib.urlencode(data)
    print(params)

    try:
        #urls = url + api + '?' + params
        #print(urls)     # for debugging
        #result = urllib.urlopen(urls)

        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None


    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    response = unicode(response, 'euc-kr',errors = 'ignore') # 'utf-8'이라고 되어 있는데 'euc-kr'로 반환하는 것 같음
    #print(response)
    tree = html.fromstring(response)

    tableSelector = '//div[@class="find_listArea openList"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody//tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if infoList == None: continue;      # for safety
        elif len(infoList) < 2: continue    # 2개 필드 있음

        strSubName = "".join(infoList[0].itertext()).strip('\r\t\n')
        storeInfo['subname'] = strSubName.rstrip().lstrip().replace(' ', '/')

        featList = infoList[1].xpath('.//p')

        if len(featList) < 3: continue

        storeInfo['newaddr'] = ''
        strtemp = "".join(featList[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            idx = strtemp.find('|')
            if idx != -1:
                strtemp = strtemp[:idx].rstrip()
            storeInfo['newaddr'] = strtemp.rstrip().lstrip()

        storeInfo['pn'] = ''
        strtemp = "".join(featList[2].itertext()).strip('\r\t\n')
        if strtemp != None:
            strtemp = strtemp.replace('전화번호 :', '').replace('전화번호:', '').replace('전화번호', '').lstrip().rstrip()
            storeInfo['pn'] = strtemp.rstrip().lstrip()

        storeInfo['feat'] = ''
        svcList = featList[1].xpath('.//img/@src')
        for j in range(len(svcList)):
            strtemp = svcList[j]
            if strtemp.endswith('1_on.png'):
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '24시간'
            elif strtemp.endswith('2_on.png'):
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '원두커피'
            elif strtemp.endswith('3_on.png'):
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '의약품'
            elif strtemp.endswith('4_on.png'):
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '택배'
            elif strtemp.endswith('5_on.png'):
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '스포츠토토'
            elif strtemp.endswith('6_on.png'):
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += 'ATM'
            elif strtemp.endswith('7_on.png'):
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += 'POSA'

        # 좌표정보 추출
        storeInfo['xcoord'] = ''
        storeInfo['ycoord'] = ''
        if len(featList) > 4:
            temp_list = featList[3].xpath('.//a/@href')
            if len(temp_list) > 0:
                strtemp = temp_list[0]
                idx = strtemp.find("searcMap(")
                if idx != -1:
                    temp_list2 = strtemp[idx+9:].lstrip().rstrip().split(',')
                    if len(temp_list2) >= 2:
                        storeInfo['xcoord'] = temp_list2[1].lstrip().rstrip()[1:-1]
                        storeInfo['ycoord'] = temp_list2[0].lstrip().rstrip()[1:-1]

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
