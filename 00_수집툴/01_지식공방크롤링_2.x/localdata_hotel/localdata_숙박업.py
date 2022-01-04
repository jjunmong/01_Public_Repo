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
    '/platform/rest/16_03_01_P/openApi': 'vtok6WintJI2UhgqF2c5n=cjJwAB8APrHD4dtPPtzYo=',    #관광숙박업
    '/platform/rest/41_43_01_P/openApi': 'd=aXyg77iLI0jA0quG7XRBC36j63wwXrXzxcVOtuY2o=',    #숙박업
    '/platform/rest/41_16_01_P/openApi': 'ScR=eqT=OwHyvFQdxVa/5uHEDVzC=ezycR01nXa5N/c=',    #숙박업(일반-여관업)
    '/platform/rest/41_13_01_P/openApi': 'Rl3FCFcwC8bQtIKOkgGQkry=MD=PSsG45DfG6B/7a/M=',    #숙박업(일반)(관광호텔)
    '/platform/rest/41_15_01_P/openApi': '5Btljk0UOOtiWW3bCco=i0qmmWd5Z=H=XL5ICjSGNgI=',    #숙박업(일반-휴양콘도미니엄업)
    '/platform/rest/41_14_01_P/openApi': '5ieRltn/NkhsB9QhthAf2iphQjw6iU=lKygPbXvKiiw=',    #숙박업(일반-일반호텔)
    '/platform/rest/41_17_01_P/openApi': '2krp8tFvRVEavjg6HkQXH8V7/1zxQ25UcBFDiO/CJQM=',    #숙박업(일반-여인숙업)
    '/platform/rest/16_19_01_P/openApi': 'SIVs4rdTsBrQGZ81fBGYDz68CZ/GllV6WJcIYfJKbPM=',    #관광펜션업
    '/platform/rest/16_24_01_P/openApi': 'kKHJYYtQZ7o78v6WHMKNSbavhMuBNtS9uGte5r47H3M=',    #외국인관광도시민박업
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('localdata_hotel_utf8.txt', 'w', 'utf-8')
    outfile.write("##NEWADDR|NAME|ENAME|TYPE|TELNUM|ADDR|STATUS|STATUS2|CAT1|CAT2|SIZE|TROOM|ROOM1|ROOM2|SINCE|CLOSED|YEAR|FEAT|BUSAGE|LUSAGE|LUSAGE2|X|Y@@TAXHOTEL\n")
    #outfile.write("##NAME|ENAME|TYPE|TELNUM|ADDR|NEWADDR|STATUS|STATUS2|CAT1|CAT2|SIZE|TROOM|ROOM1|ROOM2|SINCE|CLOSED|YEAR|FEAT|BUSAGE|LUSAGE|LUSAGE2|X|Y@@TAXHOTEL\n")

    for api_item in sorted(api_dict):
        hotel_type = ''
        if api_item == '/platform/rest/16_03_01_P/openApi': hotel_type = '관광숙박업'
        elif api_item == '/platform/rest/41_43_01_P/openApi': hotel_type = '숙박업'
        elif api_item == '/platform/rest/41_16_01_P/openApi': hotel_type = '여관업'
        elif api_item == '/platform/rest/41_13_01_P/openApi': hotel_type = '관광호텔'
        elif api_item == '/platform/rest/41_15_01_P/openApi': hotel_type = '휴양콘도미니엄업'
        elif api_item == '/platform/rest/41_14_01_P/openApi': hotel_type = '일반호텔'
        elif api_item == '/platform/rest/41_17_01_P/openApi': hotel_type = '여인숙업'
        elif api_item == '/platform/rest/16_19_01_P/openApi': hotel_type = '관광펜션업'
        elif api_item == '/platform/rest/16_24_01_P/openApi': hotel_type = '외국인관광도시민박업'

        page = 1
        while True:
            storeList = getStores(api_item, api_dict[api_item], page)
            if storeList == None: break;
            elif len(storeList) == 0: break
            elif len(storeList) == 1:
                if storeList[0]['name'] == '500error':
                    continue

            for store in storeList:
                if store['status'].find('폐업') != -1: continue  # 영업중인 것만 인쇄

                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['ename'])
                outfile.write(u'%s|' % hotel_type)
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                #outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['status'])
                outfile.write(u'%s|' % store['status2'])
                outfile.write(u'%s|' % store['cat1'])
                outfile.write(u'%s|' % store['cat2'])
                outfile.write(u'%s|' % store['size'])
                outfile.write(u'%s|' % store['room_total'])
                outfile.write(u'%s|' % store['room1'])
                outfile.write(u'%s|' % store['room2'])
                outfile.write(u'%s|' % store['since'])
                outfile.write(u'%s|' % store['closed'])
                outfile.write(u'%s|' % store['year'])
                outfile.write(u'%s|' % store['feat'])
                outfile.write(u'%s|' % store['b_usage'])
                outfile.write(u'%s|' % store['l_usage'])
                outfile.write(u'%s|' % store['l_usage2'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 299:
                break

    outfile.close()

def getStores(strApi, strApiKey, intPageNo):
    url = 'http://www.localdata.kr'
    api = strApi
    data = {
        'pageSize': 500,
        #'bgnYmd': '20180501',       # 시작일자(YYYYMMDD)
        #'endYmd': '20180531',       # 종료일자(YYYYMMDD)
        'state': '01',      # 운영상태코드 01:운영/02:휴업/03:폐업
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
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        storeList = []
        storeInfo = {}
        storeInfo['name'] = '500error'
        storeList += [storeInfo]
        return storeList
        #return None

    response = result.read()
    #response = '<?xml version="1.0" encoding="utf-8"?><lists><total><page>185</page></total><item>	<s_num><![CDATA[1721]]></s_num>	<menu_id><![CDATA[2]]></menu_id>	<s_name><![CDATA[가락부대점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 송파구 가락동 79-3 대동빌딩1층]]></s_address2>	<s_address3><![CDATA[서울 송파구 가락동 79-3 대동빌딩1층]]></s_address3>	<naver_address><![CDATA[서울 송파구 가락동 79-3 대동빌딩1층]]></naver_address>	<s_tel><![CDATA[02-443-8088]]></s_tel>	<s_reserve><![CDATA[가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[불가능]]></s_holiday>	<s_park><![CDATA[가능]]></s_park>	<menu_name><![CDATA[부대찌개&철판구이]]></menu_name>	<s_time><![CDATA[10:00 - 22:00]]></s_time></item><item>	<s_num><![CDATA[20665]]></s_num>	<menu_id><![CDATA[1]]></menu_id>	<s_name><![CDATA[가락쌍용프라자보쌈점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 송파구 가락동 140]]></s_address2>	<s_address3><![CDATA[서울 송파구 가락동 140]]></s_address3>	<naver_address><![CDATA[서울특별시 송파구 가락동 140]]></naver_address>	<s_tel><![CDATA[02-400-4745]]></s_tel>	<s_reserve><![CDATA[가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[가능]]></s_holiday>	<s_park><![CDATA[가능]]></s_park>	<menu_name><![CDATA[놀부보쌈]]></menu_name>	<s_time><![CDATA[11:00 - 22:00]]></s_time></item><item>	<s_num><![CDATA[20695]]></s_num>	<menu_id><![CDATA[6]]></menu_id>	<s_name><![CDATA[가락쌍용프라자유황오리점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 송파구 가락동 140번지 [서울 송...]]></s_address2>	<s_address3><![CDATA[서울 송파구 가락동 140번지 [서울 송파구 동남로 189 쌍용프라자 224호]]></s_address3>	<naver_address><![CDATA[서울특별시 송파구 가락동 140]]></naver_address>	<s_tel><![CDATA[02-400-4745]]></s_tel>	<s_reserve><![CDATA[가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[가능]]></s_holiday>	<s_park><![CDATA[가능]]></s_park>	<menu_name><![CDATA[유황오리진흙구이]]></menu_name>	<s_time><![CDATA[11:00 - 22:00]]></s_time></item><item>	<s_num><![CDATA[504]]></s_num>	<menu_id><![CDATA[2]]></menu_id>	<s_name><![CDATA[가산2단지부대점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 금천구 가산동 60-19 SJ테크노...]]></s_address2>	<s_address3><![CDATA[서울 금천구 가산동 60-19 SJ테크노빌지하1층 142]]></s_address3>	<naver_address><![CDATA[서울금천구가산동60-19]]></naver_address>	<s_tel><![CDATA[02-3397-0977]]></s_tel>	<s_reserve><![CDATA[불가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[불가능]]></s_holiday>	<s_park><![CDATA[가능]]></s_park>	<menu_name><![CDATA[부대찌개&철판구이]]></menu_name>	<s_time><![CDATA[11:30 - 23:00]]></s_time></item><item>	<s_num><![CDATA[465]]></s_num>	<menu_id><![CDATA[2]]></menu_id>	<s_name><![CDATA[가산3단지부대점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 금천구 가산동 426-5 월드메르디...]]></s_address2>	<s_address3><![CDATA[서울 금천구 가산동 426-5 월드메르디앙벤처센타2차 102호]]></s_address3>	<naver_address><![CDATA[서울금천구가산동426-5]]></naver_address>	<s_tel><![CDATA[02-2025-8298]]></s_tel>	<s_reserve><![CDATA[불가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[불가능]]></s_holiday>	<s_park><![CDATA[불가능]]></s_park>	<menu_name><![CDATA[부대찌개&철판구이]]></menu_name>	<s_time><![CDATA[11:30 - 22:30]]></s_time></item></lists>'

    #response = '<?xml version="1.0" encoding="UTF-8"?><result><header>aaa</header><body><rows><row>aa</row><row>bb</row></rows></body></result>'
    #print(response)        # for debugging
    #tree = html.fromstring(response)
    #root = etree.fromstring(response)
    root = ElementTree.fromstring(response)
    #root = tree.getroot()

    storeList = []

    for child in root.iter('row'):
        storeInfo = {}
        storeInfo['name'] = ''
        storeInfo['ename'] = ''
        storeInfo['pn'] = ''
        storeInfo['addr'] = ''
        storeInfo['newaddr'] = ''
        storeInfo['status'] = ''
        storeInfo['status2'] = ''
        storeInfo['b_usage'] = ''
        storeInfo['l_usage'] = ''
        storeInfo['l_usage2'] = ''
        storeInfo['cat1'] = ''
        storeInfo['cat2'] = ''
        storeInfo['size'] = ''
        storeInfo['room_total'] = ''
        storeInfo['room1'] = ''
        storeInfo['room2'] = ''
        storeInfo['since'] = ''
        storeInfo['closed'] = ''
        storeInfo['year'] = ''
        storeInfo['feat'] = ''
        storeInfo['xcoord'] = ''
        storeInfo['ycoord'] = ''

        for infoitem in child:
            # print(child.tag, child.text)

            if infoitem.tag == 'bplcNm': storeInfo['name'] = infoitem.text
            elif infoitem.tag == 'engStnTrnmNm':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['ename'] = strtemp
            elif infoitem.tag == 'siteTel':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['pn'] = strtemp.replace('  ', ' ').replace('  ', '').replace(' ', '-')
            elif infoitem.tag == 'siteWhlAddr':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['addr'] = strtemp
            elif infoitem.tag == 'rdnWhlAddr':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['newaddr'] = strtemp
            elif infoitem.tag == 'trdStateNm': storeInfo['status'] = infoitem.text
            elif infoitem.tag == 'sntCobNm': storeInfo['cat1'] = infoitem.text
            elif infoitem.tag == 'sntUptaeNm': storeInfo['cat2'] = infoitem.text
            elif infoitem.tag == 'facilScp':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['size'] = strtemp
            elif infoitem.tag == 'stroomCnt':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['room_total'] = strtemp
            elif infoitem.tag == 'yangsilCnt':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['room1'] = strtemp
            elif infoitem.tag == 'hanshilCnt':
                strtemp = infoitem.text
                if strtemp != None: storeInfo['room2'] = strtemp
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
                storeInfo['feat'] = infoitem.text
            elif infoitem.tag == 'bdngSrvNm':
                strtemp = infoitem.text
                if strtemp != None:
                    strtemp = strtemp.replace('？', '').replace('?', '').replace(' ', '')
                    storeInfo['b_usage'] = strtemp
            elif infoitem.tag == 'nearEnvNm':
                strtemp = infoitem.text
                if strtemp != None:
                    strtemp = strtemp.replace('？', '').replace('?', '').replace(' ', '')
                    storeInfo['l_usage'] = strtemp
            elif infoitem.tag == 'regnSeNm':
                strtemp = infoitem.text
                if strtemp != None:
                    strtemp = strtemp.replace('？', '').replace('?', '').replace(' ', '')
                    storeInfo['l_usage2'] = strtemp
            elif infoitem.tag == 'dtlStateNm':
                storeInfo['status2'] = infoitem.text
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
