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

#서버에서는 IP차단 먹은 듯한 느낌..............@@@@@

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('twosome_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|ADDR|OT|PARKING@@투썸플레이스\n")

    page = 1
    while True:
        storeList = getStores('P', page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write("투썸플레이스|")
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['parking'])

        page += 1

        if page == 200:     # 2016년12월 기준 77 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    page = 1
    while True:
        storeList = getStores('C', page)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write("투썸커피|")
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['parking'])

        page += 1

        if page == 101:  # 2016년12월 기준 4 페이지까지 정보 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(brandType, intPageNo):
    url = 'https://www.twosome.co.kr:7009'
    api = '/store/search_list.asp'
    data = {
        'area': '',
        'area2': ''
    }
    data['s_gubun'] = brandType
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    #print(params)

    storeList = []

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        #errExit('Error calling the API')
        print('Error calling the API')
        return storeList

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return storeList

    response = result.read()
    response = unicode(response, 'euc-kr')
    #print(response)

    idx = response.find('<![CDATA[')
    if idx != -1:
        response = '<html><body><response>' + response[idx+9:] + '</body></html>'

    tree = html.fromstring(response)

    #tableSelector = '//table[@class="mt30 tbl-list02"]'
    #dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = tree.xpath(entitySelector)

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if (len(infoList) < 4): continue

        strtemp = infoList[1].text
        # 코드 깨지는 문제 해결해야 함!!!
        #strtemp = unicode(strtemp, 'euc-kr').encode('utf-8')
        storeInfo['subname'] = strtemp.replace(' ', '/').replace('\r', '').replace('\t', '').replace('\n', '')
        storeInfo['pn'] = infoList[2].text

        storeInfo['newaddr'] = ''
        storeInfo['addr'] = ''
        storeInfo['ot'] = ''
        storeInfo['parking'] = ''
        strtemp = infoList[3].xpath('.//a/@onclick')[0]    # goStore('1159')
        idx = strtemp.find('goStore')
        if idx != -1:
            strtemp = strtemp[idx+9:len(strtemp)-2]

            if strtemp != "":
                if brandType == "P": final_suburl = url + '/store/storeView.asp?sort_store=' + strtemp
                #else: final_suburl = url + '/coffee/store/storeView.asp?sort_store=' + strtemp      # 투썸커피 (2018/1까지의 url)
                else: final_suburl = url + '/store/storeView.asp?sort_store=' + strtemp     # 투썸커피 url 변경됨 (2018/2)

                delay_time = random.uniform(0.3, 0.9)
                time.sleep(delay_time)

                try:
                    print(final_suburl)
                    subresult = urllib.urlopen(final_suburl)
                except:
                    #errExit('Error calling the suburl')
                    print('Error calling the suburl')
                    continue

                subcode = subresult.getcode()
                if subcode != 200:
                    #errExit('suburl HTTP request error (status %d)' % subcode)
                    print('suburl HTTP request error (status %d)' % subcode)
                    continue

                subresponse = subresult.read()
                #print(subresponse)
                subtree = html.fromstring(subresponse)

                subtableSelector = '//table[@class="tbl-list03"]'
                subdataTableList = subtree.xpath(subtableSelector)
                if len(subdataTableList) < 1:   # 간혹 상세정보가 없는 점포가 있음
                    storeList += [storeInfo]
                    continue

                subdataTable = subtree.xpath(subtableSelector)[0]

                storeInfo['subname'] = ''
                strtemp = subtree.xpath('//div[@id="content"]//h5')[0].text
                if strtemp != None:
                    strtemp = strtemp.lstrip().rstrip()
                    if strtemp.startswith('투썸커피'): strtemp = strtemp[4:].lstrip()
                    elif strtemp.startswith('투썸'): strtemp = strtemp[2:].lstrip()
                    if not strtemp.endswith('점'): strtemp += '점'
                    storeInfo['subname'] = strtemp.replace(' ', '/')

                subentitySelector = './/tbody/tr'
                subentityList = subdataTable.xpath(entitySelector)

                if len(subentityList) >= 5:
                    storeInfo['newaddr'] = subentityList[0].xpath('.//td')[0].text.strip('\r\t\n').lstrip().rstrip()
                    storeInfo['addr'] = subentityList[1].xpath('.//td')[0].text.strip('\r\t\n').lstrip().rstrip()
                    strtemp = subentityList[2].xpath('.//td')[0].text
                    if strtemp != None:
                        storeInfo['ot'] = strtemp.strip('\r\t\n')
                    strtemp = subentityList[4].xpath('.//td')[0].text
                    if strtemp != None:
                        strtemp = strtemp.strip('\r\t\n').lstrip().rstrip()
                        if strtemp == '가능': strtemp = '주차가능'
                        elif strtemp == '불가': strtemp = '주차불가'
                        storeInfo['parking'] = strtemp

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
