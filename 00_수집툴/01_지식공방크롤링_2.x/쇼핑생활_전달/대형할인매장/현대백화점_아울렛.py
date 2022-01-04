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

    outfile = codecs.open('hyundai_department_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR@@현대백화점\n")

    outfile2 = codecs.open('hyundai_outlet_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|MTYPE@@현대아울렛\n")


    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['newaddr'])

            if store['name'].find('아울렛') != -1 or store['name'].find('시티몰') != -1:
                outfile2.write(u'%s|' % store['name'])
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['addr'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s\n' % u'아울렛')

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()

def getStores(intPageNo):
    url = 'http://www.ehyundai.com'
    api = '/newPortal/DP/DP000000_V.do'
    data = {
        'topheaderClick': 'Y',
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

    entity_list = tree.xpath('//li[@class="snb-item"]/a')

    result_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('./@href')
        if len(temp_list) == 0: continue

        strtemp = temp_list[0]
        if strtemp.find('DP000000_V.do') == -1 and strtemp.find('DP000000_M.do') == -1: continue

        idx = strtemp.find('branchCd=')
        if idx == -1: continue
        shop_id = strtemp[idx+9:]

        subname = entity_list[i].text

        subdata = {}
        subdata['branchCd'] = shop_id
        subparams = urllib.urlencode(subdata)

        try:
            suburl = url + '/newPortal/DP/WC/WC000000_V.do' + '?' + subparams
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
        store_info['name'] = '현대백화점'
        store_info['subname'] = subname.lstrip().rstrip().replace(' ', '/')

        if strtemp.find('uplex') != -1:
            store_info['name'] = '현대UPLEX'
        elif strtemp.find('outlet') != -1:
            store_info['name'] = '현대아울렛'

        store_info['pn'] = ''
        store_info['addr'] = '';     store_info['newaddr'] = '';   store_info['ot'] = ''

        info_node = subtree.xpath('//div[@class="triple_cont"]')
        if len(info_node) > 0:
            name_list = info_node[0].xpath('./h5')
            info_list = info_node[0].xpath('.//li')

            if len(info_list) < 2: continue  # 최소 2개 필드 있어야

            if len(name_list) > 0:
                name = name_list[0].text
                if name != None:
                    name = name.lstrip().rstrip()
                    idx = name.find(' ')
                    if idx != -1:
                        store_info['name'] = name[:idx]

            strtemp = "".join(info_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('대표전화 : '): strtemp = strtemp[7:].lstrip()
                idx = strtemp.find('(')
                if idx != -1: strtemp = strtemp[:idx].rstrip()
                store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '')

            strtemp = "".join(info_list[1].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
                idx = strtemp.find('/')
                if idx != -1:
                    store_info['newaddr'] = strtemp[:idx].rstrip().replace(':', '').lstrip().rstrip()
                    strtemp = strtemp[idx+1:]
                    store_info['addr'] = strtemp.replace('(구)', '').replace(':', '').lstrip().rstrip()
                else:
                    store_info['newaddr'] = strtemp.replace(':', '').lstrip().rstrip()

        result_list += [store_info]

    return result_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
