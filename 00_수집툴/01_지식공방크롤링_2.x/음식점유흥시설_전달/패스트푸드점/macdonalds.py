# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import random
import codecs
import urllib
#import json
from lxml import html

area2 = {
    '서울특별시': '02'
}

area = {
    '서울특별시': '02',
    '광주광역시': '062',
    '대구광역시': '053',
    '대전광역시': '042',
    '부산광역시': '051',
    '울산광역시': '052',
    '인천광역시': '032',
    '경기도': '031',
    '강원도': '033',
    '경상남도': '055',
    '경상북도': '054',
    '전라남도': '061',
    '전라북도': '063',
    '충청남도': '041',
    '충청북도': '043',
    '제주특별자치도': '064',
    '세종특별자치시': '044'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('mac_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|FEAT|OT@@맥도날드\n")

    for areainfo in area:

        page = 1
        while True:
            storeList = getStores(areainfo, page)
            if storeList == None: break
            elif len(storeList) == 0: break

            for store in storeList:
                outfile.write("맥도날드|")
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['feat'])
                outfile.write(u'%s\n' % store['ot'])

            page += 1

            if page == 101:
                break

            time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(search_keyword, intPageNo):
    url = 'http://www.mcdonalds.co.kr'
    api = '/www/kor/findus/district.do'

    data = {
        'sSearch_yn': 'Y',
        'skey': 2,
        'skey1': '',
        'skey2': '',
        'skey4': '',
        'skey5': '',
        'skeyword2': '',
        'sflag1': '',
        'sflag2': '',
        'sflag3': '',
        'sflag4': '',
        'sflag5': '',
        'sflag6': '',
        'sflag': 'N'
    }
    data['skeyword'] = search_keyword
    data['pageIndex'] = intPageNo

    params = urllib.urlencode(data)
    print(params)

    try:
        #result = urllib.urlopen(url + api, params)

        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API')
        return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)


    tableSelector = '//div[@class="searchResult"]'
    dataTable = tree.xpath(tableSelector)[0]

    nameSelector = '//div[@class="detail"]//dl[@class="clearFix"]/dt/a'
    addrSelector = '//div[@class="detail"]//dd[@class="road"]'
    pnSelector = '//div[@class="detail"]//dl[@class="clearFix"]//dd'
    #featSelector = '//div[@class="detail"]//dd[@class="infoCheck"]//span'
    featSelector = '//div[@class="detail"]//dd[@class="infoCheck"]'

    nameList = dataTable.xpath(nameSelector)
    addrList = dataTable.xpath(addrSelector)
    pnList = dataTable.xpath(pnSelector)
    featList = dataTable.xpath(featSelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(nameList)):
        storeInfo = {}

        strtemp = "".join(nameList[i].itertext())
        strtemp = strtemp.replace('\r', '').replace("\n", '').replace(' ', '')
        storeInfo['name'] = strtemp.strip('\n\t\r')

        strtemp = addrList[i].text.strip('\n\t\r')
        idx = strtemp.find('[도로명주소]')
        if (idx != -1): strtemp = strtemp[idx + 7:]
        storeInfo['newaddr'] = strtemp

        storeInfo['addr'] = pnList[i*4+1].text.strip('\n\t\r')

        strtemp = pnList[i*4].text
        strtemp = strtemp.replace('\r', '').replace("\n", '').replace(' ', '')
        storeInfo['pn'] = strtemp.strip('\n\t\r')

        features = featList[i].xpath('.//img/@alt')

        idx = 0
        storeInfo['feat'] = ''
        for feat_item in features:
            if(idx != 0):
                storeInfo['feat'] += ';'

            feat_item = feat_item.replace('있음', '').lstrip().rstrip()

            storeInfo['feat'] += feat_item
            idx += 1

        storeInfo['ot'] = ''
        info_list = featList[i].xpath('.//tbody//tr//td')
        if len(info_list) >= 1:
            strtemp = "".join(info_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                storeInfo['ot'] = strtemp

        if len(info_list) >= 5:
            strtemp = "".join(info_list[4].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if storeInfo['ot'] != '': storeInfo['ot'] += ';'
                storeInfo['ot'] += '맥딜리버리:'
                storeInfo['ot'] += strtemp

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
