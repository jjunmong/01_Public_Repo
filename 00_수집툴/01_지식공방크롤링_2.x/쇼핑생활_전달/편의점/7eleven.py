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
import urllib2
#import json
from lxml import html

area2 = {
     '제주특별자치도': '064'
}

area = {
    '서울': '02',
    '광주': '062',
    '대구': '053',
    '대전': '042',
    '부산': '051',
    '울산': '052',
    '인천': '032',
    '경기도': '031',
    '강원도': '033',
    '경상남도': '055',
    '경상북도': '054',
    '전라남도': '061',
    '전라북도': '063',
    '충청남도': '041',
    '충청북도': '043',
    '제주': '064',
    '세종': '044'
}

sidolist2 = {
    '충청남도': {'당진시'},
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
    '경기도': {'수원시','성남시','의정부시','안양시','부천시','광명시','평택시','동두천시','안산시','고양시','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군'},
    # 수원시, 성남시, 용인시 등 '구'가 있는 시의 경우 '구' 수준까지 지명을 제시하지 않아도 다 수집됨 ㅎㅎ
    #'경기도': {'수원시','성남시 분당구','성남시 수정구','성남시 중원구','의정부시','안양시','부천시','광명시','평택시','동두천시','안산시','고양시','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군'},
    '강원도': {'춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군'},
    '경상남도': {'창원시','진주시','통영시','사천시','김해시','밀양시','거제시','양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군'},
    '경상북도': {'포항시','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군'},
    '전라남도': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전라북도': {'전주시','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충청남도': {'천안시','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충청북도': {'청주시','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '제주도': {'제주시','서귀포시'},
    '세종': {''}
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('seveneleven_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|XCOORD|YCOORD@@세븐일레븐\n")

    for sidoname in sorted(sidolist):
        gugunlist = sidolist[sidoname]
        for gugunname in sorted(gugunlist):
            store_list = getStores2(sidoname, gugunname)

            if store_list == None: continue

            for store in store_list:
                outfile.write(u"세븐일레븐|")
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['feat'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

# v2.0 (2018/6)
def getStores2(sido_name, gugun_name):
    # 'http://www.7-eleven.co.kr/util/storeLayerPop.asp'
    url = 'http://www.7-eleven.co.kr'
    api = '/util/storeLayerPop.asp'

    data = {
        'hiddentext': 'none'
    }
    data['storeLaySido'] = sido_name
    data['storeLayGu'] = gugun_name
    params = urllib.urlencode(data)
    print('%s %s' % (sido_name, gugun_name))

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Accept-Encoding': 'deflate, br',   # gzip 옵션이 있으면 압축해서 결과를 반환하므로 gzip 옵션 제외함
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        #'Connection': 'keep-alive',
        #'cache-control': 'max-age=0',
        #'cookie': 's_fid=452EE41751587777-03FB2E9A6FACE93F; s_cc=true; WHATAP=x4nkofsbq9fdp; SCOUTER=x5pu4v0rk5s27k; JSESSIONID=BED4B3009FBD1A8DCD28A25EB6F00D21.lalavlashop-site; MOBILEYN=N; _ga=GA1.2.88744728.1528387772; _gid=GA1.2.2122373241.1528387772; __atssc=google%3B2; s_sq=gsretail-com-prd%3D%2526c.%2526a.%2526activitymap.%2526page%253DSTORE%25255E%2525EB%2525A7%2525A4%2525EC%25259E%2525A5%2525EA%2525B2%252580%2525EC%252583%252589%2526link%253D4%2526region%253DpagingTagBox%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DSTORE%25255E%2525EB%2525A7%2525A4%2525EC%25259E%2525A5%2525EA%2525B2%252580%2525EC%252583%252589%2526pidt%253D1%2526oid%253Dhttp%25253A%25252F%25252Flalavla.gsretail.com%25252Flalavla%25252Fko%25252Fmarket-info%252523%25253B%2526ot%253DA; AWSALB=Rx9EwfztniZ8qn0cRiadwWmzYqmL+gJVdbMbJmxPELrCe8rcK5M5ISh93101ozdfZm01pbT84FyG0bPhbuFX2qJRsSksJOh2a9jW9zZ+4a3se9vRu5XtbGnOUybg; __atuvc=10%7C23; __atuvs=5b1958bb83e6627b009',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)     # 이렇게 호출하지 않으면 'Error calling the API' 오류 발생
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
    #return response
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//div[@class="list_stroe"]//li')

    store_list = []
    for i in range(len(entity_list)):
        href_list = entity_list[i].xpath('.//a/@href')
        info_list = entity_list[i].xpath('.//span')

        if len(info_list) < 3: continue  # 최소 3개 필드 있어야 함

        store_info = {}

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('<img')
            if idx != -1: strtemp = strtemp[:idx].rstrip()
            store_info['subname'] = strtemp.replace(' ', '/').replace('-', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            strtemp = strtemp.replace('101,102호', ' 101,102호').replace('105,106호', ' 105,106호').lstrip().rstrip()
            strtemp = strtemp.replace('3,4호', ' 3,4호').lstrip().rstrip()
            strtemp = strtemp.replace('101~', ' 101~').replace('102~', ' 102~').replace('103~', ' 103~').replace('104~',' 104~').replace('105~', ' 105~').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('101호', ' 101호').replace('102호', ' 102호').replace('103호', ' 103호').replace('104호', ' 104호').replace('105호', ' 105호').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('106호', ' 106호').replace('107호', ' 107호').replace('108호', ' 108호').replace('109호', ' 109호').replace('110호', ' 110호').replace('  ', ' ').lstrip().rstrip()
            store_info['newaddr'] = strtemp.replace('1층', ' 1층').replace('2층', ' 2층').replace('1츠', ' 1층').replace('  ', ' ')

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None: store_info['pn'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').replace('.', '-').replace(')', '-')

        store_info['feat'] = ''
        feat_list = info_list[0].xpath('.//img/@alt')
        for j in range(len(feat_list)):
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_list[j]

        store_info['xcoord'] = '';    store_info['ycoord'] = ''
        if len(href_list) > 0:
            strtemp = href_list[0]
            idx = strtemp.find('markerClick(')
            if idx != -1:
                strtemp = strtemp[idx+12:].lstrip()
                idx = strtemp.find(')')
                if idx != -1:
                    temp_list = strtemp[:idx].split(',')
                    if len(temp_list) >= 3:
                        store_info['ycoord'] = temp_list[1]
                        store_info['xcoord'] = temp_list[2]

        store_list += [store_info]

    return store_list

# v1.0
def getStores(search_keyword):
    url = 'http://www.7-eleven.co.kr'
    api = '/util/storeLayerPop.asp'

    data = {
        'hiddentext': 'none'
    }
    data['storeText'] = search_keyword

    params = urllib.urlencode(data)
    print(params)

    try:
        #result = urllib.urlopen(url + api, params)

        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    #return response
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//div[@class="list_stroe"]//li')

    store_list = []
    for i in range(len(entity_list)):
        href_list = entity_list[i].xpath('.//a/@href')
        info_list = entity_list[i].xpath('.//span')

        if len(info_list) < 3: continue  # 최소 3개 필드 있어야 함

        store_info = {}

        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/').replace('-', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            strtemp = strtemp.replace('101,102호', ' 101,102호').replace('105,106호', ' 105,106호').lstrip().rstrip()
            strtemp = strtemp.replace('3,4호', ' 3,4호').lstrip().rstrip()
            strtemp = strtemp.replace('101~', ' 101~').replace('102~', ' 102~').replace('103~', ' 103~').replace('104~',' 104~').replace('105~', ' 105~').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('101호', ' 101호').replace('102호', ' 102호').replace('103호', ' 103호').replace('104호', ' 104호').replace('105호', ' 105호').replace('  ', ' ').lstrip().rstrip()
            strtemp = strtemp.replace('106호', ' 106호').replace('107호', ' 107호').replace('108호', ' 108호').replace('109호', ' 109호').replace('110호', ' 110호').replace('  ', ' ').lstrip().rstrip()
            store_info['newaddr'] = strtemp.replace('1층', ' 1층').replace('2층', ' 2층').replace('1츠', ' 1층').replace('  ', ' ')

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None: store_info['pn'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').replace('.', '-').replace(')', '-')

        store_info['feat'] = ''
        feat_list = info_list[0].xpath('.//img/@alt')
        for j in range(len(feat_list)):
            if store_info['feat'] != '': store_info['feat'] += ';'
            store_info['feat'] += feat_list[j]

        store_info['xcoord'] = '';    store_info['ycoord'] = ''
        if len(href_list) > 0:
            strtemp = href_list[0]
            idx = strtemp.find('markerClick(')
            if idx != -1:
                strtemp = strtemp[idx+12:].lstrip()
                idx = strtemp.find(')')
                if idx != -1:
                    temp_list = strtemp[:idx].split(',')
                    if len(temp_list) >= 3:
                        store_info['ycoord'] = temp_list[1]
                        store_info['xcoord'] = temp_list[2]

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
