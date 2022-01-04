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

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('addal_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@감탄떡볶이\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'감탄떡볶이|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 19: break
        elif len(storeList) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.gamtan.co.kr'
    api = '/page/store/shop.php'
    data = {
        'catetype': '',
        'key': '',
        'keyword': '',
        'pstate': '',
        'gubun': '',
        'code': ''
    }
    data['page'] = intPageNo

    params = urllib.urlencode(data)
    # print(params)

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
    #print(response)
    tree = html.fromstring(response)

    tableSelector = '//div[@class="board_list01"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        suburl_info_list = infoList[1].xpath('.//a/@href')
        if len(suburl_info_list) == 0:
            continue

        # suburl_info= "('/addal/store/addal_search_view_popup.php?serial=1207&searchoption=&keyword=&code=', 'mSearch', 462, 560);"
        suburl_info = suburl_info_list[0]
        idx = suburl_info.find('(\'')
        if idx == -1: continue
        suburl_info = suburl_info[idx+2:]
        idx = suburl_info.find('\',')
        if idx == -1: continue
        suburl_info = suburl_info[:idx]

        suburl = url + suburl_info

        try:
            print(suburl)
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburl)
        except:
            errExit('Error calling the suburl')

        subcode = subresult.getcode()
        if subcode != 200:
            errExit('suburl HTTP request error (status %d)' % subcode)

        subresponse = subresult.read()
        subtree = html.fromstring(subresponse)

        subtableSelector = '//div[@class="shopview_list"]'
        subdataTable = subtree.xpath(subtableSelector)[0]

        infoSelector = './/tbody//tr'
        infoList = subdataTable.xpath(infoSelector)

        if(infoList == None): continue;     # for safety
        if (len(infoList) < 4): continue    # 5개 필드 있음 (앞에서 4개가 정보 추출 대상 필드)

        strSubName = infoList[0].xpath('.//td')[0].text
        strSubName = strSubName.replace('감탄-', '').replace('감탄', '').lstrip().rstrip()
        storeInfo['subname'] = strSubName.rstrip().lstrip().replace(' ', '/')

        storeInfo['ot'] = ''
        strtemp = infoList[1].xpath('.//td')[0].text
        if strtemp != None: storeInfo['ot'] = strtemp.rstrip()

        storeInfo['newaddr'] = ''
        strtemp = infoList[2].xpath('.//td')[0].text
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip()

        storeInfo['pn'] = ''
        strtemp = infoList[3].xpath('.//td')[0].text
        if strtemp != None: storeInfo['pn'] = strtemp.rstrip()

        storeInfo['xcoord'] = '';       storeInfo['ycoord'] = ''
        temp_list = subtree.xpath('//iframe[@id="frame_map"]/@src')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            if strtemp != None:
                # '"map_new.html?serial=110&map_pointx=37.64569448&map_pointy=127.2349994&areacode=C100&shopname=평내점'
                strtemp = strtemp.lstrip().rstrip()
                idx = strtemp.find('&map_pointy=')
                if idx != -1:
                    strtemp2 = strtemp[idx+12:]
                    idx = strtemp2.find('&')
                    storeInfo['xcoord'] = strtemp2[:idx]
                idx = strtemp.find('&map_pointx=')
                if idx != -1:
                    strtemp2 = strtemp[idx+12:]
                    idx = strtemp2.find('&')
                    storeInfo['ycoord'] = strtemp2[:idx]

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
