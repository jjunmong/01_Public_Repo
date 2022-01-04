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
import random
import json
from lxml import html


sido_list2 = {
    #'광주광역시': {'동구','서구','남구','북구','광산구'},
    #'세종특별자치시': {''},
    #'인천광역시': {'남구'},
    '충청북도': {'청주시 흥덕구','충주시'},
}

sido_list = {
    '서울특별시': {'종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구'},
    '광주광역시': {'동구','서구','남구','북구','광산구'},
    '대구광역시': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전광역시': {'동구','중구','서구','유성구','대덕구'},
    '부산광역시': {'중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군'},
    '울산광역시': {'중구','남구','동구','북구','울주군'},
    #'인천광역시': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군'},
    '인천광역시': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군','남구'},
    '경기도': {'수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구', '성남시 분당구','성남시 수정구','성남시 중원구','의정부시','안양시 동안구','안양시 만안구','부천시','광명시','평택시',
            '동두천시', '안산시 단원구','안산시 상록구','고양시 덕양구','고양시 일산서구','고양시 일산동구','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시',
            '용인시 기흥구','용인시 수지구','용인시 처인구','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군',
            '수원시', '성남시', '안양시', '안산시', '고양시', '용인시'},
    '강원도': {'춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군'},
    '경상남도': {'창원시 마산합포구','창원시 마산회원구','창원시 성산구','창원시 의창구','창원시 진해구','진주시','통영시','사천시','김해시','밀양시','거제시',
             '양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군',
             '창원시'},
    '경상북도': {'포항시 북구','포항시 남구','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군',
             '포항시'},
    '전라남도': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전라북도': {'전주시 덕진구','전주시 완산구','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군',
             '전주시'},
    '충청남도': {'천안시 서북구','천안시 동남구','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시',
             '천안시'},
    '충청북도': {'청주시 상당구','청주시 서원구','청주시 청원구','청주시 흥덕구','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군',
             '청주시'},
    '제주특별자치도': {'제주시','서귀포시'},
    #'세종특별자치시': {'세종특별자치시'},
    '세종특별자치시': {'세종특별자치시',''}
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('bokjiro3_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|FEAT|ID|TELNUM|NEWADDR|XCOORD|YCOORD@@복지서비스\n")

    for sido_name in sorted(sido_list):

        gugun_list = sido_list[sido_name]

        for gugun_name in sorted(gugun_list):

            page = 1
            while True:
                store_list = getStores(sido_name, gugun_name, page)
                if store_list == None: break;
                elif len(store_list) < 1: break

                for store in store_list:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['subname'])
                    outfile.write(u'%s|' % store['type'])
                    outfile.write(u'%s|' % store['id'])
                    outfile.write(u'%s|' % store['pn'])
                    outfile.write(u'%s|' % store['newaddr'])
                    outfile.write(u'%s|' % store['xcoord'])
                    outfile.write(u'%s\n' % store['ycoord'])

                page += 1

                if page == 99: break
                elif len(store_list) < 110: break
                time.sleep(random.uniform(0.3, 0.9))
                #break   # 한번 호출로 시군구내 정보 다 읽어옴

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()


