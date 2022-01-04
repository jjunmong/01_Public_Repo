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
import json
from lxml import html

sido_list2 = {
    '인천': {'미추홀구'},
    '충남': {'당진시'},
}

sido_list = {
    '서울': {'종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구'},
    '광주': {'동구','서구','남구','북구','광산구'},
    '대구': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전': {'동구','중구','서구','유성구','대덕구'},
    '부산': {'중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군'},
    '울산': {'중구','남구','동구','북구','울주군'},
    #'인천': {'중구','동구','남구','연수구','남동구','부평구','계양구','서구','강화군','옹진군'},
    '인천': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군','남구'},
    '경기': {'수원시','성남시','의정부시','안양시','부천시','광명시','평택시','동두천시','안산시','고양시','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군'},
    '강원': {'춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군'},
    '경남': {'창원시','진주시','통영시','사천시','김해시','밀양시','거제시','양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군'},
    '경북': {'포항시','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군'},
    '전남': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완료도군','진도군','신안군'},
    '전북': {'전주시','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충남': {'천안시','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충북': {'청주시','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '제주': {'제주시','서귀포시'},
    '세종': {'세종시'}
}

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('sinhyup_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|TYPE|XCOORD|YCOORD@@신용협동조합\n")

    for sido_name in sorted(sido_list):
        page = 1
        sentinel = 'xxxxxxxxxx';    tempaddr = ''
        while True:
            store_list = getStores(sido_name, page)
            print(store_list)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['type'])
                tempaddr = store['newaddr']
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 60: break
            elif len(store_list) < 4: break
            elif sentinel == tempaddr: break;

            sentinel = tempaddr     # 같은 주소가 반복되서 나타나면 break하려고, 페이지의 마지막 주소를 기록해 둠 (마지막 페이지 이후로도 계속 마지막 페이지의 내용을 반환해서...)

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

# v2.0 (2018/9)
def getStores(sido_name, intPageNo):
    url = 'http://www.cu.co.kr'
    api = '/tritops/main.jsp'
    data = {
        'cu_ingno': '',
        'sigungu': '',
        'bizpl_no': '',
        'srcType': '',
        'use_info_nm': '',
        'mnbr_code': '',
        'search_type': '',
        'tab_class': '1',
        'page_type': '',
        'srcTxt': '',
        'mnbr_nm': '',
    }
    data['sido'] = sido_name
    data['pg'] = intPageNo
    params = urllib.urlencode(data)
    #print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
    }

    try:
        urls = url + api + '?' + params
        print(urls)
        #req = urllib2.Request(urls, headers=hdr)
        #result = urllib2.urlopen(req)

        #req = urllib2.Request(url + api, params, headers=hdr)
        req = urllib2.Request(urls, headers=hdr)
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
    entity_list = tree.xpath('//div[@id="result"]//tbody//tr')
    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')

        # if len(info_list) < 5: continue  # 최소 5개 필드 있어야 함

        store_info = {}
        store_info['name'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['name'] = strtemp.rstrip().lstrip()

        store_info['subname'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.rstrip().lstrip().replace(' ', '/')

        store_info['type'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['type'] = strtemp.rstrip().lstrip()

        store_info['newaddr'] = '';     store_info['addr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            idx = strtemp.find('(')
            if idx > 0 and store_info['subname'] == '지점':      # '서울특별시 강동구 상일로15길 6 (고덕동)' 문자열에서 지점명 '고덕지점' 만들기
                dongname = strtemp[idx+1:].lstrip()
                idx = dongname.find(')')
                if idx != -1:
                    dongname = dongname[:idx].rstrip()
                    idx = dongname.find(',')
                    if idx != -1: dongname = dongname[:idx].lstrip()    # '(강일동,리버파크아파트)'와 같은 경우가 있어서...
                    if dongname.endswith('읍') or dongname.endswith('면') or dongname.endswith('동'):
                        if len(dongname) >= 3:
                            dongname = dongname[:-1]     # 일단 지점 명칭에서 '읍면동' postfix 제거했음 ('교동'같이 읍면동 이름이 3글자 미만인 경우는 제외)
                    store_info['subname'] = dongname + '/지점'

            #idx = strtemp.find(')')
            #if idx != -1:
            #    store_info['addr'] = strtemp[idx+1:].lstrip()
            #    strtemp = strtemp[:idx+1]

            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        store_info['xcoord'] = '';  store_info['ycoord'] = ''

        temp_list = info_list[1].xpath('./a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0].lstrip().rstrip()
            idx = strtemp.find('goDetail(')
            if idx == -1:
                store_list += [store_info];     continue
            id_list = strtemp[idx+9:-2].split(',')
            id1 = id_list[0][1:-1]
            id2 = id_list[1][1:-1]

            subapi = '/tritops/content.jsp'
            subdata = {
                'search_type': '',
                'sigungu': '',
                'tab_class': '1',
                'pg': '',
                'bizpl_no': '',
                'mnbr_nm': '',
                'use_info_nm': '',
                'page_type': 'detail',
                'srcType': '',
                'srcTxt': '',
            }
            data['sido'] = sido_name
            subdata['cu_ingno'] = id1
            subdata['mnbr_code'] = id2
            subparams = urllib.urlencode(subdata)

            try:
                suburls = url + subapi + '?' + subparams
                print(suburls)
                time.sleep(random.uniform(0.3, 0.9))
                subreq = urllib2.Request(suburls, headers=hdr)
                subreq.get_method = lambda: 'POST'
                subresult = urllib2.urlopen(subreq)

            except:
                print('Error calling the API')
                store_list += [store_info]
                continue

            code = subresult.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code)
                store_list += [store_info]
                continue

            subresponse = subresult.read()
            #print(subresponse)

            idx = subresponse.find('mapX =')
            if idx != -1:
                strtemp = subresponse[idx+6:].lstrip()
                idx = strtemp.find(';')
                store_info['xcoord'] = strtemp[:idx].rstrip()[1:-1]
                idx  = strtemp.find('mapY =')
                strtemp = strtemp[idx+6:].lstrip()
                idx = strtemp.find(';')
                store_info['ycoord'] = strtemp[:idx].rstrip()[1:-1]

            subtree = html.fromstring(subresponse)

            subinfo_list = subtree.xpath('//div[@id="result_src_desc"]//table//tr/td')
            if len(subinfo_list) >= 2:  # 최소 2개 필드 있어야 함
                strtemp = "".join(subinfo_list[1].itertext())
                if strtemp != None:
                    strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                    store_info['pn'] = strtemp.rstrip().lstrip().replace('.', '-').replace(')', '-').replace('(', '')

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
