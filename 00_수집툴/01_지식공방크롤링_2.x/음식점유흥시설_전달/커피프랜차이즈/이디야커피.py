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

sidolist2 = {
    '광주광역시': {'동구','서구','남구','북구','광산구'},

}

sidolist = {
    '서울': {'종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구'},
    '광주': {'동구','서구','남구','북구','광산구'},
    '대구': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전': {'동구','중구','서구','유성구','대덕구'},
    '부산': {'중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군'},
    '울산': {'중구','남구','동구','북구','울주군'},
    '인천': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군'},
    '경기': {'수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구', '성남시 분당구','성남시 수정구','성남시 중원구','의정부시','안양시 동안구','안양시 만안구','부천시','광명시','평택시',
            '동두천시', '안산시 단원구','안산시 상록구','고양시 덕양구','고양시 일산서구','고양시 일산동구','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시',
            '용인시 기흥구','용인시 수지구','용인시 처인구','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군'},
    '강원': {'춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군'},
    '경상남도': {'창원시 마산합포구','창원시 마산회원구','창원시 성산구','창원시 의창구','창원시 진해구','진주시','통영시','사천시','김해시','밀양시','거제시',
             '양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군'},
    '경남': {'창원시 마산합포구','창원시 마산회원구','창원시 성산구','창원시 의창구','창원시 진해구','진주시','통영시','사천시','김해시','밀양시','거제시',
             '양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군'},
    '경상북도': {'포항시 북구','포항시 남구','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군'},
    '경북': {'포항시 북구','포항시 남구','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군'},
    '전라남도': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전남': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전라북도': {'전주시 덕진구','전주시 완산구','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '전북': {'전주시 덕진구','전주시 완산구','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충청남도': {'천안시 서북구','천안시 동남구','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충남': {'천안시 서북구','천안시 동남구','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충청북도': {'청주시 상당구','청주시 서원구','청주시 청원구','청주시 흥덕구','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '충북': {'청주시 상당구','청주시 서원구','청주시 청원구','청주시 흥덕구','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '제주': {'제주시','서귀포시'},
    '세종': {''}
}


def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('ediya_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OT@@이디야\n")

    for sidoname in sorted(sidolist):

        gugunlist = sidolist[sidoname]
        for gugunname in sorted(gugunlist):

            query = sidoname + ' ' + gugunname
            query = query.lstrip().rstrip()
            storeList = getStores(query)
            if storeList == None: break;
            elif len(storeList) == 0: break

            for store in storeList:
                outfile.write("이디야|")
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['ot'])

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

# v2.0 (2017/12)
def getStores(short_sidoname):
    url = 'https://www.ediya.com'
    api = '/inc/ajax_adm_map.php'
    data = {
        'gubun': 'map',
    }
    data['address'] = short_sidoname
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'PHPSESSID=k7eck8ejmq3aksqtnq0bosnfm1; _ga=GA1.2.1313761453.1512709826; _gid=GA1.2.658235623.1512709826',
        #'Cookie': 'PHPSESSID=k7eck8ejmq3aksqtnq0bosnfm1',
        'Host': 'www.ediya.com',
        'Origin': 'http://www.ediya.com',
        'Referer': 'http://www.ediya.com/contents/find_store.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
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
    idx = response.find('_&12345&_')
    if idx == -1: return None
    address_info = response[:idx].lstrip().rstrip()
    response = response[idx+9:].rstrip()

    idx = response.find('_&12345&_')
    if idx == -1: return None
    etc_info = response[:idx].lstrip()
    subname_info = response[idx+9:].rstrip().lstrip()

    if address_info.startswith('///'): address_info = address_info[3:].lstrip()
    if etc_info.startswith('///'): etc_info = etc_info[3:].lstrip()
    if subname_info.startswith('///'): subname_info = subname_info[3:].lstrip()

    addr_list = address_info.split('///')
    subname_list = subname_info.split('///')
    etcinfo_list = etc_info.split('///')

    store_list = []
    for i in range(len(subname_list)):
        store_info = {}

        strtemp = subname_list[i].lstrip().rstrip()
        strtemp = strtemp.replace(' ', '/')


        store_info['newaddr'] = ''
        if len(addr_list) > i: store_info['newaddr'] = addr_list[i]
        store_info['pn'] = ''
        store_info['id'] = ''

        strtemp = ''
        if len(etcinfo_list) > i: strtemp = etcinfo_list[i]
        idx = strtemp.find('&phone&')
        if idx != -1:
            store_info['pn'] = strtemp[idx+7:].replace('--', '').lstrip().rstrip()
            strtemp = strtemp[:idx].rstrip()

            idx = store_info['pn'].find('&phone&')
            if idx != -1:
                str_idinfo = store_info['pn'][idx+7:].lstrip()
                store_info['pn'] = store_info['pn'][:idx].rstrip()

                idx = str_idinfo.find('_')
                if idx != -1:
                    str_idinfo = str_idinfo[:idx].rstrip()
                store_info['id'] = str_idinfo

        store_info['ot'] = strtemp.replace('<br/>', ' ').replace('주말 및 공휴일에는 변경될 수 있습니다.', '').lstrip().rstrip()

        if store_info['id'] == '': continue

        if store_info['id'] != '':
            suburls = 'https://www.ediya.com/inc/ajax_adm_map.php'
            subdata = {
                'gubun': 'storeView',
            }
            subdata['idx'] = store_info['id']
            subparams = urllib.urlencode(subdata)
            print(subparams)

            try:
                subreq = urllib2.Request(suburls, subparams, headers=hdr)
                subreq.get_method = lambda: 'POST'
                time.sleep(random.uniform(0.3, 0.9))
                subresult = urllib2.urlopen(subreq)
            except:
                print('Error calling the subAPI');
                store_list += [store_info]
                continue

            subcode = subresult.getcode()
            if subcode != 200:
                print('HTTP request error (status %d)' % subcode);
                store_list += [store_info]
                continue

            subresponse = subresult.read()
            # print(subresponse)
            subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)

            name_list = subtree.xpath('//h1[@class="pop_tt"]')
            info_list = subtree.xpath('//div[@class="store_pop_info"]//dl')

            if len(name_list) > 0:
                strtemp = "".join(name_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                    strtemp = strtemp.replace(' ', '/')
                    if store_info['subname'] != strtemp:
                        print("지점명 변경 from " + store_info['subname'] + " to " + strtemp)
                        store_info['subname'] = strtemp

            for j in range(len(info_list)):
                tag_list = info_list[j].xpath('.//dt')
                value_list = info_list[j].xpath('.//dd')

                if len(tag_list) < 1 or len(value_list) < 1: continue

                tag = "".join(tag_list[0].itertext())
                value = "".join(value_list[0].itertext())

                if tag == None or value == None: continue

                tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                value = value.replace('<br/>', ' ').replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

                if tag == '전화번호':
                    store_info['pn'] = value
                elif tag == '매장주소':
                    store_info['newaddr'] = value
                elif tag == '영업시간':
                    store_info['ot'] = value.replace('주말 및', ';주말 및')

        store_list += [store_info]

    print(short_sidoname + ' : ' + str(len(store_list)))
    return store_list

# v1.0
'''
def getStores(intPageNo):
    url = 'http://www.ediya.com'
    api = '/board/listing/brd/store/page/'

    try:
        urls = url + api + str(intPageNo)
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    tableSelector = '//div[@class="table_wrap"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody/tr'
    entityList = dataTable.xpath(entitySelector)

    store_list = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        store_info = {}

        infoList = entityList[i].xpath('.//td')

        if (len(infoList) < 5):
            continue

        strtemp = infoList[1].text.lstrip().rstrip()
        strtemp = strtemp.replace(' ', '/')
        store_info['subname'] = strtemp

        store_info['newaddr'] = infoList[2].text
        store_info['pn'] = ''

        store_info['feat'] = ''
        featList = infoList[3].xpath('.//img/@alt')
        if featList != None:
            for feat_item in featList:
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += feat_item

        store_info['ot'] = ''
        temp_list = infoList[4].xpath('.//a/@href')
        if len(temp_list) < 1:
            store_list += [store_info];
            continue

        subapi = temp_list[0]

        try:
            suburls = url + subapi
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.7))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];
            continue

        code = result.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];
            continue

        subresponse = subresult.read()
        # print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="table_wrap"]//tbody//tr')

        for j in range(len(subinfo_list)):
            tag_list = subinfo_list[j].xpath('.//th')
            value_list = subinfo_list[j].xpath('.//td')

            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            value = "".join(value_list[0].itertext())

            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

            if tag == '영업시간':
                store_info['ot'] = value.replace('주말 및 공휴일에는 변경될 수 있습니다.', '').rstrip()
            elif tag == '주소':
                store_info['newaddr'] = value
            elif tag.find('전화번호') != -1:
                store_info['pn'] = value

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
