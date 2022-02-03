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

    outfile = codecs.open('kofic_all_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|SCREEN|SIZE|HOMEPAGE|SOURCE2@@영화관\n")

    outfile2 = codecs.open('kofic_other_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|SCREEN|SIZE|HOMEPAGE|SOURCE2@@일반극장영화관\n")

    outfile3 = codecs.open('lottecinema_utf8.txt', 'w', 'utf-8')
    outfile3.write("##NAME|SUBNAME|TYPE|ID|TELNUM|NEWADDR|SCREEN|SIZE|HOMEPAGE|SOURCE2@@롯데시네마\n")


    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['screen'])
            outfile.write(u'%s|' % store['size'])
            outfile.write(u'%s|' % store['homepage'])
            outfile.write(u'%s\n' % u'영화진흥위원회')

            if store['homepage'].find('cgv') != -1 or store['name'].find('CGV') != -1: pass
            elif store['homepage'].find('megabox') != -1 or store['name'].find('메가박스') != -1: pass
            elif store['homepage'].find('lottecinema') != -1 or store['name'].find('롯데시네마') != -1:
                outfile3.write(u'%s|' % store['name'])
                outfile3.write(u'%s|' % store['subname'])
                outfile3.write(u'%s|' % store['type'])
                outfile3.write(u'%s|' % store['id'])
                outfile3.write(u'%s|' % store['pn'])
                outfile3.write(u'%s|' % store['newaddr'])
                outfile3.write(u'%s|' % store['screen'])
                outfile3.write(u'%s|' % store['size'])
                outfile3.write(u'%s|' % store['homepage'])
                outfile3.write(u'%s\n' % u'영화진흥위원회')
            else:
                outfile2.write(u'%s|' % store['name'])
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['type'])
                outfile2.write(u'%s|' % store['id'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s|' % store['screen'])
                outfile2.write(u'%s|' % store['size'])
                outfile2.write(u'%s|' % store['homepage'])
                outfile2.write(u'%s\n' % u'영화진흥위원회')

        page += 1

        if page == 59: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()
    outfile3.close()


def getStores(intPageNo):
    url = 'http://www.kobis.or.kr'
    api = '/kobis/business/mast/thea/findTheaterInfoList.do'
    hdr = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '218',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ACEUCI=1; JSESSIONID=bWH2pfsVxyTKYb7vCjFKvQT1MBt3lQQ21GCh2vH5QZf4Qtzl9J2D!96614232!-774082815; ACEFCID=UID-5E1FAC96580FC37F71C53973; _ga=GA1.3.764442180.1579134103; _gid=GA1.3.417307771.1579134103; ACEFBID=X6R5LQSJWKKVQE8880VXJMYOA; _gat_gtag_UA_127072686_1=1',
        'Host': 'www.kobis.or.kr',
        'Origin': "http': // www.kobis. or.kr",
        'Referer': "http': // www.kobis. or.kr / kobis / business / mast / thea / findTheaterInfoList.do",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'CSRFToken': '5XvCFzMjX0GckYFxlW2EomSVmxt_PCHWSw1QhP5DHCM'
    }
    data = {
        'CSRFToken': '5XvCFzMjX0GckYFxlW2EomSVmxt_PCHWSw1QhP5DHCM',
        'theaCd': '',
        'sTheaNm': '',
        'sTheaCd': '',
        'sPermYn': 'Y',
        'sJoinYn': 'Y',
        'sWideareaCd': '',
        'sBasareaCd': '',
        'sSaleStat': '018201',
        'sSenderCd': '',
        'CSRFToken': '5XvCFzMjX0GckYFxlW2EomSVmxt_PCHWSw1QhP5DHCM',
    }
    data['pageIndex'] = intPageNo
    params = urllib.urlencode(data)
    #
    # hdr = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #     'Accept-Encoding': 'gzip, deflate, sdch',
    #     'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    #     'Connection': 'keep-alive',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    # }

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
    tree = html.fromstring(response)
    print(tree)
    entity_list = tree.xpath('//table[@class="tbl_comm"]//tbody//tr')
    print(entity_list)
    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 11: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[3].itertext())
        print(strtemp)
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('롯데시네마'):
                store_info['name'] = '롯데시네마'
                store_info['subname'] = strtemp[5:].lstrip().replace(' ', '/')
            elif strtemp.startswith('메가박스'):
                store_info['name'] = '메가박스'
                store_info['subname'] = strtemp[4:].lstrip().replace(' ', '/')
            elif strtemp.startswith('CGV'):
                store_info['name'] = 'CGV'
                store_info['subname'] = strtemp[3:].lstrip().replace(' ', '/')
            else:
                store_info['name'] = strtemp.replace(' ', '/')

        store_info['id'] = ''
        temp_list = info_list[3].xpath('.//a/@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('fn_detail(')
            if idx != -1:
                strtemp = strtemp[idx+10:]
                idx = strtemp.find(');')
                subinfo_list = strtemp[:idx].split(',')
                if len(subinfo_list) >= 3:
                    store_info['id'] = subinfo_list[2].lstrip().rstrip()[1:-1]

        store_info['type'] = ''
        strtemp = "".join(info_list[6].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['type'] = strtemp

        store_info['screen'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['screen'] = strtemp

        store_info['size'] = ''
        strtemp = "".join(info_list[5].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['size'] = strtemp


        store_info['newaddr'] = ''
        store_info['homepage'] = ''
        store_info['pn'] = ''

        # 상세정보 페이지 크롤링
        if store_info['id'] != '':
            suburl = 'http://www.kobis.or.kr/kobis/business/mast/thea/findTheaterCodeLayer.do?theaCd=' + store_info['id']
            try:
                time.sleep(random.uniform(0.3, 0.9))
                print(suburl)   # for debugging
                subresult = urllib.urlopen(suburl)
            except:
                print('Error calling the subAPI')
                store_list += [store_info];     continue

            code = subresult.getcode()
            if code != 200:
                print('HTTP request error (status %d)' % code);
                store_list += [store_info];     continue

            subresponse = subresult.read()
            # print(subresponse)
            #subtree = html.fromstring(subresponse)
            subtree = html.fromstring('<?xml version="1.0" encoding="utf-8"?>' + subresponse)

            subinfo_list = subtree.xpath('//table[@class="tbl_99"]//tbody//tr')
            print(subinfo_list)
            for j in range(len(subinfo_list)):
                tag_list = subinfo_list[j].xpath('.//th')
                value_list = subinfo_list[j].xpath('.//td')

                if len(tag_list) < 1 or len(value_list) < 1: continue

                tag = "".join(tag_list[0].itertext())
                value = "".join(value_list[0].itertext())

                if tag == None or value == None: continue

                tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

                if tag.find('전화번호') != -1:
                    if value.startswith('('): value = value[1:].lstrip()    # '(031)311-2234' 이렇게 표기한 경우 있음
                    store_info['pn'] = value.replace(' ', '').replace('.', '-').replace(')', '-')
                elif tag == '주소':
                    if value.startswith('('):   # 우편번호 정보 제거
                        idx = value.find(')')
                        value = value[idx+1:].lstrip()
                    store_info['newaddr'] = value
                elif tag == '홈페이지':
                    store_info['homepage'] = value

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
