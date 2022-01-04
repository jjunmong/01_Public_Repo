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

brand_list = {
    u'애슐리': 'AL',
}

brand_list2 = {
    u'애슐리': 'AL',
    u'자연별곡': 'JB',
    u'피자몰': 'PM',
    u'수사': 'SS',
    u'샹하오': 'CW',
    u'로운': 'RU',
    u'리미니': 'RI',
    u'테루': 'TL',
    u'아시아문': 'OR',
    u'후원': 'HW',
    u'반궁': 'KR',
    u'글로버거': 'GB',
    u'비사이드': 'BE',
    u'다구오': 'FP',
    u'더카페': 'TC',
    u'루고': 'LG',
    u'프랑제리': 'FB',
    u'페르케노': 'PC',
    #u'애슐리투고': 'AT',
    u'페어링6': 'AQ',
    #u'모뉴망': 'DB',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('ashley_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|SOURCE2|OT|PARKING@@애슐리\n")

    for brand in sorted(brand_list):

        page = 1
        while True:
            storeList = getStores(brand_list[brand], brand, page)
            if storeList == None: break
            if len(storeList) == 0: break

            for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['name'])   # 'SOURCE" 정보로 브랜드이름 지정
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s\n' % store['parking'])
            page += 1

            if page == 101:
                break

            time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(strBrandCode, strBrandName, intPageNo):
    url = 'http://www.elandeat.com'
    api = '/brandDetail/'
    data = {
        'SearchString': ''
    }
    data['Brand'] = strBrandCode
    data['CurPage'] = intPageNo

    api += strBrandCode     # 이랜드계열은 특이하게 이렇게 호출해야 함
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
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

    tableSelector = '//table[@class="tbl_horizen"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if(infoList == None): continue;     # 1번째 <tr>에는 <td>가 하나도 없음 (필드 소갯글 영역)

        if (len(infoList) < 9): continue    # 5개 필드 있음

        storeInfo['name'] = infoList[2].text.rstrip().lstrip()

        strSubName = infoList[3].xpath('.//a')[0].text
        strtemp = strSubName.rstrip().lstrip()
        if strtemp.startswith(strBrandName): strtemp = strtemp[len(strBrandName):].lstrip()
        storeInfo['subname'] = strtemp.replace(' ', '/')

        storeInfo['newaddr'] = infoList[4].text.rstrip().lstrip()
        storeInfo['pn'] = ''
        strtemp = infoList[5].text          # 정보가 없는 경우도 있어서 rstip() lstrip() 호출하면 오류 발생
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace(' ', '')
            storeInfo['pn'] = strtemp.replace('.', '-').replace(')', '-')

        storeInfo['ot'] = ''
        strtemp = infoList[6].text          # 정보가 없는 경우도 있어서 rstip() lstrip() 호출하면 오류 발생
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace(' ', '')
            storeInfo['ot'] = strtemp

        storeInfo['parking'] = ''
        strtemp = infoList[7].text    # 정보가 없는 경우도 있어서 rstip() lstrip() 호출하면 오류 발생
        if strtemp != None:
            strtemp = strtemp.lstrip().rstrip().replace(' ', '')
            storeInfo['parking'] = '주차' + strtemp

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
