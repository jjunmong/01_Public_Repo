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

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('nissan_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|SUBNAME2|ORGNAME|TELNUM|ADDR|NEWADDR|WEBSITE|XCOORD|YCOORD\n")

    page = 1
    while True:
        #store_list = getStores(page)
        store_list = getStores2(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['subname2'])
            outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 전체 점포 정보 모두 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores2(intPageNo):
    hdr = {
        ':authority': 'www.nissan.co.kr',
        ':method': 'GET',
        ':path': '/content/nissan_prod/ko_KR/index/dealer-finder/jcr:content/freeEditorial/contentzone_e70c/columns/columns12_df4d/col1-par/find_a_dealer_1b87.basic_dealers_by_location.json/page/1/_charset_/utf-8/size/-1/data.json',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',     # 'text/html,application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'cache-control': 'max-age=0',
        'adrum': 'isAjax:true',
        'cookie': 'X-Mapping-pjobmcgf=0854BDAA0B811B7898C1AB3E1C9D4B13; JSESSIONID=kt5uw3jwjbj7n1w0rfua1b78; AMCVS_0BCEE1CE543D41F50A4C98A5%40AdobeOrg=1; AMCV_0BCEE1CE543D41F50A4C98A5%40AdobeOrg=-1176276602%7CMCIDTS%7C17359%7CMCMID%7C61657170255089947471858775697928288324%7CMCAAMLH-1500050159%7C11%7CMCAAMB-1500367614%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1499770014s%7CNONE%7CMCAID%7C2C05BEDD052A14E3-400001068003A356; aam_uuid=61887469355869966141853350946988169081; satNavigation=ëì° ì ìì¥|https://www.nissan.co.kr/dealer-finder.html|Homepage|nav global; ADRUM=s=1499763019545&r=https%3A%2F%2Fwww.nissan.co.kr%2F%3F0; gpv_pn=dealer-finder; s_ppvl=Homepage%2C33%2C24%2C873%2C1175%2C873%2C2560%2C1440%2C1%2CP; s_ppv=dealer-finder%2C71%2C71%2C873%2C1175%2C873%2C2560%2C1440%2C1%2CP; visitorID=61657170255089947471858775697928288324; s_sq=%5B%5BB%5D%5D; s_cc=true',
        'connection': 'keep-alive',
        #'Content-Length': '1004',
        #'Host': 'www.nissan.co.kr',
        #'if-modified-since': 'Fri, 14 Apr 2017 09:25:15 GMT',
        #'upgrade-insecure-requests': '1',
        #'Referer': 'https://www.nissan.co.kr/dealer-finder.html',
        #'Content-type': 'text/plain',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }


    try:
        urls = 'https://www.nissan.co.kr/dealer-finder.html'
        # 아래와 같이 호출하면 다 얻을 수 있음
        # urls = 'https://www.nissan.co.kr/content/nissan_prod/ko_KR/index/dealer-finder/jcr:content/freeEditorial/contentzone_e70c/columns/columns12_5fe8/col1-par/find_a_dealer_14d.extended_dealers_by_location.json/_charset_/utf-8/page/1/size/50/data.json'     # 더 이상 동작하지 않음 ㅠㅠ
        urls = 'https://www.nissan.co.kr/content/nissan_prod/ko_KR/index/dealer-finder/jcr:content/freeEditorial/contentzone_e70c/columns/columns12_df4d/col1-par/find_a_dealer_1b87.extended_dealers_by_location.json/_charset_/utf-8/page/1/size/30/data.json'    # 2017년 7월8일에 동작하는 url
        print(urls)
        #req = urllib2.Request(urls, None)
        #req = urllib2.Request(urls, None, headers=hdr)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)

        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)

    response_json = json.loads(response)

    entity_list = response_json['dealers']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'Nissan'
        subname = entity_list[i]['tradingName'].lstrip().rstrip()
        store_info['orgname'] = subname
        store_info['subname'] = '';     store_info['subname2'] = ''
        if subname.endswith('서비스센터'):
            subname = subname[:-5].rstrip()
            idx = subname.rfind(' ')
            store_info['subname2'] = subname[idx+1:]
            subname = subname.replace(store_info['subname2'], '').rstrip()
            subname += '서비스센터'
            store_info['subname'] = subname.replace(' ', '/')
        else:
            idx = subname.rfind(' ')
            store_info['subname2'] = subname[idx + 1:]
            subname = subname.replace(store_info['subname2'], '').rstrip()
            subname += '전시장'
            store_info['subname'] = subname.replace(' ', '/')

        store_info['addr'] = '';     store_info['newaddr'] = ''
        strtemp = entity_list[i]['address']['addressLine1']
        if strtemp != None:
            idx = strtemp.find('/')
            if idx != -1:
                store_info['newaddr'] = strtemp[:idx].rstrip()
                store_info['addr'] = strtemp[idx+1:].lstrip()
            else: store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = entity_list[i]['contact']['phone']
        if strtemp != None:
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['website'] = ''
        strtemp = entity_list[i]['contact']['website']
        if strtemp != None:
            store_info['website'] = strtemp

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['geolocation']['longitude']
        store_info['ycoord'] = entity_list[i]['geolocation']['latitude']

        store_list += [store_info]

    return store_list


# 아래 URL의 반환값에서 데이터 추출
# https://www.nissan.co.kr/content/nissan_prod/ko_KR/index/dealer-finder/jcr:content/freeEditorial/contentzone_e70c/columns/columns12_df4d/col1-par/find_a_dealer_1b87.extended_dealers_by_location.json/_charset_/utf-8/page/1/size/30/data.json
def getStores(intPageNo):
    response = '{"totalResults":37,"dealers":[{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"서울특별시 강남구 도산대로 168 / 서울특별시 강남구 논현동 7-3","postalCode":"06040"},"contact":{"phone":"(02)544-5010","website":"http://nissan-premier.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PMD0009","id":"kr_nissan_PMD0009","dealerId":"PMD0009","tradingName":"강남 프리미어오토모빌","geolocation":{"latitude":37.518985,"longitude":127.027033},"suggestedName":"강남 프리미어오토모빌","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"서울특별시 강서구 공항대로 345 / 서울특별시 강서구 등촌동 664-12","postalCode":"07590"},"contact":{"phone":"(02)6090-7200","website":"http://nissan-premier.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PMD0012","id":"kr_nissan_PMD0012","dealerId":"PMD0012","tradingName":"강서 프리미어오토모빌","geolocation":{"latitude":37.558254,"longitude":126.846087},"suggestedName":"강서 프리미어오토모빌","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"광주광역시 동구 독립로 286 / 광주광역시 동구 대인동 320-12","postalCode":"61426"},"contact":{"phone":"(062)221-7000","website":"http://www.nissan-prima.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PED0001","id":"kr_nissan_PED0001","dealerId":"PED0001","tradingName":"광주 프리마모터스","geolocation":{"latitude":35.156468,"longitude":126.913106},"suggestedName":"광주 프리마모터스","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"광주광역시 동구 독립로 286 / 광주광역시 동구 대인동 320-12","postalCode":"61426"},"contact":{"phone":"(062)221-7007","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PED0001S","id":"kr_nissan_PED0001S","dealerId":"PED0001S","tradingName":"광주 프리마모터스  서비스센터","geolocation":{"latitude":35.156246,"longitude":126.913162},"suggestedName":"광주 프리마모터스  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경북 구미시 1공단로 3길 95 / 경북 구미시 광평동 61-1","postalCode":"39365"},"contact":{"phone":"(054)462-1200","website":"http://www.nissan-sc.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SCD0002","id":"kr_nissan_SCD0002","dealerId":"SCD0002","tradingName":"구미 신창모터스","geolocation":{"latitude":36.110756,"longitude":128.36594},"suggestedName":"구미 신창모터스","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"대구광역시 서구 서대구로 63안길 13 / 대구광역시 서구 비산동 1825","postalCode":"41711"},"contact":{"phone":"(053)341-2700","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SCD0004","id":"kr_nissan_SCD0004","dealerId":"SCD0004","tradingName":"대구 서구 신창모터스  서비스센터","geolocation":{"latitude":35.88623,"longitude":128.555562},"suggestedName":"대구 서구 신창모터스  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"대구광역시 수성구 들안로 116 / 대구광역시 수성구 두산동 1-1","postalCode":"42169"},"contact":{"phone":"(053)710-2200","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SCD0002S","id":"kr_nissan_SCD0002S","dealerId":"SCD0002S","tradingName":"대구 수성 신창모터스  서비스센터","geolocation":{"latitude":35.840112,"longitude":128.617344},"suggestedName":"대구 수성 신창모터스  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"대구광역시 수성구 들안로 116 / 대구광역시 수성구 두산동 1-1","postalCode":"42169"},"contact":{"phone":"(053)710-2200","website":"http://www.nissan-sc.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SCD0001","id":"kr_nissan_SCD0001","dealerId":"SCD0001","tradingName":"대구 신창모터스","geolocation":{"latitude":35.84002,"longitude":128.617231},"suggestedName":"대구 신창모터스","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"대전광역시 동구 한밭대로 1261 /  대전광역시 동구 용전동 14-10","postalCode":"34539"},"contact":{"phone":"(042)823-0068","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"NED0001S","id":"kr_nissan_NED0001S","dealerId":"NED0001S","tradingName":"대전  서비스 지정점","geolocation":{"latitude":36.3557863,"longitude":127.43700369999999},"suggestedName":"대전  서비스 지정점","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"부산광역시 수영구 수영로 449 / 부산광역시 수영구 남천동 55-22","postalCode":"48264"},"contact":{"phone":"(051)780-2300","website":"http://www.nissan-sb.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SBD0002","id":"kr_nissan_SBD0002","dealerId":"SBD0002","tradingName":"부산 에쓰비모터스","geolocation":{"latitude":35.14607,"longitude":129.109606},"suggestedName":"부산 에쓰비모터스","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"부산광역시 남구 우암로 375 / 부산광역시 남구 문현동 821","postalCode":"48475"},"contact":{"phone":"(051)780-2323","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SBD0003","id":"kr_nissan_SBD0003","dealerId":"SBD0003","tradingName":"부산 에쓰비모터스  서비스센터","geolocation":{"latitude":35.135707,"longitude":129.066623},"suggestedName":"부산 에쓰비모터스  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"인천광역시 부평구 장제로 336 / 인천광역시 부평구 삼산동 435-2","postalCode":"21323"},"contact":{"phone":"(032)328-7900","website":"http://nissan-premier.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PMD0008","id":"kr_nissan_PMD0008","dealerId":"PMD0008","tradingName":"부평 프리미어오토모빌","geolocation":{"latitude":37.515831,"longitude":126.732524},"suggestedName":"부평 프리미어오토모빌","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 성남시 분당구 서현로 247 / 경기도 성남시 분당구 서현동 81-1","postalCode":"13572"},"contact":{"phone":"(031)781-8004","website":"http://www.nissan-sn.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SND0001","id":"kr_nissan_SND0001","dealerId":"SND0001","tradingName":"분당 성남모터스","geolocation":{"latitude":37.384784,"longitude":127.12912},"suggestedName":"분당 성남모터스","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 성남시 분당구 탄천로 257 / 경기도 성남시 분당구 야탑동 403","postalCode":"13447"},"contact":{"phone":"(031)704-7712","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SND0004","id":"kr_nissan_SND0004","dealerId":"SND0004","tradingName":"분당 성남모터스  서비스센터","geolocation":{"latitude":37.414622,"longitude":127.119059},"suggestedName":"분당 성남모터스  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"서울시 서초구 반포대로 81 영림빌딩 1층 / 서울특별시 서초구 서초동 1538-5 영림빌딩 1층","postalCode":"06657"},"contact":{"phone":"(02)523-6400","website":"http://nissan-premier.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PMD0003","id":"kr_nissan_PMD0003","dealerId":"PMD0003","tradingName":"서초 프리미어오토모빌","geolocation":{"latitude":37.4875726,"longitude":127.00931850000006},"suggestedName":"서초 프리미어오토모빌","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"서울특별시 성동구 왕십리로 130(성수동1가) / 서울특별시 성동구 성수동 1가 656-53번지","postalCode":"04789"},"contact":{"phone":"(02)460-9999","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PMD0007","id":"kr_nissan_PMD0007","dealerId":"PMD0007","tradingName":"성수 프리미어오토모빌 서비스센터","geolocation":{"latitude":37.549177,"longitude":127.044845},"suggestedName":"성수 프리미어오토모빌 서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"인천광역시 연수구 해돋이로 157 / 인천광역시 연수구 송도동 22-8","postalCode":"22003"},"contact":{"phone":"(032)812-2323","website":"http://www.nissan-webon.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"WBD0001","id":"kr_nissan_WBD0001","dealerId":"WBD0001","tradingName":"송도 위본오토모빌","geolocation":{"latitude":37.394397,"longitude":126.645628},"suggestedName":"송도 위본오토모빌","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 용인시 기흥구 중부대로 305 / 경기도 용인시 기흥구 신갈동 451","postalCode":"17094"},"contact":{"phone":"(031)284-8005","website":"http://www.nissan-sn.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SND0003","id":"kr_nissan_SND0003","dealerId":"SND0003","tradingName":"수원 성남모터스","geolocation":{"latitude":37.270512,"longitude":127.100933},"suggestedName":"수원 성남모터스","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 용인시 기흥구 중부대로 305 / 경기도 용인시 기흥구 신갈동 451","postalCode":"17094"},"contact":{"phone":"(031)284-8010","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SND0003S","id":"kr_nissan_SND0003S","dealerId":"SND0003S","tradingName":"수원 성남모터스  서비스센터","geolocation":{"latitude":37.270567,"longitude":127.100954},"suggestedName":"수원 성남모터스  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 안양시 만안구 만안로 100 / 경기도 안양시 만안구 안양6동 538-4","postalCode":"14033"},"contact":{"phone":"(031)444-2000","website":"http://www.nissan-imotors.com/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"IMD0001","id":"kr_nissan_IMD0001","dealerId":"IMD0001","tradingName":"안양 아이모터스","geolocation":{"latitude":37.392242,"longitude":126.932155},"suggestedName":"안양 아이모터스","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 안양시 만안구 만안로 100 / 경기도 안양시 만안구 안양6동 538-4","postalCode":"14033"},"contact":{"phone":"(031)443-7777","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"IMD0001S","id":"kr_nissan_IMD0001S","dealerId":"IMD0001S","tradingName":"안양 아이모터스  서비스센터","geolocation":{"latitude":37.391874,"longitude":126.932017},"suggestedName":"안양 아이모터스  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 용인시 기흥구 동백중앙로 237 / 경기도 용인시 기흥구 중동 841","postalCode":"17006"},"contact":{"phone":"(031)679-0838","website":"http://www.nissan-sn.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"SND0002","id":"kr_nissan_SND0002","dealerId":"SND0002","tradingName":"용인 성남모터스","geolocation":{"latitude":37.274619,"longitude":127.150511},"suggestedName":"용인 성남모터스","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"강원도 원주시 치악로 1221-10 / 강원도 원주시 관설동 298-3","postalCode":"26468"},"contact":{"phone":"(033)763-1231","website":"http://thenissan.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"TPD0001","id":"kr_nissan_TPD0001","dealerId":"TPD0001","tradingName":"원주 더파크오토모빌","geolocation":{"latitude":37.296796,"longitude":127.991525},"suggestedName":"원주 더파크오토모빌","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"강원도 원주시 치악로 1221-10 / 강원도 원주시 관설동 298-3","postalCode":"26505"},"contact":{"phone":"(033)901-2323","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"TPD0001S","id":"kr_nissan_TPD0001S","dealerId":"TPD0001S","tradingName":"원주 더파크오토모빌  서비스센터","geolocation":{"latitude":37.29892,"longitude":127.983039},"suggestedName":"원주 더파크오토모빌  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"인천광역시 부평구 장제로 336 / 인천광역시 부평구 삼산동 435-2","postalCode":"21330"},"contact":{"phone":"(032)505-0330","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PMD0008S","id":"kr_nissan_PMD0008S","dealerId":"PMD0008S","tradingName":"인천 부평 프리미어오토모빌  서비스센터","geolocation":{"latitude":37.515472,"longitude":126.732471},"suggestedName":"인천 부평 프리미어오토모빌  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"인천광역시 중구 서해대로 186 / 인천광역시 중구 신흥동 50-5","postalCode":"22339"},"contact":{"phone":"(032)886-7114","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"WBD0001S","id":"kr_nissan_WBD0001S","dealerId":"WBD0001S","tradingName":"인천 중구 위본오토모빌 서비스센터","geolocation":{"latitude":37.444617,"longitude":126.62676},"suggestedName":"인천 중구 위본오토모빌 서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 고양시 일산동구 백마로 522 / 경기 고양시 일산동구 풍동 114-2","postalCode":"10300"},"contact":{"phone":"(031)810-1600","website":"http://nissan-premier.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PMD0002","id":"kr_nissan_PMD0002","dealerId":"PMD0002","tradingName":"일산 프리미어오토모빌","geolocation":{"latitude":37.663521,"longitude":126.805957},"suggestedName":"일산 프리미어오토모빌","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"경기도 고양시 일산동구 백마로 522 / 경기 고양시 일산동구 풍동 114-2","postalCode":"10300"},"contact":{"phone":"(031)919-3800","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"PMD0002S","id":"kr_nissan_PMD0002S","dealerId":"PMD0002S","tradingName":"일산 프리미어오토모빌  서비스센터","geolocation":{"latitude":37.663489,"longitude":126.805996},"suggestedName":"일산 프리미어오토모빌  서비스센터","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VO","serviceId":"VO","icon":"icon-car","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"전라북도 전주시 효자로 161 / 전라북도 전주시 완산구 효자동 3가 1693-5","postalCode":"54963"},"contact":{"phone":"(063)270-0000","website":"http://www.nissan-jsauto.co.kr/"},"dealerServices":[{"iconId":"icon-car","name":"딜러 전시장","openingHoursText":"","rank":"2"}],"actions":{"BOOK_A_TEST_DRIVE":true},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"JSD0001","id":"kr_nissan_JSD0001","dealerId":"JSD0001","tradingName":"전주  제이에스오토모빌","geolocation":{"latitude":35.819212,"longitude":127.102322},"suggestedName":"전주  제이에스오토모빌","markerStyle":""},{"country":"kr","servicesStructure":[{"_id":"kr_nissan_VE","serviceId":"VE","icon":"icon-configure","openingHoursLocalized":{"hasAfternoonHours":false}}],"address":{"addressLine1":"전라북도 전주시 완산구 쑥고개로 372 / 전라북도 전주시 완산구 효자동 2가 360-4","postalCode":"55079"},"contact":{"phone":"(063)270-0010","website":"-"},"dealerServices":[{"iconId":"icon-configure","name":"서비스 센터","openingHoursText":"","rank":"1"}],"actions":{},"averageStarRating":{"afterSales":{"title":"  "},"sales":{"title":"  "}},"openNow":false,"hasDealerWebsite":true,"urlId":"JSD0001S","id":"kr_nissan_JSD0001S","dealerId":"JSD0001S","tradingName":"전주  제이에스오토모빌  서비스센터","geolocation":{"latitude":35.803518,"longitude":127.105615},"suggestedName":"전주  제이에스오토모빌  서비스센터","markerStyle":""}]}'

    print(response)
    response_json = json.loads(response)

    entity_list = response_json['dealers']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = 'Nissan'
        subname = entity_list[i]['tradingName'].lstrip().rstrip()
        store_info['orgname'] = subname
        store_info['subname'] = '';     store_info['subname2'] = ''
        if subname.endswith('서비스센터'):
            subname = subname[:-5].rstrip()
            idx = subname.rfind(' ')
            store_info['subname2'] = subname[idx+1:]
            subname = subname.replace(store_info['subname2'], '').rstrip()
            subname += '서비스센터'
            store_info['subname'] = subname.replace(' ', '/')
        else:
            idx = subname.rfind(' ')
            store_info['subname2'] = subname[idx + 1:]
            subname = subname.replace(store_info['subname2'], '').rstrip()
            subname += '전시장'
            store_info['subname'] = subname.replace(' ', '/')

        store_info['addr'] = '';     store_info['newaddr'] = ''
        strtemp = entity_list[i]['address']['addressLine1']
        if strtemp != None:
            idx = strtemp.find('/')
            if idx != -1:
                store_info['newaddr'] = strtemp[:idx].rstrip()
                store_info['addr'] = strtemp[idx+1:].lstrip()
            else: store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = entity_list[i]['contact']['phone']
        if strtemp != None:
            if strtemp.startswith('('): strtemp = strtemp[1:]
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['website'] = ''
        strtemp = entity_list[i]['contact']['website']
        if strtemp != None:
            store_info['website'] = strtemp

        store_info['xcoord'] = ''; store_info['ycoord'] = ''
        store_info['xcoord'] = entity_list[i]['geolocation']['longitude']
        store_info['ycoord'] = entity_list[i]['geolocation']['latitude']

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
