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

brandcode_list = {
    u'본죽': 'BF101',
#    u'본도시락': 'BF104',
    u'본설': 'BF105',     # 본설렁탕
    u'본죽&비빔밥': 'BF102',
}

brandcode_list2 = {
    #u'본죽': 'BF101',
    u'본도시락': 'BF104',
    #u'본설': 'BF105',     # 본설렁탕
    #u'본죽&비빔밥': 'BF102',
}

brand_list = {
    u'본죽': '/bonJuk/store',
    u'본비빔밥': '/bonBibimbab/store',
    u'본설렁탕': '/bonSeolleongtang/store',
    u'본죽&비빔밥': '/bonCafe/store',
}

sido_list2 = {
    #'전남': {'완도군'},
    #'인천광역시': {'미추홀구'},
    #'충청남도': {'당진시'},
    '서울특별시': {'강남구'},
}

sido_list = {
    '서울특별시': {'종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구'},
    '광주광역시': {'동구','서구','남구','북구','광산구'},
    '대구광역시': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전광역시': {'동구','중구','서구','유성구','대덕구'},
    '부산광역시': {'중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군'},
    '울산광역시': {'중구','남구','동구','북구','울주군'},
    #'인천광역시': {'중구','동구', '남구','연수구','남동구','부평구','계양구','서구','강화군','옹진군'},
    '인천광역시': {'중구','동구', '미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군', '남구'},
    '경기도': {'수원시','성남시','의정부시','안양시','부천시','광명시','평택시','동두천시','안산시','고양시','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군'},
    '강원도': {'춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군'},
    '경상남도': {'창원시','진주시','통영시','사천시','김해시','밀양시','거제시','양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군'},
    '경상북도': {'포항시','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군'},
    '전라남도': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전라북도': {'전주시','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충청남도': {'천안시','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충청북도': {'청주시','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '제주특별자치도': {'제주시','서귀포시'},
    '세종특별자치시': {''}
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('bonjuk_utf8.txt', 'w', 'utf-8')      # 본죽
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|FEAT|OT|XCOORD|YCOORD@@본죽\n")

    #outfile = codecs.open('bondosirak_utf8.txt', 'w', 'utf-8')     # 본도시락
    #outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|FEAT|OT|XCOORD|YCOORD@@본도시락\n")

    for sido_name in sorted(sido_list):

        gugun_list = sido_list[sido_name]

        for gugun_name in sorted(gugun_list):

            for brand_name in brandcode_list:   # 본죽
            #for brand_name in brandcode_list2:   # 본도시락
                page = 1
                sentinel_id = 99999

                while True:
                    #store_list = getStores(sido_name, gugun_name, brand_name, brand_list[brand_name], page)

                    # 광역시도명으로만 호출해도 결과 반환
                    store_list = getStores3(sido_name, gugun_name, brand_name, brandcode_list[brand_name], page)    # 본죽
                    #store_list = getStores3(sido_name, gugun_name, brand_name, brandcode_list2[brand_name], page)    # 본도시락

                    if store_list == None: break;
                    elif len(store_list) < 1: break

                    # 끝에서 같은 결과값이 계속 반환되므로...
                    if store_list[0]['id'] == sentinel_id: break
                    sentinel_id = store_list[0]['id']

                    for store in store_list:
                        outfile.write(u'%s|' % store['name'])
                        outfile.write(u'%s|' % store['subname'])
                        outfile.write(u'%s|' % store['id'])
                        outfile.write(u'%s|' % store['pn'])
                        outfile.write(u'%s|' % store['newaddr'])
                        outfile.write(u'%s|' % store['feat'])
                        outfile.write(u'%s|' % store['ot'])
                        outfile.write(u'%s|' % store['xcoord'])
                        outfile.write(u'%s\n' % store['ycoord'])

                    page += 1

                    if page == 2: break     # 한번에 시군구내 모든 점포 반환
                    elif len(store_list) < 4: break
                    time.sleep(random.uniform(0.3, 0.9))

                time.sleep(random.uniform(0.3, 0.9))

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v3.0 (2019/1)
def getStores3(sido_name, gugun_name, brand_name, brand_code, intPageNo):
    # 'https://www.bonif.co.kr/store/listAjax'
    url = 'https://www.bonif.co.kr'
    api = '/store/listAjax'
    data = {
        'addr': '',
        'strIdx': '',
        'distance': '3',
        'selDiv': 'NOORDER',
        'schKey': '',
        'lat': '',
        'lng': '',
    }
    #data['sido'] = '서울특별시'
    #data['gugun'] = '서초구'
    #data['brdCd'] = 'BF101'
    data['sido'] = sido_name
    data['gugun'] = gugun_name
    data['brdCd'] = brand_code
    params = urllib.urlencode(data)
    print(sido_name+gugun_name+brand_name+params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.3.1475971607.1543986352; JSESSIONID=F85EF13946C4CD68F4D2377ED45E3FB2; AUTH=%7B%22idx%22%3Anull%2C%22name%22%3Anull%2C%22mobile%22%3Anull%2C%22email%22%3Anull%2C%22memberCd%22%3Anull%7D; _gid=GA1.3.99853357.1546748979',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        urls = url+api+'?'+params
        print(urls)
        result = urllib.urlopen(urls)

        #urls = url + api
        #req = urllib2.Request(urls, params, headers=hdr)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['data']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}
        store_info['name'] = entity_list[i]['brdNm'].lstrip().rstrip()
        store_info['subname'] = ''

        strtemp = entity_list[i]['strNm'].lstrip().rstrip()
        if strtemp == '': continue

        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip().replace('본 죽', '본죽')
            if strtemp.startswith('본죽&비빔밥cafe'):
                store_info['name'] = '본죽&비빔밥CAFE';
                strtemp = strtemp[10:].lstrip()
            elif strtemp.startswith('본죽&비빔밥'):
                store_info['name'] = '본죽&비빔밥';
                strtemp = strtemp[6:].lstrip()
            elif strtemp.startswith( store_info['name']):
                strtemp = strtemp[len( store_info['name']):].lstrip()

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['strCd']

        store_info['pn'] = ''
        if entity_list[i].get('telRep'):
            store_info['pn'] = entity_list[i]['telRep'].replace('(', '').replace(')', '-').lstrip().rstrip()

        store_info['newaddr'] = ''
        if entity_list[i].get('addr'):
            store_info['newaddr'] = entity_list[i]['addr']

        store_info['ot'] = ''
        if entity_list[i].get('workTm'):
            store_info['ot'] = entity_list[i]['workTm'].replace('\r', '').replace('\t', '').replace('\n', ' ').replace('  ', ' ').replace('  ', ' ').rstrip().lstrip()

        store_info['feat'] = ''
        if entity_list[i].get('service'):
            store_info['feat'] = entity_list[i]['service'].replace('\r', '').replace('\t', '').replace('\n', '').replace(',', ';').replace(' ', '').rstrip().lstrip()

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if entity_list[i].get('lng'):
            store_info['xcoord'] = entity_list[i]['lng']
        if entity_list[i].get('lat'):
            store_info['ycoord'] = entity_list[i]['lat']

        store_list += [store_info]

    return store_list

# v2.0
def getStores(sido_name, gugun_name, brand_name, requested_api, intPageNo):
    url = 'https://www.bonif.co.kr'
    #api = '/bonDosirak/store'
    api = requested_api
    data = {
        #'sido': '',
        #'gugun': '',
        'chainname': '',
        'lat': '',
        'lng': '',
        'flag': 'N',
    }
    data['sido'] = sido_name
    data['gugun'] = gugun_name
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    print(sido_name+gugun_name+brand_name+params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        urls = url + api
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="map_list"]//li')

    store_list = []
    for i in range(len(entity_list)):
        id_list = entity_list[i].xpath('./@idx')
        name_list = entity_list[i].xpath('.//strong[@class="name"]')
        addr_list = entity_list[i].xpath('.//p[@class="dsc"]')
        pn_list = entity_list[i].xpath('.//em[@class="phone"]')
        info_list = entity_list[i].xpath('.//td')

        if len(name_list) < 0: continue

        store_info = {}
        store_info['name'] = brand_name

        store_info['subname'] = ''
        store_info['addr'] = ''
        store_info['id'] = ''
        store_info['pn'] = ''

        strtemp = "".join(name_list[0].itertext()).strip('\r\t\n')
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip().replace('본 죽', '본죽')
            if strtemp.startswith('본죽&비빔밥cafe'):
                store_info['name'] = '본죽&비빔밥CAFE';
                strtemp = strtemp[10:].lstrip()
            elif strtemp.startswith('본죽&비빔밥'):
                store_info['name'] = '본죽&비빔밥';
                strtemp = strtemp[6:].lstrip()
            elif strtemp.startswith(brand_name):
                strtemp = strtemp[len(brand_name):].lstrip()

            store_info['subname'] = strtemp.replace(' ', '/')

        if len(id_list) > 0:
            store_info['id'] = id_list[0]

        if len(addr_list) > 0:
            strtemp = addr_list[0].text
            strtemp3 = "".join(addr_list[0].itertext()).strip('\r\t\n')
            if strtemp == None:
                strtemp = "".join(addr_list[0].itertext()).strip('\r\t\n')
            elif strtemp3 != None:
                strtemp3 = strtemp3.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                idx = strtemp3.find(strtemp)
                if idx != -1:
                    strtemp += ' ' + strtemp3[idx+len(strtemp):].lstrip()

            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                strtemp = strtemp.replace('101호', ' 101호').replace('102호', ' 102호').replace('103호', ' 103호').replace('104호', ' 104호').replace('105호', ' 105호').replace('  ', ' ').lstrip().rstrip()
                strtemp = strtemp.replace('1층', ' 1층').replace('2층', ' 2층').replace('3층', ' 3층').replace('  ', ' ').lstrip().rstrip()
                strtemp = strtemp.replace('1동', '1동 ').replace('2동', '2동 ').replace('3동', '3동 ').replace('4동', '4동 ').replace('5동', '5동 ').replace('  ', ' ').lstrip().rstrip()
                strtemp = strtemp.replace('6동', '6동 ').replace('7동', '7동 ').replace('8동', '8동 ').replace('9동', '9동 ').replace('0동', '0동 ').replace('  ', ' ').lstrip().rstrip()
                strtemp = strtemp.replace(' )', ')')
                temp_list = strtemp.split(' ')
                normalized_addr = ''
                for j in range(len(temp_list)):  # '751-10751-10' 이렇게 잘못 입력된 지번 데이터 처리
                    temp_item = temp_list[j]
                    idx = len(temp_item) / 2
                    if len(temp_item) >= 5 and temp_item[:idx] == temp_item[idx:]:
                        temp_item = temp_item[:idx]

                    if j != 0: normalized_addr += ' '
                    normalized_addr += temp_item

                store_info['addr'] = normalized_addr.replace('  ', ' ')


        if len(pn_list) > 0:
            strtemp = "".join(pn_list[0].itertext()).strip('\r\t\n')
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['pn'] = strtemp.replace('.', '-').replace(')', '-')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
