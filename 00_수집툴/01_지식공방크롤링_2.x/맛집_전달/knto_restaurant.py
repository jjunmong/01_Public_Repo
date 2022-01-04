# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import codecs
import time
import random
import urllib
import urllib2
import json
from lxml import html

area = {
    '서울특별시': 'seoul',
}

area2 = {
    '서울특별시': 'seoul',
    '광주광역시': 'kwangju',
    '대구광역시': 'daegu',
    '대전광역시': 'daejeon',
    '부산광역시': 'busan',
    '울산광역시': 'ulsan',
    '인천광역시': 'incheon',
    '경기도': 'gyenggi',
    '강원도': 'gangwon',
    '경상남도': 'kyungnam',
    '경상북도': 'kyungbuk',
    '전라남도': 'jeonnam',
    '전라북도': 'jeonbuk',
    '충청남도': 'chungnam',
    '충청북도': 'chungbuk',
    '제주특별자치도': 'jeju',
    '세종특별자치시': 'sejong',
}

category = {
    '한식': 'F0101',
    '양식': 'F0102',
    '일식': 'F0103',
    '중식': 'F0104',
    '아시아식': 'F0105',
    '공연&식사': 'F0106',
    '공연&식사2': 'F0107',
    '채식': 'F0108',
    '카페&전통찻집': 'F0109'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('kto_restaurant_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|FEAT2|OT|OFFDAY|PARKING|ID|XCOORD|YCOORD|SOURCE2@@관광공사맛집\n")

    page = 1
    retry_count = 0
    while True:
        store_list = getStores(page)
        if store_list == None:
            if retry_count < 3: retry_count += 1;   continue
            else: break
        elif len(store_list) == 0: break
        retry_count = 0

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['feat2'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['offday'])
            outfile.write(u'%s|' % store['parking'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s|' % store['ycoord'])
            outfile.write(u'%s\n' % u'한국관광공사')

        page += 1

        if page == 999: break       # 2018년11월 기준 4707곳 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/11)
def getStores(intPageNo):
    url = 'https://korean.visitkorea.or.kr'
    api = '/call'

    data = {
        'cmd': 'TOUR_CONTENT_LIST_VIEW',
        'month': 'All',
        'areaCode': 'All',
        'sigunguCode' : 'All',
        'tagId': '11751b64-5bf9-44fa-90cd-e0e1b092caf6',   # 맛집
        'sortkind': '1',    # 최신순
        'locationx': '0',
        'locationy': '0',
        'cnt': '10',
    }

    data['page'] = intPageNo
    params = urllib.urlencode(data)
    #print(params)
    print('%d' % intPageNo)

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

    try:
        response_json = json.loads(response)
        entity_list = response_json['body']['result']
    except:
        print('return value error');     return None

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}
        store_info['name'] = ''
        store_info['subname'] = ''

        if entity_list[i].get('title'):
            store_info['name'] = entity_list[i]['title']

        store_info['id'] = ''
        if entity_list[i].get('cotId'):
            store_info['id'] = entity_list[i]['cotId']

        store_info['newaddr'] = ''
        if entity_list[i].get('addr1'):
            store_info['newaddr'] = entity_list[i]['addr1']

        store_info['feat'] = ''
        if entity_list[i].get('tagName'):
            store_info['feat'] = entity_list[i]['tagName'].replace('|', ';')

        store_info['pn'] = ''
        if entity_list[i].get('telNo'):
            store_info['pn'] = entity_list[i]['telNo'].replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

        store_info['ot'] = ''
        store_info['offday'] = ''
        store_info['parking'] = ''
        store_info['feat2'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        #store_list += [store_info]
        #continue

        suburl = 'https://korean.visitkorea.or.kr/call'
        subparams = 'cmd=TOUR_CONTENT_BODY_VIEW&cotid=' + store_info['id'] + '&locationx=0&locationy=0&stampId='

        try:
            time.sleep(random.uniform(0.2, 0.5))
            print(store_info['id'])
            subreq = urllib2.Request(suburl, subparams)
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the suburl');
            store_list += [store_info]; continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('suburl HTTP request error (status %d)' % subcode);
            store_list += [store_info];     continue

        subresponse = subresult.read()

        subresponse = json.loads(subresponse)
        info_list = subresponse['body']['article']

        if len(info_list) > 0:
            if info_list[0].get('useTime'):
                store_info['ot'] = info_list[0]['useTime']

            if info_list[0].get('restDate'):
                store_info['offday'] = info_list[0]['restDate']

            if info_list[0].get('firstMenu'):
                store_info['feat2'] = info_list[0]['firstMenu']

            if info_list[0].get('parking'):
                store_info['parking'] = info_list[0]['parking'].replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

            if info_list[0].get('mapX'):
                store_info['xcoord'] = info_list[0]['mapX']

            if info_list[0].get('mapY'):
                store_info['ycoord'] = info_list[0]['mapY']

            # 기타 정보도 있음 (갱신일 등등)

        store_list += [store_info]

    return store_list



'''
# v1,0
def getStores(catinfo, areacode, intPageNo):
    url = 'http://korean.visitkorea.or.kr'
    api = '/kor/bz15/food/food_list.jsp'

    data = {
        'listType': 'rdesc',
        'cid': '',
        'out_service': ''
    }
    data['category'] = catinfo
    data['areaCode'] = areacode
    data['gotoPage'] = intPageNo
    params = urllib.urlencode(data)
    #print(params)
    print('%s : %d' % (catinfo, intPageNo))

    try:
        #result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)
        result = urllib.urlopen(urls)
        #result = urllib.urlopen('http://www.caffebene.co.kr/Content/Gnb/Store/Map.aspx?&SearchValue=&gugun=&StoreName=&room=N&wifi=N&all=N&pc=N&book=N&store=N&Page=9&code=T5M2I2')
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)

    tableSelector = '//div[@class="whereWrap"]'

    nameSelector = '//div[@class="cnt"]/h3/b'
    svcInfoSelector = '//div[@class="cnt"]/ul/li'
    catSelector = '//div[@class="dc-restaurant-category"]'
    scoreInfoSelector = '//div[@class="dc-restaurant-stat-item-count"]'

    dataTable = tree.xpath(tableSelector)[0]
    names = dataTable.xpath(nameSelector)
    #tels = dataTable.xpath(telSelector)
    svcInfo = dataTable.xpath(svcInfoSelector)

    #suburlInfo = dataTable.xpath('//div[@class="whereWrap"]//a[contains(@href, "w_food_main_view.jsp")]/@href')
    suburlInfo = dataTable.xpath('//div[@class="whereWrap"]//ul//li/a/@href')

    storeList = []

    for i in range(len(names)):
        storeInfo = {}

        storeInfo['name'] = names[i].text or ''

        #strtemp = svcInfo[i*3 + 2].text or ''
        #idx = strtemp.find('대표메뉴 : ')
        #if (idx != -1): strtemp = strtemp[idx+7:]
        #storeInfo['features'] = strtemp
        #strtemp = svcInfo[i*3].text or ''
        #idx = strtemp.find('지역 : ')
        #if (idx != -1): strtemp = strtemp[idx+4:]
        #storeInfo['address'] = strtemp
        #strtemp = svcInfo[i*3 + 1].text or ''
        #idx = strtemp.find('전화번호 : ')
        #if (idx != -1): strtemp = strtemp[idx+7:]
        #storeInfo['telephone'] = strtemp

        storeInfo['feat1'] = ''
        storeInfo['feat2'] = ''
        storeInfo['feat3'] = ''
        storeInfo['feat4'] = ''
        storeInfo['feat5'] = ''
        storeInfo['feat6'] = ''
        storeInfo['feat7'] = ''
        storeInfo['feat8'] = ''
        storeInfo['feat9'] = ''
        storeInfo['feat10'] = ''

        suburl = suburlInfo[i]

        if suburl != "":
            final_suburl = ''
            if suburl.startswith('http'): final_suburl = suburl
            else: final_suburl = url + '/kor/bz15/food/' + suburl

            try:
                time.sleep(random.uniform(0.3, 0.9))
                print(final_suburl)
                subresult = urllib.urlopen(final_suburl)
            except:
                print('Error calling the suburl');      continue

            subcode = subresult.getcode()
            if subcode != 200:
                print('suburl HTTP request error (status %d)' % subcode);   continue

            subresponse = subresult.read()
            subtree = html.fromstring(subresponse)

            subtableSelector = '//div[@class="doc"]'
            shopInfoTitleSelector = '//figcaption/ul/li/b'
            shopInfoDataSelector = '//figcaption/ul/li/span'

            if len(subtree.xpath(subtableSelector)) > 0:
                subdataTable = subtree.xpath(subtableSelector)[0]
                shopInfoTitleList = subdataTable.xpath(shopInfoTitleSelector)
                shopInfoDataList = subdataTable.xpath(shopInfoDataSelector)

                for j in range(len(shopInfoTitleList)):
                    title = shopInfoTitleList[j].text
                    if (title == "위치"): storeInfo['feat1'] = shopInfoDataList[j].text.strip('\n\t\r')
                    elif (title == "문의/안내"):
                        strtemp = "".join(shopInfoDataList[j].itertext())
                        if strtemp != None:
                            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                            if strtemp[0] >= '0' and strtemp[0] <= '9': pass
                            else:
                                idx = strtemp.find(' ')
                                if idx != -1:
                                    strtemp = strtemp[idx+1:].lstrip()
                                    if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()

                            storeInfo['feat2'] = strtemp
                    elif (title == "대표메뉴"): storeInfo['feat3'] = shopInfoDataList[j].text.strip('\n\t\r')
                    elif (title == "영업시간"): storeInfo['feat4'] = shopInfoDataList[j].text.strip('\n\t\r')
                    elif (title == "쉬는날"): storeInfo['feat5'] = shopInfoDataList[j].text.strip('\n\t\r')
                    elif (title == "좌석수"): storeInfo['feat6'] = shopInfoDataList[j].text.strip('\n\t\r')

                shopDetailInfoTitleSelector = '//div[@id="con_sect"]//div[@id="group1"]/ul/li/em'
                shopDetailInfoDataSelector = '//div[@id="con_sect"]//div[@id="group1"]/ul/li'
                shopDetailInfoTitleList = subdataTable.xpath(shopDetailInfoTitleSelector)
                shopDetailInfoDataList =  subdataTable.xpath(shopDetailInfoDataSelector)
                for j in range(len(shopDetailInfoTitleList)):
                    title = shopDetailInfoTitleList[j].text
                    title = title.replace(' ', '')
                    if (title == "개업일"):
                        #storeInfo['feat7'] = shopDetailInfoDataList[j].tail
                        storeInfo['feat7'] = "".join(shopDetailInfoDataList[j].itertext())
                        storeInfo['feat7'] = storeInfo['feat7'].strip('\n\t\r')
                    elif (title == "관련홈페이지"):
                        #storeInfo['feat8'] = shopDetailInfoDataList[j].tail
                        strtemp = "".join(shopDetailInfoDataList[j].itertext())
                        idx = strtemp.find('http')
                        if (idx != -1): strtemp = strtemp[idx:]
                        storeInfo['feat8'] = strtemp.strip('\n\t\r')

                shopDetailInfoTitleSelector = '//div[@id="con_sect"]//div[@id="group4"]/ul/li/em'
                shopDetailInfoDataSelector = '//div[@id="con_sect"]//div[@id="group4"]/ul/li'
                shopDetailInfoTitleList = subdataTable.xpath(shopDetailInfoTitleSelector)
                shopDetailInfoDataList =  subdataTable.xpath(shopDetailInfoDataSelector)
                for j in range(len(shopDetailInfoTitleList)):
                    title = shopDetailInfoTitleList[j].text
                    title = title.replace(' ', '')
                    if (title == "취급메뉴"):
                        #storeInfo['feat9'] = shopDetailInfoDataList[j].tail
                        strtemp = "".join(shopDetailInfoDataList[j].itertext())
                        strtemp = strtemp.replace('\r', '').replace("\n", '')
                        strtemp = '_'.join(strtemp.split())
                        strtemp = strtemp.replace('_', ' ')
                        idx = strtemp.find('메뉴 구성')
                        if(idx != -1): strtemp = strtemp[:idx-1]
                        idx = strtemp.find('자세한 메뉴')
                        if(idx != -1): strtemp = strtemp[:idx-1]
                        idx = strtemp.find('취급메뉴')
                        if(idx != -1): strtemp = strtemp[idx+4:]
                        storeInfo['feat9'] = strtemp.strip('\n\t\r')
                    elif (title == "외국인선호추천메뉴"):
                        #storeInfo['feat10'] = shopDetailInfoDataList[j].tail
                        strtemp = "".join(shopDetailInfoDataList[j].itertext())
                        strtemp = strtemp.replace('\r', '').replace("\n", '')
                        strtemp = '_'.join(strtemp.split())
                        strtemp = strtemp.replace('_', ' ')
                        idx = strtemp.find('추천메뉴')
                        if(idx != -1): strtemp = strtemp[idx+4:]
                        storeInfo['feat10'] = strtemp.strip('\n\t\r')
            else:   # 페이지 포맷이 다른 경우...
                subinfo_list = subtree.xpath('//div[@class="useinfo"]//ul//li')

                for j in range(len(subinfo_list)):
                    tag_list = subinfo_list[j].xpath('.//strong')
                    value_list = subinfo_list[j].xpath('.//span')

                    if len(tag_list) < 1 or len(value_list) < 1: continue

                    tag = "".join(tag_list[0].itertext())
                    value = "".join(value_list[0].itertext())

                    if tag == None or value == None: continue

                    tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                    value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', ' ')

                    if tag == '위치':
                        storeInfo['feat1'] = value
                    elif tag == '연락처':
                        storeInfo['feat2'] = value
                    elif tag == '휴무일' or tag == '휴뮤일' :
                        storeInfo['feat5'] = value
                    elif tag == '취급메뉴':
                        storeInfo['feat3'] = value

        storeList += [storeInfo]

    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
