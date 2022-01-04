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
import json
from lxml import html

sidolist2 = {
    '충남': {'당진시'},
    '인천': {'미추홀구'},
}

sidolist = {
    '서울': {'종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구'},
    '광주': {'동구','서구','남구','북구','광산구'},
    '대구': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전': {'동구','중구','서구','유성구','대덕구'},
    '부산': {'중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군'},
    '울산': {'중구','남구','동구','북구','울주군'},
    #'인천': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군'},
    '인천': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군','남구'},
    '경기': {'수원시','성남시','의정부시','안양시','부천시','광명시','평택시','동두천시','안산시','고양시','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군'},
    '강원': {'춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군'},
    '경남': {'창원시','진주시','통영시','사천시','김해시','밀양시','거제시','양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군'},
    '경북': {'포항시','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군'},
    '전남': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전북': {'전주시','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충남': {'천안시','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충북': {'청주시','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '제주': {'제주시','서귀포시'},
    '세종': {''}
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('dunkin_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OTWD|OTWE|OT|OFFDATE|FEAT|FEAT2@@던킨도너츠\n")

    for sidoname in sorted(sidolist):

        gugunlist = sidolist[sidoname]

        count=0;
        for gugunname in sorted(gugunlist):

            storeList = getStores(sidoname, gugunname)
            if storeList == None:
                time.sleep(random.uniform(1, 2))
                storeList = getStores(sidoname, gugunname)
                if storeList == None:
                    #continue   # 한번만 더 확인하면 충분...
                    time.sleep(random.uniform(1, 2))
                    storeList = getStores(sidoname, gugunname)
                    if storeList == None:
                        continue

            for store in storeList:
                outfile.write(u'던킨도너츠|')
                strtemp = store['name']
                if not strtemp.endswith('점'): strtemp += '점'
                outfile.write(u'%s|' % strtemp)
                outfile.write(u'%s|' % store['tel'])

                strtemp = store['address']
                strtemp = strtemp.replace('&#40;', '(').replace('&#41;', ')')
                outfile.write(u'%s|' % strtemp)

                store_ot = ''
                store_ot1 = ''
                if store.get('operationtimeA'):
                    store_ot1 = store['operationtimeA'].replace('09&#5', 'AM').replace('18&#5', 'PM').replace(';', ':').replace(' ', '')
                    store_ot = '주중' +  store_ot1
                outfile.write(u'%s|' % store_ot1)
                store_ot2 = ''
                if store.get('operationtimeB'):
                    store_ot2 = store['operationtimeB'].replace('09&#5', 'AM').replace('18&#5', 'PM').replace(';', ':').replace(' ', '')
                    if store_ot != '': store_ot += ';'
                    store_ot += '주말' + store_ot2
                outfile.write(u'%s|' % store_ot2)
                outfile.write(u'%s|' % store_ot)

                store_offdate = ''
                if store.get('operationtimeC'): store_offdate = store['operationtimeC']
                outfile.write(u'%s|' % store_offdate)

                if store.get('serviceInfo'): svcList = store['serviceInfo']
                else: svcList = []

                store_svc = ''
                for i in range(len(svcList)):
                    if svcList[i]['name'] == None: continue
                    if (store_svc != ''): store_svc += ';'
                    store_svc += svcList[i]['name']
                outfile.write(u'%s|' % store_svc)

                if store.get('storeInfo'): itemList = store['storeInfo']
                else: itemList = []

                store_item = ''
                for i in range(len(itemList)):
                    if itemList[i]['name'] == None: continue
                    if (store_item != ''): store_item += ';'
                    store_item += itemList[i]['name']
                outfile.write(u'%s' % store_item)

                outfile.write(u'\n')

            time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(sidoname, gugunname):
    url = 'http://www.dunkindonuts.co.kr'
    api = '/store/list_ajax.php'
    data = {
        'ScWord': ''
    }
    data['ScS'] = sidoname
    data['ScG'] = gugunname

    params = urllib.urlencode(data)
    #print(params)

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
    #tree = html.fromstring(response)

    # 사이트 불안정...
    if response.find('"cnt"') == -1 or response.find('"default"') == -1:
        print('invalid return value')
        return None

    if response.find('"list"') == -1:
        print('invalid return value2')
        return None

    receivedData = json.loads(response)

    if receivedData.get('list'): storeList = receivedData['list']
    else: storeList = []

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
