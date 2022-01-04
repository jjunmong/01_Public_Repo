# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
import random
#import json
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

    outfile = codecs.open('museum_all_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|TYPE|SUBNAME|TELNUM|NEWADDR|OT|OFFDAY|COST|FEAT|WEBSITE|SOURCE2|XCOORD|YCOORD@@박물관\n")

    outfile2 = codecs.open('museum_art_big_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|TYPE|SUBNAME|TELNUM|NEWADDR|OT|OFFDAY|COST|FEAT|WEBSITE|SOURCE2|XCOORD|YCOORD@@미술관\n")

    outfile22 = codecs.open('museum_art_other_utf8.txt', 'w', 'utf-8')
    outfile22.write("##NAME|TYPE|SUBNAME|TELNUM|NEWADDR|OT|OFFDAY|COST|FEAT|WEBSITE|SOURCE2|XCOORD|YCOORD@@미술관\n")

    outfile3 = codecs.open('museum_memorial_utf8.txt', 'w', 'utf-8')
    outfile3.write("##NAME|TYPE|SUBNAME|TELNUM|NEWADDR|OT|OFFDAY|COST|FEAT|WEBSITE|SOURCE2|XCOORD|YCOORD@@기념관\n")

    outfile4 = codecs.open('museum_big_utf8.txt', 'w', 'utf-8')
    outfile4.write("##NAME|TYPE|SUBNAME|TELNUM|NEWADDR|OT|OFFDAY|COST|FEAT|WEBSITE|SOURCE2|XCOORD|YCOORD@@박물관\n")

    outfile42 = codecs.open('museum_other_utf8.txt', 'w', 'utf-8')
    outfile42.write("##NAME|TYPE|SUBNAME|TELNUM|NEWADDR|OT|OFFDAY|COST|FEAT|WEBSITE|SOURCE2|XCOORD|YCOORD@@박물관\n")


    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['offday'])
            outfile.write(u'%s|' % store['cost'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['website'])
            outfile.write(u'%s|' % u'한국박물관협회')
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

            if store['name'].endswith('미술관'):
                if store['type'] == '국립' or store['type'] == '공립':
                    outfile2.write(u'%s|' % store['name'])
                    outfile2.write(u'%s|' % store['type'])
                    outfile2.write(u'%s|' % store['subname'])
                    outfile2.write(u'%s|' % store['pn'])
                    outfile2.write(u'%s|' % store['newaddr'])
                    outfile2.write(u'%s|' % store['ot'])
                    outfile2.write(u'%s|' % store['offday'])
                    outfile2.write(u'%s|' % store['cost'])
                    outfile2.write(u'%s|' % store['feat'])
                    outfile2.write(u'%s|' % store['website'])
                    outfile2.write(u'%s|' % u'한국박물관협회')
                    outfile2.write(u'%s|' % store['xcoord'])
                    outfile2.write(u'%s\n' % store['ycoord'])
                else:
                    outfile22.write(u'%s|' % store['name'])
                    outfile22.write(u'%s|' % store['type'])
                    outfile22.write(u'%s|' % store['subname'])
                    outfile22.write(u'%s|' % store['pn'])
                    outfile22.write(u'%s|' % store['newaddr'])
                    outfile22.write(u'%s|' % store['ot'])
                    outfile22.write(u'%s|' % store['offday'])
                    outfile22.write(u'%s|' % store['cost'])
                    outfile22.write(u'%s|' % store['feat'])
                    outfile22.write(u'%s|' % store['website'])
                    outfile22.write(u'%s|' % u'한국박물관협회')
                    outfile22.write(u'%s|' % store['xcoord'])
                    outfile22.write(u'%s\n' % store['ycoord'])
            elif store['name'].endswith('기념관'):
                outfile3.write(u'%s|' % store['name'])
                outfile3.write(u'%s|' % store['type'])
                outfile3.write(u'%s|' % store['subname'])
                outfile3.write(u'%s|' % store['pn'])
                outfile3.write(u'%s|' % store['newaddr'])
                outfile3.write(u'%s|' % store['ot'])
                outfile3.write(u'%s|' % store['offday'])
                outfile3.write(u'%s|' % store['cost'])
                outfile3.write(u'%s|' % store['feat'])
                outfile3.write(u'%s|' % store['website'])
                outfile3.write(u'%s|' % u'한국박물관협회')
                outfile3.write(u'%s|' % store['xcoord'])
                outfile3.write(u'%s\n' % store['ycoord'])
            else:
                if store['type'] == '국립' or store['type'] == '공립':
                    outfile4.write(u'%s|' % store['name'])
                    outfile4.write(u'%s|' % store['type'])
                    outfile4.write(u'%s|' % store['subname'])
                    outfile4.write(u'%s|' % store['pn'])
                    outfile4.write(u'%s|' % store['newaddr'])
                    outfile4.write(u'%s|' % store['ot'])
                    outfile4.write(u'%s|' % store['offday'])
                    outfile4.write(u'%s|' % store['cost'])
                    outfile4.write(u'%s|' % store['feat'])
                    outfile4.write(u'%s|' % store['website'])
                    outfile4.write(u'%s|' % u'한국박물관협회')
                    outfile4.write(u'%s|' % store['xcoord'])
                    outfile4.write(u'%s\n' % store['ycoord'])
                else:
                    outfile42.write(u'%s|' % store['name'])
                    outfile42.write(u'%s|' % store['type'])
                    outfile42.write(u'%s|' % store['subname'])
                    outfile42.write(u'%s|' % store['pn'])
                    outfile42.write(u'%s|' % store['newaddr'])
                    outfile42.write(u'%s|' % store['ot'])
                    outfile42.write(u'%s|' % store['offday'])
                    outfile42.write(u'%s|' % store['cost'])
                    outfile42.write(u'%s|' % store['feat'])
                    outfile42.write(u'%s|' % store['website'])
                    outfile42.write(u'%s|' % u'한국박물관협회')
                    outfile42.write(u'%s|' % store['xcoord'])
                    outfile42.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 199: break       # 2018년 5월 51까지
        elif len(store_list) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close();   outfile22.close()
    outfile3.close()
    outfile4.close();   outfile42.close()

def getStores(intPageNo):
    url = 'http://www.museum.or.kr'
    api = '/museum_bd4/bbs/board.php'
    data = {
        'bo_table': 'museums',
        #'sca': '국립',
        'sca': '',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    tree = html.fromstring(response)

    entity_list = tree.xpath('//table//tr[@height="35"]')   # 반환값에서 구분자 불분명 ㅠㅠ

    store_list = []
    for i in range(len(entity_list)):

        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 4: continue  # 최소 4개 필드 있어야 함

        store_info = {}

        store_info['name'] = ''
        store_info['type'] = ''
        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('['):
                idx = strtemp.find(']')
                if idx > 1:
                    store_info['type'] = strtemp[1:idx].lstrip().rstrip()
                    strtemp = strtemp[idx+1:].lstrip()

            if strtemp.endswith(')'):
                idx = strtemp.rfind('(')
                if idx > 0:
                    store_info['subname'] = strtemp[idx+1:-1].lstrip().rstrip()
                    strtemp = strtemp[:idx].rstrip()

            store_info['name'] = strtemp.replace(' / ', '/').replace(' ', '/')

        if store_info['name'] == '관명': continue

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['ot'] = ''
        store_info['offday'] = ''
        store_info['feat'] = ''
        store_info['cost'] = ''
        store_info['website'] = ''
        store_info['xcoord'] = ''
        store_info['ycoord'] = ''

        temp_list = info_list[1].xpath('./a/@href')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        subapi = temp_list[0]
        if subapi.startswith('..'): subapi = '/museum_bd4' + subapi[2:]

        try:
            suburls = url + subapi
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//table[@width="777"]//tr')   # 반환값에서 구분자 불분명 ㅠㅠ

        for j in range(len(subinfo_list)):
            item_list = subinfo_list[j].xpath('.//td')
            if len(item_list) < 2: continue  # 최소 2개 필드 있어야 함

            str_key = "".join(item_list[0].itertext())
            str_value = "".join(item_list[1].itertext())

            if str_key != None and str_value != None:
                str_key = str_key.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                str_value = str_value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

                if str_key == '휴관일':
                    store_info['offday'] = str_value
                elif str_key == '입장료':
                    store_info['cost'] = str_value
                elif str_key == '부대시설':
                    store_info['feat'] = str_value.replace(',', ';')
                elif str_key == '홈페이지':
                    store_info['website'] = str_value
                elif str_key == '관람안내':
                    store_info['ot'] = str_value
                elif str_key == '주소':
                    temp_list = item_list[1].xpath('./a/@href')
                    if len(temp_list) > 0:
                        strtemp = temp_list[0]
                        # 0                               1            2              3             4            5
                        #'http://map.naver.com/?dlevel=11&pinType=site&pinId=11620558&x=126.8830500&y=35.1890510&enc=b64 target=_blank'
                        temp_list = strtemp.split('&')
                        if len(temp_list) > 5:
                            if temp_list[3].startswith('x='):
                                store_info['xcoord'] = temp_list[3][2:].lstrip().rstrip()
                            if temp_list[4].startswith('y='):
                                store_info['ycoord'] = temp_list[4][2:].lstrip().rstrip()

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
