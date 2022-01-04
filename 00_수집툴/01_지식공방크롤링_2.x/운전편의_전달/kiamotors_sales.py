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
import xml.etree.ElementTree as ElementTree

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('kiamotors_sales_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|COMMENTS|PARKINFO|XCOORD|YCOORD\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'기아자동차|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['intro'])
            outfile.write(u'%s|' % store['parkinfo'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 999: break
        elif len(storeList) < 10: break

        delay_time = random.uniform(0.3, 1.1)
        time.sleep(delay_time)

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.kia.com'
    api = '/api/kia_korea/base/br01/branchInfo.selectBranchInfoList'
    data = {
        'sc.searchKey[2]': '',
        'sc.searchType[2]': '',
        'sortKey[0]': 'typeSort',
        'sortKey[1]': 'branchNm',
        'sortType[0]': 'A',
        'sortType[1]': 'A',
    }
    data['pageNum'] = intPageNo

    params = urllib.urlencode(data)
    print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #response = unicode(response, 'euc-kr')     # euc-kr to utf-8 변환
    #print(response)

    idx = response.find('"dataInfo":')
    if idx == -1: return None

    response = response[idx+11:]
    idx = response.find('}],"param')
    if idx == -1: return None

    response = response[:idx+2]
    #print(response)

    data_list = json.loads(response)  # json 포맷으로 결과값 반환

    storeList = []
    for data_item in data_list:
        storeInfo = {}

        storeInfo['subname'] = ''
        strtemp = data_item['branchNm']
        if strtemp != None:
            if strtemp.endswith('지점'): pass
            elif strtemp.endswith('점'): pass
            else: strtemp += '지점'
            storeInfo['subname'] = strtemp

        storeInfo['pn'] = data_item['tel']
        storeInfo['newaddr'] = data_item['addr']

        storeInfo['intro'] = ''
        strtemp = data_item['introduce']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            storeInfo['intro'] = strtemp

        storeInfo['parkinfo'] = ''
        stetemp = data_item['prk']
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            storeInfo['parkinfo'] = strtemp

        storeInfo['ycoord'] = data_item['lat']
        storeInfo['xcoord'] = data_item['lng']

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
