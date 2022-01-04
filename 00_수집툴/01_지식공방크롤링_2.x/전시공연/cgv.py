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

    outfile = codecs.open('cgv_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ORGNAME|ID|TELNUM|ADDR|NEWADDR|FEAT|XCOORD|YCOORD@@CGV\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['orgname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.cgv.co.kr'
    api = '/theaters/'
    data = {
    }
    params = urllib.urlencode(data)
    # print(params)

    try:
        urls = url + api
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    idx = response.find('theaterJsonData =')
    if idx == -1: return None
    response = response[idx+17:].lstrip()
    idx = response.find('}];')
    if idx == -1: return None
    response = response[:idx+2]
    response_json = json.loads(response)

    result_list = []
    for data_item in response_json:
        if data_item['AreaTheaterDetailList'] == None: continue

        store_list = data_item['AreaTheaterDetailList']

        for store in store_list:
            if store.has_key('TheaterName') != True:
                print('theater name missing')
                continue

            store_info = {}
            store_info['name'] = 'CGV'
            subname = store['TheaterName']
            orgname = subname
            if subname.startswith('CGV'): subname = subname[3:].lstrip()
            store_info['subname'] = subname.replace(' ', '/')
            store_info['orgname'] = orgname

            store_info['pn'] = '';    store_info['newaddr'] = '';   store_info['addr'] = '';    store_info['feat'] = ''

            subdata = {
                'date': '',
            }
            subdata['areacode'] = store['RegionCode']
            subdata['theaterCode'] = store['TheaterCode']
            subparams = urllib.urlencode(subdata)

            time.sleep(random.uniform(0.3, 0.9))
            try:
                suburl = url + api + '?' + subparams
                print(suburl)  # for debugging
                subresult = urllib.urlopen(suburl)
            except:
                print('Error calling the suburl');
                store_list += [store_info]
                continue

            code = subresult.getcode()
            if code != 200:
                print('suburl HTTP request error (status %d)' % code);
                store_list += [store_info]
                continue

            subresponse = subresult.read()
            # print(response)
            subtree = html.fromstring(subresponse)

            addrinfo_list = subtree.xpath('//div[@class="theater-info"]//strong')
            subinfo_list = subtree.xpath('//div[@class="theater-info"]//span/em')

            if len(addrinfo_list) > 0:
                strtemp = addrinfo_list[0].text
                strtemp2 = "".join(addrinfo_list[0].itertext())
                if strtemp != None:
                    store_info['addr'] = strtemp
                    if strtemp2 != None:
                        idx = strtemp2.find(strtemp)
                        if idx != -1:
                            strtemp2 = strtemp2[idx+len(strtemp):].lstrip()
                            idx = strtemp2.find('위치/주차')
                            if idx != -1: strtemp2 = strtemp2[:idx].rstrip()
                            store_info['newaddr'] = strtemp2

            if len(subinfo_list) >= 2:  # 최소 3개 필드 있어야 함
                strtemp = subinfo_list[0].text
                if strtemp != None:
                    store_info['pn'] = strtemp.lstrip().rstrip().replace('.', '-').replace(')', '-')

                strtemp = subinfo_list[1].text
                if strtemp != None:
                    store_info['feat'] = strtemp.lstrip().rstrip().replace(' ', '').replace(',', '')

            store_info['id'] = '';  store_info['xcoord'] = '';     store_info['ycoord'] = ''
            locinfo_url_list = subtree.xpath('//div[@class="theater-info"]//strong//a/@href')
            if len(locinfo_url_list) > 0:
                locinfo = locinfo_url_list[0]
                if locinfo.startswith('.'): locinfo = locinfo[1:]
                locinfo = locinfo.replace('#menu', '')

                time.sleep(random.uniform(0.3, 0.9))
                try:
                    suburl2 = url + '/theaters' + locinfo
                    print(suburl2)  # for debugging
                    subresult = urllib.urlopen(suburl2)
                except:
                    print('Error calling the suburl2');
                    store_list += [store_info]
                    continue

                code = subresult.getcode()
                if code != 200:
                    print('suburl HTTP request error (status %d)' % code);
                    store_list += [store_info]
                    continue

                subresponse = subresult.read()
                #print(subresponse)

                idx = subresponse.find('locationTheaterJsonData =')
                if idx != -1:
                    strtemp = subresponse[idx+25:].lstrip()
                    idx = strtemp.find('];')
                    if idx != -1:
                        strtemp = strtemp[:idx+1]
                        extra_info_list = json.loads(strtemp)
                        for extra_info in extra_info_list:
                            if extra_info['label'] == orgname:
                                store_info['id'] = extra_info['code']
                                store_info['xcoord'] = extra_info['lng']
                                store_info['ycoord'] = extra_info['lat']

            result_list += [store_info]

    return result_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