def getStores(sido_name, gugun_name, intPageNo):
    # 'http://www.bokjiro.go.kr/nwel/welfareinfo/facinfo/egovCommSiSulDataAsynList.do'
    url = 'http://www.bokjiro.go.kr'
    api = '/nwel/welfareinfo/facinfo/egovCommSiSulDataAsynList.do'
    data = {}
    data['searchAddr'] = sido_name + ' ' + gugun_name
    data['siDo'] = sido_name
    data['siGunGu'] = gugun_name
    params = urllib.urlencode(data)
    #print(params)
    print(sido_name + ' ' + gugun_name + ' ' + str(intPageNo))

    # 복지시설
    params = 'selectedId=&wfcltId=&siSulGubun=&viewFaclLat=&viewFaclLng=&centerMovYnId=N&iTmp=&siPage=&errorFlag=false&initsearchGubun=&iPage=' + str(intPageNo) + '&userLng=&userLat=&userLocalNm=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C+%EA%B0%95%EB%82%A8%EA%B5%AC&mapLavel=4&topGubunShowBuf=0&searchFaclDivCd=welFacl&searchFaclNm=&searchDispsFaclY=&searchDispsFacl=&mapTypeId=1&searchAddr='\
             + urllib.quote(sido_name + ' ' + gugun_name) + '&userIpCurrentLng=127.0473774084&userIpCurrentLat=37.5173319259&returnUrl=%2Fnwel%2Fwelfareinfo%2Ffacinfo%2FegovFacInfoList.do&searchWelFacl0=0&_searchWelFacl0=on&searchWelFacl1=SB&_searchWelFacl1=on&searchWelFacl2=NY&_searchWelFacl2=on&searchWelFacl3=SJ&_searchWelFacl3=on&searchWelFaclSub0=0&_searchWelFaclSub0=on&searchWelFaclSub1=01&_searchWelFaclSub1=on&searchWelFaclSub2=02&_searchWelFaclSub2=on&searchWelFaclSub3=03&_searchWelFaclSub3=on&searchWelFaclSub4=04&_searchWelFaclSub4=on&searchWelFaclSub5=05&_searchWelFaclSub5=on&searchWelFaclSub6=06&_searchWelFaclSub6=on&searchWelFaclSub7=07&_searchWelFaclSub7=on&searchWelFaclSub8=08&_searchWelFaclSub8=on&searchWelFaclSub9=09&_searchWelFaclSub9=on&searchWelFaclSub10=14&_searchWelFaclSub10=on&searchWelFaclSub11=99&_searchWelFaclSub11=on&_searchEduFacl0=on&_searchEduFacl1=on&_searchEduFacl2=on&_searchPubAgenFacl0=on&_searchPubAgenFacl1=on&_searchPubAgenFacl2=on&_searchPubAgenFacl3=on&_searchPubAgenFacl4=on&_searchPubAgenFacl5=on&_searchHsptFacl0=on&_searchHsptFacl1=on&_searchHsptFacl2=on&_searchHsptFacl3=on&_searchHsptFacl4=on&_searchHsptFacl5=on&_searchHsptFacl6=on&_searchDispsFacl0=on&_searchDispsFacl1=on&_searchDispsFacl2=on&_searchDispsFacl3=on&_searchDispsFacl4=on&_searchDispsFacl5=on&searchGubun=1&banKyungVal=1&nowSiSulMyungUpMynDong=&siDo='\
             + urllib.quote(sido_name) + '&siGunGu=' + urllib.quote(gugun_name) + '&upMynDong=&siSulMyungUpMynDong=&roDeSiDo=&roDeSiGunGu=&roDeGuBun=&roDeMyung=&siSulMyungRoDe=&siSulMyungFull=&key1=list&stsfCn='

    # 공공기관
    params = 'selectedId=&wfcltId=&siSulGubun=&viewFaclLat=&viewFaclLng=&centerMovYnId=N&iTmp=&siPage=&errorFlag=false&initsearchGubun=&iPage=' + str(intPageNo) + '&userLng=&userLat=&userLocalNm=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C+%EA%B0%95%EB%82%A8%EA%B5%AC&mapLavel=4&topGubunShowBuf=0&searchFaclDivCd=pubAgenFacl&searchFaclNm=&searchDispsFaclY=&searchDispsFacl=&mapTypeId=1&searchAddr='\
             + urllib.quote(sido_name + ' ' + gugun_name) + '&userIpCurrentLng=127.0473774084&userIpCurrentLat=37.5173319259&returnUrl=%2Fnwel%2Fwelfareinfo%2Ffacinfo%2FegovFacInfoList.do&_searchWelFacl0=on&_searchWelFacl1=on&_searchWelFacl2=on&_searchWelFacl3=on&_searchWelFaclSub0=on&_searchWelFaclSub1=on&_searchWelFaclSub2=on&_searchWelFaclSub3=on&_searchWelFaclSub4=on&_searchWelFaclSub5=on&_searchWelFaclSub6=on&_searchWelFaclSub7=on&_searchWelFaclSub8=on&_searchWelFaclSub9=on&_searchWelFaclSub10=on&_searchWelFaclSub11=on&_searchEduFacl0=on&_searchEduFacl1=on&_searchEduFacl2=on&searchPubAgenFacl0=0&_searchPubAgenFacl0=on&searchPubAgenFacl1=JUM&_searchPubAgenFacl1=on&searchPubAgenFacl2=NPS&_searchPubAgenFacl2=on&searchPubAgenFacl3=NHI&_searchPubAgenFacl3=on&searchPubAgenFacl4=EI&_searchPubAgenFacl4=on&searchPubAgenFacl5=KCO&_searchPubAgenFacl5=on&_searchHsptFacl0=on&_searchHsptFacl1=on&_searchHsptFacl2=on&_searchHsptFacl3=on&_searchHsptFacl4=on&_searchHsptFacl5=on&_searchHsptFacl6=on&_searchDispsFacl0=on&_searchDispsFacl1=on&_searchDispsFacl2=on&_searchDispsFacl3=on&_searchDispsFacl4=on&_searchDispsFacl5=on&searchGubun=1&banKyungVal=1&nowSiSulMyungUpMynDong=&siDo='\
             + urllib.quote(sido_name) + '&siGunGu=' + urllib.quote(gugun_name) + '&upMynDong=&siSulMyungUpMynDong=&roDeSiDo=&roDeSiGunGu=&roDeGuBun=&roDeMyung=&siSulMyungRoDe=&siSulMyungFull=&key1=list&stsfCn='

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    entity_list = json.loads(response)
    print(len(entity_list))     # for debugging

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        strtemp = entity_list[i]['title_nm'].lstrip().rstrip()
        if strtemp == '': continue

        store_info['name'] = strtemp
        store_info['subname'] = ''

        store_info['id'] = ''
        if entity_list[i].get('wfcltId'):
            store_info['id'] = entity_list[i]['wfcltId']

        strtemp = entity_list[i]['fac_gb']
        if strtemp == 'JUM':
            store_info['type'] = '주민센터'
            if not store_info['name'].endswith('주민센터'): store_info['name'] += ' 주민센터'
        elif strtemp == 'NPS':
            store_info['type'] = '국민연금공단'
            store_info['subname'] = store_info['name']
            store_info['name'] = store_info['type']
        elif strtemp == 'KCO':
            store_info['type'] = '근로복지공단'
            store_info['subname'] = store_info['name']
            store_info['name'] = store_info['type']
        elif strtemp == 'NHI':
            store_info['type'] = '국민건강보험'
            store_info['subname'] = store_info['name']
            store_info['name'] = store_info['type']
        elif strtemp == 'EI':
            store_info['type'] = '고용보험공단'
            store_info['subname'] = store_info['name']
            store_info['name'] = store_info['type']
        else: store_info['type'] = strtemp

        store_info['pn'] = ''
        if entity_list[i].get('tel_no'):
            store_info['pn'] = entity_list[i]['tel_no'].replace('(', '').replace(')', '-').lstrip().rstrip()
        store_info['newaddr'] = ''
        if entity_list[i].get('addr_nm'):
            store_info['newaddr'] = entity_list[i]['addr_nm']
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if entity_list[i].get('addr_x'):
            store_info['xcoord'] = entity_list[i]['addr_x']
        if entity_list[i].get('addr_y'):
            store_info['ycoord'] = entity_list[i]['addr_y']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
