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

sidolist2 = {    # 오류처리용 목록
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
    '세종': {'세종'}
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('kookmin_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|CODE|XCOORD|YCOORD\n")

    for sido_name in sorted(sidolist):
        gugunlist = sidolist[sido_name]
        for gugun_name in sorted(gugunlist):

            page = 1
            retry_count = 0
            while True:
                store_list = getStores(gugun_name, page)
                if store_list == None:
                    if retry_count >= 7:
                        print('critical error!')
                        break
                    else:
                        time.sleep(random.uniform(1, 2))
                        retry_count += 1;   continue

                retry_count = 0

                for store in store_list:
                    if sido_name.endswith('남') or sido_name.endswith('북'): pass
                    elif not store['addr'].startswith(sido_name) or not store['newaddr'].startswith(sido_name): continue

                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['subname'])
                    outfile.write(u'%s|' % store['pn'])
                    outfile.write(u'%s|' % store['addr'])
                    outfile.write(u'%s|' % store['newaddr'])
                    outfile.write(u'%s|' % store['code'])
                    outfile.write(u'%s|' % store['xcoord'])
                    outfile.write(u'%s\n' % store['ycoord'])

                page += 1

                if page == 99: break
                elif len(store_list) < 10: break

                time.sleep(random.uniform(0.3, 0.9))

            time.sleep(random.uniform(0.5, 1.5))

        time.sleep(random.uniform(1, 2))

    outfile.close()


def getStores(sido_name, intPageNo):
    url = 'https://omoney.kbstar.com'
    api = '/quics?asfilecode=548565'

    data = {
        'searchtype': 'branch_road',
        'type05': 1,
        'type07': 0,
        'type08': 0,
        'type09': 0,
        'type10': 10,
        'type11': 'undefined',
        'type21': 0,
        'USER_TYPE': '03',
    }
    data['type01'] = intPageNo-1
    data['type04'] = sido_name
    params = urllib.urlencode(data)
    params = params.replace('%', '%25')     # '%'문자도 인코딩 ('%'를 인코딩하면 '%25'가 된다고 함
    print('%s : %d' % (sido_name, intPageNo-1))
    #print(params)

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
    response = unicode(response, 'euc-kr')
    #print(response)
    response = response.replace('list:', '"list":').replace('name:', '"name":').replace('code:', '"code":').replace(',tel:', ',"tel":').replace(',addr:', ',"addr":')
    response = response.replace(',addr2:', ',"addr2":').replace('road:', '"road":').replace('road2:', '"road2":').replace(',x:', ',"x":').replace(',y:', ',"y":').replace('num:', '"num":')
    response = response.replace('dist:', '"dist":').replace('brnFetr:', '"brnFetr":').replace('brnInfo:', '"brnInfo":')
    response = response.replace('wgsx:', '"wgsx":').replace('wgsy:', '"wgsy":').replace('brnInfo:', '"brnInfo":').replace('total:', '"total":')
    # 2017년 10월에 추가된 필드
    response = response.replace('startTime:', '"startTime":').replace('endTime:','"endTime":').replace('complexBankYN:','"complexBankYN":')
    # 2018년 3월에 추가된 필드
    response = response.replace('changGu:', '"changGu":')
    # 2018년 6월에 추가된 필드
    response = response.replace('park:', '"park":').replace('parkText:', '"parkText":').replace('counsel:', '"counsel":').replace('specialBranchYN:', '"specialBranchYN":')\
        .replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
    # 2021년 2월에 추가된 필드
    response = response.replace('frgnCrrATM:', '"frgnCrrATM":').replace('outAccYN:', '"outAccYN":').replace('gb:','"gb":')

    if response == '{result:true}':     # 검색결과가 없으면 이렇게 반환???
        print response
        return None

    response_json = json.loads(response)
    entity_list = response_json['list']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '국민은행'
        store_info['subname'] = ''
        strtemp = entity_list[i]['name']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.endswith('(출)'): strtemp = strtemp[:-3].rstrip() + '(출장소)'
            elif strtemp.endswith('센터'): pass
            elif strtemp.endswith('본점'): pass
            elif strtemp.endswith('(점)'): strtemp = strtemp[:-3] + '(출장소)'
            elif not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['road'].lstrip().rstrip() + ' ' + entity_list[i]['road2']
        store_info['addr'] = entity_list[i]['addr'].lstrip().rstrip() + ' ' + entity_list[i]['addr2']
        strtemp = entity_list[i]['addr2']
        store_info['code'] = entity_list[i]['code']
        store_info['xcoord'] = entity_list[i]['wgsx']
        store_info['ycoord'] = entity_list[i]['wgsy']

        store_info['pn'] = ''
        strtemp = entity_list[i]['tel']
        if strtemp != None:
            strtemp = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')
            store_info['pn'] = strtemp

        store_list += [store_info]

    return store_list


def convert_full_to_half_char(ch):
    codeval = ord(ch)
    if 0xFF00 <= codeval <= 0xFF5E:
        ascii = codeval - 0xFF00 + 0x20;
        return unichr(ascii)
    else:
        return ch


def convert_full_to_half_string(line):
    output_list = [convert_full_to_half_char(x) for x in line]
    return ''.join(output_list)


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
