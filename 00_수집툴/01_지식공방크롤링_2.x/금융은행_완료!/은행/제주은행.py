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

    outfile = codecs.open('jejubank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OT|XCOORD|YCOORD@@제주은행\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 99: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'https://www.e-jejubank.com'
    api = '/HomeBranch.do'
    data = {}
    params = urllib.urlencode(data)
    #print(params)
    params = 'menuCd=674&scrType=Search&currPage=' + str(intPageNo) + '&selectRow=0&srchCond1=&srchCond2=&srchCondition5=&srchCondition6=&srchCondition7=&srchCondition8=&srchCondition10=&srchCondition11=&srchSeqNo=0&detailViewFalg=&branchType=ALL&branchType2=pageing&airportType=&checkBox_All=&checkBox_BRA_USE=&checkBox_BRA_GUBUN=&checkBox_BRA_HANDICAP=&checkBox_BRA_TANLEOK=&branchHiddenSearchText=&detailViewIDNo=0&branchName=bra_name&branchNameText=&cChk=checkBocheckBox_BRA_USEx_All&cChk=checkBox_BRA_USE&cChk=checkBox_BRA_GUBUN&cChk=checkBox_BRA_HANDICAP&cChk=checkBox_BRA_TANLEOK&branchJuSo=ALL&branchJuSoText='

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, headers=hdr)
        req = urllib2.Request(url + api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    print(response)
    response_json = json.loads(response)

    entity_list = response_json['schList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '제주은행'
        store_info['id'] = entity_list[i]['BRA_BRAID']
        store_info['subname'] = entity_list[i]['BRA_NAME'].lstrip().rstrip().replace(' ', '/')

        store_info['newaddr'] = entity_list[i]['BRA_ADDR1'] + ' ' + entity_list[i]['BRA_ADDR2']
        store_info['pn'] = entity_list[i]['BRA_TELNO'].replace(')', '-')
        store_info['ot'] = ''
        if entity_list[i].get('BRA_OPTIME'):
            store_info['ot'] = entity_list[i]['BRA_OPTIME'].replace(' ', '')

        store_info['xcoord'] = entity_list[i]['BRA_Y']
        store_info['ycoord'] = entity_list[i]['BRA_X']

        store_list += [store_info]

    return store_list


    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@id="all_tblview"]//tbody//tr')

    store_list = []
    for i in range(len(entity_list)):
        info_list = entity_list[i].xpath('.//td')
        if len(info_list) < 5: continue  # 최소 필드 수 체크

        store_info = {}

        store_info['name'] = '수협'

        store_info['subname'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[4].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '-').replace('.', '-')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
