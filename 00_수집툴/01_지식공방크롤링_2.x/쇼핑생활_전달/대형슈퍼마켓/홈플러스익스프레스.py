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

    outfile = codecs.open('homeplus_express_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|OT|OFFDAY|XCOORD|YCOORD@@홈플러스익스프레스\n")

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
            outfile.write(u'%s|' % store['offday'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 2: break     # 한번 호출로 모든 점포 정보 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    url = 'http://corporate.homeplus.co.kr'
    api = '/Store/HyperMarket.aspx'

    #data = {}
    #params = urllib.urlencode(data)
    # storetype1 = 홈플러스   storetype2 = 홈플러스익스프레스
    params = '__EVENTTARGET=ctl00%24ContentPlaceHolder1%24storetype2&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUJLTc2MDkzMDI3D2QWAmYPZBYCAgUPZBYCAgEPZBYOAgEPEGRkFgFmZAIHDxYCHgVjbGFzcwUOYnRuIGJ0bi1jaGVjazEWAgIBDxAPFgIeB0NoZWNrZWRoZGRkZAIJDxYCHwAFDmJ0biBidG4tY2hlY2syFgICAQ8QDxYCHwFoZGRkZAILDxYCHwAFDmJ0biBidG4tY2hlY2szFgICAQ8QDxYCHwFoZGRkZAINDw8WAh4EVGV4dAUG7KCE7LK0ZGQCDw8PFgIfAgUBMGRkAhEPFgIeC18hSXRlbUNvdW50ZmQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgMFJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkc3RvcmV0eXBlMQUkY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRzdG9yZXR5cGUyBSRjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJHN0b3JldHlwZTMe2a7%2Fc0iKSsdvL6%2BufoUrPDl8iw%3D%3D&ctl00%24ContentPlaceHolder1%24Region_Code=&ctl00%24ContentPlaceHolder1%24srch_name=&ctl00%24ContentPlaceHolder1%24storetype2=on'
    print(params)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
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
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//ul[@class="result_list"]//li[@class="clearfix"]')

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '홈플러스익스프레스'

        store_info['subname'] = ''
        subapi = ''
        temp_list = entity_list[i].xpath('.//span[@class="name"]')
        if len(temp_list) > 0:
            strtemp = "".join(temp_list[0].itertext())
            if strtemp != None:
                strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
                store_info['subname'] = strtemp.replace(' ', '/')
            temp_list2 = temp_list[0].xpath('./a/@href')
            if len(temp_list2) > 0:
                subapi = temp_list2[0]

        store_info['pn'] = '';  store_info['ot'] = '';  store_info['offday'] = ''
        temp_list = entity_list[i].xpath('.//div[@class="col-lg-4 time"]')
        if len(temp_list) > 0:
            strtemp = temp_list[0].xpath('.//span')[0].text
            if strtemp != None:
                store_info['ot'] = strtemp.lstrip().rstrip()
            strtemp = temp_list[0].xpath('.//em')[0].text
            if strtemp != None:
                store_info['pn'] = strtemp.lstrip().rstrip().replace('.', '-').replace(')', '-').replace(' ', '-')
            tempinfo_list = temp_list[0].xpath('.//span[@class="off"]')     # 휴무일 정보가 없는 경우도 있음 ㅠㅠ
            if len(tempinfo_list) > 0:
                strtemp = tempinfo_list[0].text
                if strtemp != None:
                    store_info['offday'] = strtemp.lstrip().rstrip()

        store_info['xcoord'] = '';      store_info['ycoord'] = ''
        temp_list = entity_list[i].xpath('.//li[@class="navi"]/a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]      # 'http://map.naver.com/?dlevel=12&menu=route&elng=129.027&elat=35.153&eText=홈플러스 가야점'
            idx = strtemp.find('&elng=')
            if idx != -1:
                strtemp = strtemp[idx+6:].lstrip()
                idx = strtemp.find('&elat=')
                store_info['xcoord'] = strtemp[:idx].rstrip()
                strtemp = strtemp[idx+6:].lstrip()
                idx = strtemp.find('&')
                store_info['ycoord'] = strtemp[:idx].rstrip()

        store_info['newaddr'] = ''
        store_info['id'] = ''

        idx = subapi.find('sn=')
        if idx != -1:
            strtemp = subapi[idx+3:]
            idx = strtemp.find('&ind=')
            if idx != -1:
                store_info['id'] = strtemp[:idx]

        if subapi == '':
            store_list += [store_info];     continue

        try:
            suburls = url + subapi
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
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
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//div[@class="tab-content"]//tbody//tr')

        for j in range(len(subinfo_list)):
            tag_list = subinfo_list[j].xpath('.//th')
            value_list = subinfo_list[j].xpath('.//td')

            if len(tag_list) < 1 or len(value_list) < 1: continue

            tag = "".join(tag_list[0].itertext())
            value = "".join(value_list[0].itertext())

            if tag == None or value == None: continue

            tag = tag.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            value = value.lstrip().rstrip().replace('\r', '').replace('\t', '').replace('\n', '')

            if tag == '영업시간':
                store_info['ot'] = value
            elif tag == '주소':
                store_info['newaddr'] = value
            elif tag == '휴무일':
                store_info['offday'] = value


        # 내부 입점 점포 정보도 다 있음 (필요할 때 추출할 것!!)

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
