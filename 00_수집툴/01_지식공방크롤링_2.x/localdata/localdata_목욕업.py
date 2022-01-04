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
import xml.etree.ElementTree as ElementTree

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

api_dict = {
    '/platform/rest/41_19_01_P/openApi': 'xewwrixdpioLGUVTv9TTuKpYO8XTJYdavxJZgK0zoHk=',    #공동탕업
    '/platform/rest/41_22_01_P/openApi': 'UILNYBVy=IXubPTKfkPFmrGzqBjulJo6=DDiSzmf2Dc=',    #공동탕업+찜질시설서비스영업
    '/platform/rest/41_21_01_P/openApi': 'SbIRLOm0uuZPd7HiLqRaYZqE8E8Whu4OywKtknGUxsg=',    #찜질시설서비스영업
    '/platform/rest/41_20_01_P/openApi': 'KOkVqroKkrwjwYKOYq4wozzN0jBUze1AvQa/6iS7Cd8=',    #한증막업
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('localdata_bath_utf8.txt', 'w', 'utf-8')

    for api_item in sorted(api_dict):

        outfile.write("##NEWADDR|NAME|TELNUM|ADDR|STATUS|STATUS2|CAT1|CAT2|SIZE|SINCE|CLOSED|YEAR|FEAT|SOURCE2|MTYPE|X|Y@@TAXBATH\n")

        page = 1
        while True:
            storeList = getStores(api_item, api_dict[api_item], page)
            if storeList == None: break;
            elif len(storeList) == 0: break
            elif len(storeList) == 1:
                if storeList[0]['name'] == '500error':
                    continue

            for store in storeList:
                if store['status'].find('폐업') != -1: continue

                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                # outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['status'])
                outfile.write(u'%s|' % store['status2'])
                outfile.write(u'%s|' % store['cat1'])
                outfile.write(u'%s|' % store['cat2'])
                outfile.write(u'%s|' % store['size'])
                outfile.write(u'%s|' % store['since'])
                outfile.write(u'%s|' % store['closed'])
                outfile.write(u'%s|' % store['year'])  # 개업년도
                outfile.write(u'%s|' % store['feat'])
                outfile.write(u'%s|' % u'LOCALDATA')
                outfile.write(u'%s|' % u'찜질방')
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 1999: break
            elif len(storeList) < 500: break

    outfile.close()

def getStores(strApi, strApiKey, intPageNo):
    url = 'http://www.localdata.kr'
    api = strApi
    data = {
        'pageSize': 500,
        # 'bgnYmd': '20180501',       # 시작일자(YYYYMMDD)
        # 'endYmd': '20180531',       # 종료일자(YYYYMMDD)
        'state': '01',  # 운영상태코드 01:운영/02:휴업/03:폐업
        #'authKey': 'AqXywICvW92rXYFWfzc=28PrYVhKpCBzHa=bpMQJZEM='
    }
    data['pageIndex'] = intPageNo
    data['authKey'] = strApiKey

    params = urllib.urlencode(data)
    # print(params)

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
        print('HTTP request error (status %d)' % code)
        if code != 500: return None

        storeList = []
        storeInfo = {}
        storeInfo['name'] = '500error'
        storeList += [storeInfo]
        return storeList
        #return None

    response = result.read()
    #print(response)        # for debugging
    #tree = html.fromstring(response)
    root = ElementTree.fromstring(response)

    storeList = []

    for child in root.iter('row'):
        storeInfo = {}
        storeInfo['name'] = ''
        storeInfo['pn'] = ''
        storeInfo['addr'] = ''
        storeInfo['newaddr'] = ''
        storeInfo['status'] = ''
        storeInfo['status2'] = ''
        storeInfo['cat1'] = ''
        storeInfo['cat2'] = ''
        storeInfo['size'] = ''
        storeInfo['since'] = ''
        storeInfo['closed'] = ''
        storeInfo['year'] = ''
        storeInfo['feat'] = ''
        storeInfo['xcoord'] = ''
        storeInfo['ycoord'] = ''

        for infoitem in child:

            if infoitem.tag == 'bplcNm':
                storeInfo['name'] = infoitem.text
            elif infoitem.tag == 'siteTel':
                strtemp = infoitem.text
                #if strtemp != None: storeInfo['pn'] = strtemp.replace('  ', ' ').replace('  ', '').replace(' ', '-')
                if strtemp != None: storeInfo['pn'] = strtemp.replace(' ', '')
            elif infoitem.tag == 'siteWhlAddr':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['addr'] = strtemp
            elif infoitem.tag == 'rdnWhlAddr':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['newaddr'] = strtemp
            elif infoitem.tag == 'trdStateNm':
                storeInfo['status'] = infoitem.text
            elif infoitem.tag == 'dtlStateNm':
                storeInfo['status2'] = infoitem.text
            elif infoitem.tag == 'sntCobNm':
                storeInfo['cat1'] = infoitem.text
            elif infoitem.tag == 'sntUptaeNm':
                storeInfo['cat2'] = infoitem.text
            elif infoitem.tag == 'facilTotScp':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['size'] = strtemp
            elif infoitem.tag == 'apvPermYmd':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['since'] = strtemp
            elif infoitem.tag == 'dcbYmd':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['closed'] = strtemp
            elif infoitem.tag == 'yy':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['year'] = strtemp
            elif infoitem.tag == 'trdpJubnSeNm':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['feat'] = strtemp
            elif infoitem.tag == 'x':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['xcoord'] = strtemp.lstrip().rstrip()
            elif infoitem.tag == 'y':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['ycoord'] = strtemp.lstrip().rstrip()

        storeList += [storeInfo]

    delay_time = random.uniform(0.2, 0.4)
    time.sleep(delay_time)
    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
