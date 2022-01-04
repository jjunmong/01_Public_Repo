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

sido_list2 = {      # 테스트용 시도 목록
    '부산': '051'
}

sido_list = {
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

    outfile = codecs.open('sulbing_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|OT|XCOORD|YCOORD@@설빙\n")

    for sido_name in sorted(sido_list):

        page = 1
        while True:
            storeList = getStores(sido_name, page)
            if storeList == None: break;
            elif len(storeList) == 0: break

            for store in storeList:
                outfile.write(u'설빙|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['ot'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 49: break
            #elif len(storeList) < 15: break
            elif len(storeList) < 14: break     # 다음 페이지가 있는데 14개를 반환하는 경우도 있음 ㅠㅠ

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

# v2.0 (2018/7)
def getStores(strSidoName, intPageNo):
    url = 'http://sulbing.com'
    api = '/bbs/board.php'
    data = {
        'bo_table': 'store',
        'sop': 'and',
        #'sop': 'and',
    }
    data['s_wr_1'] = strSidoName
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    print(u'%s %d' % (strSidoName, intPageNo))
    #print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)    # for debugging
    #tree = html.fromstring(response)
    tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entity_list = tree.xpath('//div[@class="store_list"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):

        name_list = entity_list[i].xpath('.//a/@storename')
        addr_list = entity_list[i].xpath('.//a/@address')
        id_list = entity_list[i].xpath('.//a/@vid')
        xcoord_list = entity_list[i].xpath('.//a/@lx')
        ycoord_list = entity_list[i].xpath('.//a/@ly')
        info_list = entity_list[i].xpath('.//em')

        if len(name_list) < 1: continue

        store_info = {}

        store_info['name'] = '설빙'
        store_info['subname'] = ''
        strtemp = name_list[0]
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.startswith('설빙'): strtemp = strtemp[2:].lstrip()
            #if strtemp.startswith(strSidoName):
            #    strtemp = strtemp[len(strSidoName):].lstrip()
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = ''
        if len(id_list) > 0:
            strtemp = id_list[0]
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                store_info['id'] = strtemp

        store_info['addr'] = ''
        if len(addr_list) > 0:
            strtemp = addr_list[0]
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['addr'] = strtemp

        store_info['xcoord'] = ''
        store_info['ycoord'] = ''
        if len(xcoord_list) > 0: store_info['xcoord'] = xcoord_list[0]
        if len(ycoord_list) > 0: store_info['ycoord'] = ycoord_list[0]

        store_info['pn'] = ''
        store_info['ot'] = ''
        if len(info_list) > 0:
            strtemp = info_list[0].text
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                idx = strtemp.find('/')
                if idx != -1:
                    store_info['pn'] = strtemp[:idx].rstrip().replace(')', '-')
                    store_info['ot'] = strtemp[idx+1:].lstrip()
                else:
                    store_info['pn'] = strtemp.replace(')', '-')

        store_list += [store_info]

    return store_list


# v1.0
'''
def getStores(strSidoName):
    url = 'http://sulbing.com'
    api = '/online/wp-content/plugins/owl-maps/php/get-json.php'
    data = {
        'mode': 'address',
        'submode': 'store',
        'type': 'all',
        'fleids': '*',
        'list_row_tag': '<tr class="data"><td class="store_name"><a href="javascript:moveMap(\'{lating_y}|{lating_x}\',\'{store_namejs}\');">{store_name}</a></td><td class="store_phone_time"><p class="store_phone">{store_phone}</p><p class="store_time">{store_time}</p></td><td class="store_address pc_only">{store_address}</td></tr>',
        'storeAddr1': '',
        'storeAddr2': '',
        'searchKwd': '',
    }
    params = urllib.urlencode(data)
    print(params)

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'JSESSIONID=DBBE75A09FB6C761409B66573B6CA849; _ga=GA1.3.572484436.1481311150; wcs_bt=s_2f6be2a35c45:1482483708'
    }
    try:
        req = urllib2.Request(url + api, params, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)        # for debugging

    receivedData = json.loads(response)  # json 포맷으로 결과값 반환

    storeList = []
    for data_item in receivedData:
        shopdata = data_item['info']
        #print(shopdata)

        tree = html.fromstring(shopdata)
        #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + shopdata)

        entityList = tree.xpath('//tr')

        for i in range(len(entityList)):
            storeInfo = {}

            infoList = entityList[i].xpath('.//td')

            if (infoList == None):
                continue;  # for safety
            elif (len(infoList) < 3):
                continue  # 3개 필드 있음

            subname = "".join(infoList[0].itertext()).strip('\r\t\n')
            storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

            storeInfo['xcoord'] = '';       storeInfo['ycoord'] = ''
            coord_info = infoList[0].xpath('.//a/@href')
            if coord_info != None:
                coord_item = coord_info[0]

                idx = coord_item.find("Map('")
                coord_item = coord_item[idx + 5:]
                idx = coord_item.find("',")
                coord_item = coord_item[:idx]
                idx = coord_item.find('|')
                storeInfo['xcoord'] = coord_item[idx+1:]
                storeInfo['ycoord'] = coord_item[:idx]

            storeInfo['addr'] = ''
            strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
            if strtemp != None:
                storeInfo['addr'] = strtemp.rstrip().lstrip()

            storeInfo['pn'] = '';   storeInfo['ot'] = ''
            pnList = infoList[1].xpath('.//p[@class="store_phone"]')
            if pnList != None:
                strtemp = pnList[0].text
                if strtemp != None:
                    storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-')

            otList = infoList[1].xpath('.//p[@class="store_time"]')
            if otList != None:
                strtemp = otList[0].text
                if strtemp != None:
                    storeInfo['ot'] = strtemp.replace(' ', '').replace('am.', 'am').replace('pm.', 'pm').rstrip().lstrip()

            storeList += [storeInfo]

        break;

    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
