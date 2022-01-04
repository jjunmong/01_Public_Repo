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
import xml.etree.ElementTree as ElementTree

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

    outfile = codecs.open('insurance_hyndai_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|XCOORD|YCOORD@@현대해상\n")

    outfile2 = codecs.open('hicar_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|XCOORD|YCOORD@@현대해상하이카\n")


    for i in range(1,6):
        page = 1
        while True:
            store_list = getStores(i, page)
            if store_list == None: break;

            for store in store_list:
                if i == 4:
                    outfile2.write(u'%s|' % store['name'])
                    outfile2.write(u'%s|' % store['subname'])
                    outfile2.write(u'%s|' % store['pn'])
                    outfile2.write(u'%s|' % store['addr'])
                    outfile2.write(u'%s|' % store['newaddr'])
                    outfile2.write(u'%s|' % store['xcoord'])
                    outfile2.write(u'%s\n' % store['ycoord'])
                else:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['subname'])
                    outfile.write(u'%s|' % store['pn'])
                    outfile.write(u'%s|' % store['addr'])
                    outfile.write(u'%s|' % store['newaddr'])
                    outfile.write(u'%s|' % store['xcoord'])
                    outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 199: break
            elif len(store_list) < 5: break

            time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()

def getStores(store_type, intPageNo):
    url = 'https://www.hi.co.kr'
    api = '/HHBR1001M01L/HH.xhi'
    data = {}
    params = urllib.urlencode(data)
    print(str(store_type) + ' ' + str(intPageNo))

    params = 'loginId=999997&requestData=%3Croot%3E%0A++++%3Cheader%3E%0A++++++++%3CgId%3E7abfca6686dc978394166712657300%3C%2FgId%3E%0A++++++++%3CtranId%3EHHBR1001M01L%3C%2FtranId%3E%0A++++++++%3CchannelId%3EHI-HOME%3C%2FchannelId%3E%0A++++++++%3CclientIp%3E125.129.242.227%3C%2FclientIp%3E%0A++++++++%3CmenuId%2F%3E%0A++++%3C%2Fheader%3E%0A++++%3Crequest%3E%0A++++++++%3CpageNo%3E'
    params += str(intPageNo) + '%3C%2FpageNo%3E%0A++++++++%3CrowCount%3E5%3C%2FrowCount%3E%0A++++++++%3CsdNm%2F%3E%0A++++++++%3CaraNm%2F%3E%0A++++++++%3CbzCatChcYn1%2F%3E%0A++++++++%3CbzCatChcYn2%2F%3E%0A++++++++%3CbzCatChcYn3%2F%3E%0A++++++++%3CbzCatChcYn4%2F%3E%0A++++++++%3CbzCatChcYn5%2F%3E%0A++++++++%3CbzCatChcYn6%2F%3E%0A++++++++%3CbzCatChcYn7%2F%3E%0A++++++++%3CbzCatChcYn8%2F%3E%0A++++++++%3CbzCatChcYn9%2F%3E%0A++++++++%3CbzCatChcYn10%2F%3E%0A++++++++%3CbzCatChcYn11%2F%3E%0A++++++++%3CbzCatChcYn12%2F%3E%0A++++++++%3CbzCatChcYn13%2F%3E%0A++++++++%3CbzCatChcYn14%2F%3E%0A++++++++%3CbzCatChcYn15%2F%3E%0A++++++++%3CbzCatChcYn16%2F%3E%0A++++++++%3CbzCatChcYn17%2F%3E%0A++++++++%3CbzCatChcYn18%2F%3E%0A++++++++%3CbzCatChcYn19%2F%3E%0A++++++++%3CbzCatChcYn20%2F%3E%0A++++++++%3C'
    params += 'bzCatCd%3E' + str(store_type) + '%3C%2FbzCatCd%3E%0A++++++++%3CsearchWord%2F%3E%0A++++%3C%2Frequest%3E%0A%3C%2Froot%3E'

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
    #print(response)
    root = ElementTree.fromstring(response)

    storeList = []
    for child in root.iter('hhbr1001voList_row'):
        storeInfo = {}
        storeInfo['name'] = '현대해상화재보험'
        if store_type == 4: storeInfo['name'] = '하이카프라자'
        storeInfo['subname'] = ''
        storeInfo['pn'] = ''
        storeInfo['addr'] = ''
        storeInfo['newaddr'] = ''
        storeInfo['xcoord'] = ''
        storeInfo['ycoord'] = ''

        for infoitem in child:
            # print(child.tag, child.text)

            if infoitem.tag == 'bzNm' and infoitem.text != None:
                storeInfo['subname'] = infoitem.text.lstrip().rstrip().replace(' ', '/')
            elif infoitem.tag == 'telNo1' and infoitem.text != None:
                storeInfo['pn'] = infoitem.text
            elif infoitem.tag == 'telNo2' and infoitem.text != None:
                storeInfo['pn'] += '-' + infoitem.text
            elif infoitem.tag == 'telNo3' and infoitem.text != None:
                storeInfo['pn'] += '-' + infoitem.text
            elif infoitem.tag == 'addr1':
                storeInfo['addr'] = infoitem.text
            elif infoitem.tag == 'addr2' and infoitem.text != None:
                storeInfo['addr'] += ' ' + infoitem.text
            elif infoitem.tag == 'roadAddr1':
                storeInfo['newaddr'] = infoitem.text
            elif infoitem.tag == 'roadAddr2' and infoitem.text != None:
                storeInfo['newaddr'] += ' ' + infoitem.text
            elif infoitem.tag == 'lgtd':
                storeInfo['xcoord'] = infoitem.text
            elif infoitem.tag == 'latd':
                storeInfo['ycoord'] = infoitem.text

        if storeInfo['pn'].startswith('-'): storeInfo['pn'] = storeInfo['pn'][1:]
        storeList += [storeInfo]

    delay_time = random.uniform(0.1, 0.4)
    time.sleep(delay_time)
    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
