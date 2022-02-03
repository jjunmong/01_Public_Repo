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

sidolist_all = {
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

sidolist = {
    '서울': {'종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구'},
    '광주': {''},
    '대구': {''},
    '대전': {''},
    '부산': {''},
    '울산': {''},
    '인천': {''},
    '경기': {''},
    '강원': {''},
    '경남': {''},
    '경북': {''},
    '전남': {''},
    '전북': {''},
    '제주': {''},
    '세종': {''},
    '충남': {''},
    '충북': {''},
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('coffeebean_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|OT@@커피빈\n")

    for sidoname in sorted(sidolist):

        gugunlist = sidolist[sidoname]

        for gugunname in sorted(gugunlist):

            storeList = getStores(sidoname, gugunname)    # 70개 이상 반환을 하지 않기 때문에 서울 주요 구의 경우 나눠서 호출해야 함
            print(sidoname, gugunname)
            if len(storeList) == 0:
                break

            for store in storeList:
                outfile.write("커피빈|")
                outfile.write(u'%s|' % store['StoreName'])
                outfile.write(u'%s|' % store['StoreTel'])
                outfile.write(u'%s|' % store['StoreAddress'])

                store_feat = ''
                if store['StoreParking'] == '1':
                    store_feat += '주차가능'
                if store['StoreDrive'] == '1':
                    if store_feat != '': store_feat += ';'
                    store_feat += '드라이브스루'
                if store['StoreWifi'] == '1':
                    if store_feat != '': store_feat += ';'
                    store_feat += 'WIFI'
                if store['Storesmoking'] == '1':
                    if store_feat != '': store_feat += ';'
                    store_feat += '흡연가능'
                # 케이크, 캡슐, 디카페인, 소이밀크 속성도 있음
                outfile.write(u'%s|' % store_feat)

                store_ot = store['StoreOpendate']
                store_ot = store_ot.replace('|', ';').replace(' ㅣ ', ';').replace('ㅣ', ';')
                outfile.write(u'%s\n' % store_ot)

            time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(areaName1, areaName2):
    url = 'http://www.coffeebeankorea.com'
    api = '/store/store_data2.asp'
    data = {
        'chk1': 0,
        'chk2': 0,
        'chk3': 0,
        'chk4': 0,
        'chk5': 0,
        'chk6': 0,
        'chk7': 0,
        'chk8': 0,
        'chk9': 0,
        'keyword': '',
        'lat': '',
        'lng': '',
        'storeNo': '',
    }
    data['StoreLocal'] = areaName1
    data['StoreLocal2'] = areaName2

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
    print(response)

    response = response.replace('\'', '"')
    response = response.replace('StoreNo :', '"StoreNo":')
    response = response.replace('StoreName :', '"StoreName":')
    response = response.replace('StoreTel :', '"StoreTel":')
    response = response.replace('StoreAddress :', '"StoreAddress":')
    response = response.replace('StoreOpendate :', '"StoreOpendate":')
    response = response.replace('StoreLAT :', '"StoreLAT":')
    response = response.replace('StoreLNG :', '"StoreLNG":')
    response = response.replace('StoreShortDesc :', '"StoreShortDesc":')
    response = response.replace('StoreEmail :', '"StoreEmail":')
    response = response.replace('StoreDecaffeine :', '"StoreDecaffeine":')
    response = response.replace('StoreSoymilk :', '"StoreSoymilk":')
    response = response.replace('StoreWifi :', '"StoreWifi":')
    response = response.replace('StoreParking :', '"StoreParking":')
    response = response.replace('Storesmoking :', '"Storesmoking":')
    response = response.replace('StoreMachine :', '"StoreMachine":')
    response = response.replace('StoreCapsule :', '"StoreCapsule":')
    response = response.replace('StoreCake :', '"StoreCake":')
    response = response.replace('StoreDrive :', '"StoreDrive":')
    # 2021년  3월 9일 딜리버리 항목이 추가
    response = response.replace('StoreDelivery :', '"StoreDelivery":')
    response = response.replace('Distant :', '"Distant":')
    response = response.replace('sort :', '"sort":')
    response = response.replace('StoreImage1 :', '"StoreImage1":')
    response = response.replace('StoreImage2 :', '"StoreImage2":')
    response = response.replace('StoreImage3 :', '"StoreImage3":')
    response = response.replace('StoreImage4 :', '"StoreImage4":')
    response = response.replace('StoreImage5 :', '"StoreImage5":')
    response = response.replace('StoreImage6 :', '"StoreImage6":')
    # 2022년 펫 추가
    response = response.replace('StorePet :', '"StorePet":')

    print(response)
    #tree = html.fromstring(response)
    storeList = json.loads(response)     # json 포맷으로 결과값 반환

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
