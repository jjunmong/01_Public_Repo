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
import json
import random
from lxml import html

sidolist2 = {
    '인천광역시': {'미추홀구'},
    '충청남도': {'당진시'},
}

sidolist = {
    '서울특별시': {'종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구'},
    '광주광역시': {'동구','서구','남구','북구','광산구'},
    '대구광역시': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전광역시': {'동구','중구','서구','유성구','대덕구'},
    '부산광역시': {'중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군'},
    '울산광역시': {'중구','남구','동구','북구','울주군'},
    #'인천광역시': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군'},
    '인천광역시': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군','남구'},
    '경기도': {'수원시','성남시','의정부시','안양시','부천시','광명시','평택시','동두천시','안산시','고양시','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군'},
    '강원도': {'춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군'},
    '경상남도': {'창원시','진주시','통영시','사천시','김해시','밀양시','거제시','양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군'},
    '경상북도': {'포항시','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군'},
    '전라남도': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완료도군','진도군','신안군'},
    '전라북도': {'전주시','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충청남도': {'천안시','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충청북도': {'청주시','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '제주특별자치도': {'제주시','서귀포시'},
    '세종시': {''}         # '세종특별자치시'만 '세종시'로 호출해야 함 ㅠㅠ
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('mrpizza_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|FEAT|ID|ETCADDR|KATECX|KATECY@@미스터피자\n")

    for sidoname in sorted(sidolist):
        storeList = getStores(sidoname, '')
        if storeList == None: continue

        for store in storeList:
            outfile.write(u'미스터피자|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['etcaddr'])
            outfile.write(u'%s|' % store['katecx'])
            outfile.write(u'%s\n' % store['katecy'])

        time.sleep(random.uniform(0.3, 0.9))
        continue    # 광역시도명으로만 호출해도 지점리스트 전부 얻을 수 있음

        gugunlist = sidolist[sidoname]      # 이렇게 호출하려면 시군구 리스트에서 '성남시'와 같은 하위에 구가 있는 시군구들을 '성남시 수정구', '성남시 분당구'와 같이 나눠야 한다.
        for gugunname in gugunlist:
            storeList = getStores(sidoname, gugunname)
            print(sidoname, gugunname)
            if storeList == None: continue

            for store in storeList:
                outfile.write(u'미스터피자|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s|' % store['feat'])
                outfile.write(u'%s\n' % store['etcaddr'])

            time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(sidoname, gugunname):
    url = 'http://www.mrpizza.co.kr'
    api = '/store/getGugunBranchList.json'
    data = {
        #'ScWord': ''
    }
    data['si'] = sidoname
    data['gu'] = gugunname
    params = urllib.urlencode(data)
    print(url + api + '?' + params)  # for debugging

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-kr,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive',
        #'Cookie': 'JSESSIONID=DBBE75A09FB6C761409B66573B6CA849; _ga=GA1.3.572484436.1481311150; wcs_bt=s_2f6be2a35c45:1482483708'
    }

    try:
        req = urllib2.Request(url+api, params, headers=hdr)    # POS 방식일 땐 이렇게 호출해야 함!!!
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    receivedData = json.loads(response)

    storeList = []

    agency_list_json = receivedData
    for i in range(len(agency_list_json)):
        agency = agency_list_json[i]
        branch_nm = agency['branch_nm']
        branch_id = agency['branch_id']
        coords = agency['coordinate']

        subdata = {}
        subdata['branch_id'] = branch_id
        subparams = urllib.urlencode(subdata)

        try:
            suburl = url + '/store/findStoreInfo.json'
            print(suburl + '?' + subparams)  # for debugging

            time.sleep(random.uniform(0.3, 0.9))
            subreq = urllib2.Request(suburl, subparams, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
            #subresult = urllib.urlopen(urls)
        except:
            print('Error calling the suburl');  continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);     continue

        subresponse = subresult.read()
        store_info_json = json.loads(subresponse)

        agency_list_json = receivedData
        for j in range(len(store_info_json)):
            store_detail = store_info_json[j]

            storeInfo = {}
            storeInfo['subname'] = store_detail['branch_nm'].replace(' ', '/')
            storeInfo['pn'] = store_detail['branch_tel1']

            storeInfo['addr'] = '';     storeInfo['newaddr'] = ''
            if store_detail['bunji'] != None:
                storeInfo['addr'] = store_detail['si'] + ' ' + store_detail['gu'] + ' ' + store_detail['dong'] + ' ' + store_detail['bunji']

            #if store_detail['building'] != None:
            #    storeInfo['newaddr'] = store_detail['si'] + ' ' + store_detail['gu'] + ' ' + store_detail['building']
            #    if store_detail['dong'] != None:
            #        storeInfo['newaddr'] += ' ('
            #        storeInfo['newaddr'] += store_detail['dong']
            #        storeInfo['newaddr'] += ')'

            storeInfo['newaddr'] = store_detail['addr_doro']

            storeInfo['etcaddr'] = store_detail['addr_append'].replace('\r', '').replace('\t', '').replace('\n', '')

            storeInfo['feat'] = ''
            if store_detail['isPack'] == 'Y':
                storeInfo['feat'] += '포장할인'

            if store_detail['isSal'] == 'Y':
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '샐러드바'

            if store_detail['isYoghury'] == 'Y':
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '요거트바'

            if store_detail['isParking'] == 'Y':
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '주차가능'

            if store_detail['isDelivery'] == 'Y':
                if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                storeInfo['feat'] += '배달'


            storeInfo['ot'] = ''
            if store_detail['day_shop_time'] != None:
                storeInfo['ot'] = '주중' + ' ' + store_detail['day_shop_time']

            if store_detail['week_shop_time'] != None:
                if storeInfo['ot'] != '': storeInfo['ot'] += ';'
                storeInfo['ot'] += '주말' + ' ' + store_detail['week_shop_time']

            storeInfo['id'] = store_detail['branch_id']
            storeInfo['coords'] = store_detail['coordinate']

            storeInfo['katecx'] = ''
            storeInfo['katecy'] = ''
            coord_list = storeInfo['coords'].split(',')
            if len(coord_list) == 2:
                storeInfo['katecx'] = coord_list[0]
                storeInfo['katecy'] = coord_list[1]

            storeList += [storeInfo]
            break       # 같은 내용이 2번 들어가 있는 경우가 있어서... ㅠㅠ

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
