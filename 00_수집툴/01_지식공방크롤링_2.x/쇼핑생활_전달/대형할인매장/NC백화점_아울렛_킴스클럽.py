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

    outfile = codecs.open('nc_outlet_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT|MTYPE@@NC아울렛\n")

    outfile2 = codecs.open('kimsclub_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@킴스클럽\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s\n' % u'아울렛')

            if store['feat'].find('킴스클럽') != -1:
                outfile2.write(u'%s|' % u'킴스클럽')
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s\n' % store['feat'])

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()

def getStores(intPageNo):
    url = 'http://www.elandretail.com'
    api = '/main.do'
    data = {
        'new_lang': '000600KO',
    }
    params = urllib.urlencode(data)
    # print(params)

    try:
        urls = url + api + '?' + params
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

    entity_list = tree.xpath('//ul[@class="subm3"]//li/a')

    result_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('./@href')
        if len(temp_list) == 0: continue

        subapi = temp_list[0].replace('store01', 'store09')
        subname = entity_list[i].text.lstrip().rstrip()

        try:
            suburl = url + subapi
            print(suburl)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');      continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);      continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        store_info = {}
        #store_info['name'] = 'NC백화점'
        store_info['name'] = 'NC뉴코아몰'
        if subname.startswith('뉴코아'):
            store_info['name'] = '뉴코아아울렛'
            subname = subname[3:].lstrip()
        elif subname.startswith('2001'):
            store_info['name'] = '2001아울렛'
            subname = subname[4:].lstrip()
        elif subname.startswith('NC'):
            subname = subname[2:].lstrip()
        elif subname.startswith('동아'):
            store_info['name'] = '동아아울렛'
            subname = subname[2:].lstrip()
            #if subname.startswith('마트'):
            #    store_info['name'] = '동아마트'
            #    subname = subname[2:].lstrip()

        store_info['subname'] = subname.lstrip().rstrip().replace(' ', '/')

        store_info['pn'] = ''
        store_info['newaddr'] = ''
        store_info['feat'] = ''

        info_node = subtree.xpath('//div[@class="local-info"]')
        if len(info_node) > 0:
            info_list = info_node[0].xpath('.//li')

            if len(info_list) < 3: continue  # 최소 3개 필드 있어야

            strtemp = "".join(info_list[1].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('대표전화'): strtemp = strtemp[4:].lstrip()
                idx = strtemp.find('(')
                if idx != -1: strtemp = strtemp[:idx].rstrip()
                store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')

            strtemp = "".join(info_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
                idx = strtemp.find('(')
                if idx != -1:
                    idx = strtemp.find(')')
                    strtemp = strtemp[idx+1:].lstrip()
                store_info['newaddr'] = strtemp

            strtemp = "".join(info_list[2].itertext())
            if strtemp.find('킴스클럽') != -1:
                store_info['feat'] = '킴스클럽'

            # x,y 좌표정보도 추출할 수 있음, 영업시간 등 기타정보 많음 (필요할 때 추출할 것!!)

        result_list += [store_info]

    return result_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
