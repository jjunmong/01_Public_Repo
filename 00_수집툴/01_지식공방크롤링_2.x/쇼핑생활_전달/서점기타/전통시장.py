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

sido_list2 = {      # 테스트용 시도 목록
    '부산': '51',
}

sido_list = {
    '서울': '02',
    '광주': '62',
    '대구': '53',
    '대전': '42',
    '부산': '51',
    '울산': '52',
    '인천': '32',
    '경기': '31',
    '강원': '33',
    '경남': '55',
    '경북': '54',
    '전남': '61',
    '전북': '63',
    '충남': '41',
    '충북': '43',
    '제주': '64',
    '세종': '65',
}


def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('market_all_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|ETCNAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|SIZE|SIZE2|FEAT|SOURCE2|XCOORD|YCOORD@@전통시장\n")

    outfile2 = codecs.open('market_big_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|ETCNAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|SIZE|SIZE2|FEAT|SOURCE2|XCOORD|YCOORD@@대형전문재래시장\n")

    outfile3 = codecs.open('market_special_utf8.txt', 'w', 'utf-8')
    outfile3.write("##NAME|ETCNAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|SIZE|SIZE2|FEAT|SOURCE2|XCOORD|YCOORD@@전문도매시장\n")

    outfile4 = codecs.open('market_other_utf8.txt', 'w', 'utf-8')
    outfile4.write("##NAME|ETCNAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|SIZE|SIZE2|FEAT|SOURCE2|XCOORD|YCOORD@@지역재래시장\n")



    storeList = getStores()

    for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['etcname'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['size'])
            outfile.write(u'%s|' % store['size2'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % u'시장통')
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

            if store['feat'].find(';대형시장') != -1:
                outfile2.write(u'%s|' % store['name'])
                outfile2.write(u'%s|' % store['etcname'])
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['type'])
                outfile2.write(u'%s|' % store['id'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s|' % store['size'])
                outfile2.write(u'%s|' % store['size2'])
                outfile2.write(u'%s|' % store['feat'])
                outfile2.write(u'%s|' % u'시장통')
                outfile2.write(u'%s|' % store['xcoord'])
                outfile2.write(u'%s\n' % store['ycoord'])
            elif store['type'] != '종합시장' and store['type'] != '':
                outfile3.write(u'%s|' % store['name'])
                outfile3.write(u'%s|' % store['etcname'])
                outfile3.write(u'%s|' % store['subname'])
                outfile3.write(u'%s|' % store['type'])
                outfile3.write(u'%s|' % store['id'])
                outfile3.write(u'%s|' % store['pn'])
                outfile3.write(u'%s|' % store['newaddr'])
                outfile3.write(u'%s|' % store['size'])
                outfile3.write(u'%s|' % store['size2'])
                outfile3.write(u'%s|' % store['feat'])
                outfile3.write(u'%s|' % u'시장통')
                outfile3.write(u'%s|' % store['xcoord'])
                outfile3.write(u'%s\n' % store['ycoord'])
            else:
                outfile4.write(u'%s|' % store['name'])
                outfile4.write(u'%s|' % store['etcname'])
                outfile4.write(u'%s|' % store['subname'])
                outfile4.write(u'%s|' % store['type'])
                outfile4.write(u'%s|' % store['id'])
                outfile4.write(u'%s|' % store['pn'])
                outfile4.write(u'%s|' % store['newaddr'])
                outfile4.write(u'%s|' % store['size'])
                outfile4.write(u'%s|' % store['size2'])
                outfile4.write(u'%s|' % store['feat'])
                outfile4.write(u'%s|' % u'시장통')
                outfile4.write(u'%s|' % store['xcoord'])
                outfile4.write(u'%s\n' % store['ycoord'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()
    outfile3.close()
    outfile4.close()

def getStores():
    url = 'http://www.sbiz.or.kr'
    api = '/sijangtong/nation/sijang/readSijangListAjax.do'
    data = {
        'city_cd':'2',
        'county_cd': '',
        'mkt_cd': '',
        'mkt_nm':'',
        'lati':'',
        'longi':'',
        'menu_id':'010100',
        'special_mkt_yn': '',
    }
    params = urllib.urlencode(data)
    #print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        #'Cookie': '__smVisitorID=GoPJUsfw6Yv; JSESSIONID=OWppk4VuFQN6LCLPn3m4dr4aeyPIG0msDrM6pegoAUYstJbYgiER7uHXURWGkTcI.mgap02p_servlet_mg',
    }

    try:
        urls = url + api + '?' + params
        print(urls)
        #req = urllib2.Request(urls, headers=hdr)
        #result = urllib2.urlopen(req)

        #req = urllib2.Request(url + api, params, headers=hdr)
        req = urllib2.Request(urls, headers=hdr)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)

    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)

    # 커멘트 부분에 euc-kr 코드가 섞여 있어서 커멘트 부분을 제거 (반환값은 utf-8 인코딩)
    response_core = ''
    while True:
        idx = response.find('<!--')
        if idx == -1:
            response_core += response
            break

        response_core += response[:idx]
        idx = response.find('-->')
        if idx == -1: return None

        response = response[idx+3:]

    #print(response_core)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + response_core)

    entity_list = tree.xpath('//table[@width="700"]//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        name_list = info_list[0].xpath('.//a/@market_name')
        id_list = info_list[0].xpath('.//a/@mkt_cd')
        siDo = info_list[0].xpath('.//a/@siDo')
        siGunGu = info_list[0].xpath('.//a/@siGunGu')
        xcoord_list = info_list[0].xpath('.//a/@longi')
        ycoord_list = info_list[0].xpath('.//a/@lati')
        if len(name_list) < 1 or len(id_list) < 1: continue

        store_info = {}
        store_info['name'] =  ''
        store_info['etcname'] = ''
        strtemp = name_list[0]
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            strtemp = strtemp.replace('(주)', '').replace('㈜', '').lstrip().rstrip()
            if strtemp.endswith(')'):
                idx = strtemp.rfind('(')
                if idx > 0:
                    store_info['etcname'] = strtemp[idx+1:-1].lstrip().rstrip()
                    strtemp = strtemp[:idx].rstrip()
            store_info['name'] = strtemp.replace(' ', '/')

        store_info['subname'] = ''

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            store_info['newaddr'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        store_info['pn'] = ''
        store_info['id'] = ''
        store_info['type'] = ''
        store_info['size'] = ''
        store_info['size2'] = ''
        store_info['feat'] = ''
        store_info['xcoord'] = '';    store_info['ycoord'] = ''

        if len(xcoord_list) > 0: store_info['xcoord'] = xcoord_list[0]
        if len(ycoord_list) > 0: store_info['ycoord'] = ycoord_list[0]

        #
        # 추가 정보 읽어들이기
        #
        shop_id = id_list[0]
        store_info['id'] = shop_id

        subdata = {}
        subdata['mkt_cd'] = shop_id
        subparams = urllib.urlencode(subdata)

        # step 1. 기본 정보 읽어들이기
        try:
            time.sleep(random.uniform(0.3, 0.9))
            sub_urls = url + '/nation/sijang/readSijangReportAjax.do' + '?' + subparams
            print(sub_urls)
            time.sleep(random.uniform(0.3, 0.5))
            # req = urllib2.Request(url + api, params, headers=hdr)
            subreq = urllib2.Request(sub_urls, headers=hdr)
            subreq.get_method = lambda: 'GET'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the sub API');     store_list += [store_info];     continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);     store_list += [store_info];     continue

        subresponse = subresult.read()
        #print(subresponse)
        if subresponse == None:
            store_list += [store_info];     continue
        subresponse = subresponse.lstrip().rstrip()
        if subresponse == '':
            store_list += [store_info];     continue

        subresult_json = json.loads(subresponse)
        #store_info['pn'] = ''
        if subresult_json.get('opener_tel'):
            store_info['pn'] = subresult_json['opener_tel']

        #store_info['id'] = ''
        if subresult_json.get('mkt_cd'):
            store_info['id'] = subresult_json['mkt_cd']

        # step 2. 상세 정보 읽어들이기
        try:
            sub_urls = url + '/nation/sijang/readSijangInfoAjax.do' + '?' + subparams
            print(sub_urls)
            time.sleep(random.uniform(0.3, 0.5))
            # req = urllib2.Request(url + api, params, headers=hdr)
            subreq = urllib2.Request(sub_urls, headers=hdr)
            subreq.get_method = lambda: 'GET'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the sub API');     store_list += [store_info];     continue

        code = subresult.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);     store_list += [store_info];     continue

        subresponse = subresult.read()
        #print(subresponse)
        if subresponse == None:
            store_list += [store_info];     continue
        subresponse = subresponse.lstrip().rstrip()
        if subresponse == '':
            store_list += [store_info];     continue

        subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)

        # subinfo_list = subtree.xpath('//div[@role="tabpanel"]//table//tr')     # 전체 탭의 정보 모두 추출
        subinfo_list = subtree.xpath('//div[@id="tab1"]//table//tr')        # 기본 탭에서만 정보 추출
        subinfo_list += subtree.xpath('//div[@id="tab5"]//table//tr')       # 추가로 여기서도 정보 추출


        for j in range(len(subinfo_list)):
            taginfo_list = subinfo_list[j].xpath('.//td')

            # to do : 온갖 정보 다 있음, 필요할 때 추출규칙 세분화해서 추출할 것!!!

            if len(taginfo_list) < 2: continue  # 최소 2개 필드 있어야 함

            tag = "".join(taginfo_list[0].itertext())
            value = "".join(taginfo_list[1].itertext())

            if tag == None or value == None: continue

            tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            if tag == '시장크기':
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += value
            elif tag == '개설주기':
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += value
            elif tag == '소유관리':
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += value
            elif tag == '시장형태':
                if store_info['feat'] != '': store_info['feat'] += ';'
                store_info['feat'] += value
            elif tag == '토지면적':
                store_info['size'] = value.replace('㎡', '').replace(',', '').replace(' ', '')
            elif tag == '전체점포수':
                store_info['size2'] = value
            elif tag == '상품취급':
                if value != '':
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += value
            elif tag == '주취급품목':
                if value != '':
                    if store_info['type'] != '': store_info['type'] += ';'
                    store_info['type'] += value

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
