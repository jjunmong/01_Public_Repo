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
from selenium import webdriver
from seleniumrequests import Chrome
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

    outfile = codecs.open('pelicana_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|XCOORD|YCOORD\n")

    driver = webdriver.Chrome('C:\Python27\chromedriver.exe')

    page = 1
    while True:
        storeList = getStores2(driver, page)
        if storeList == None: break;

        for store in storeList:
            outfile.write(u'페리카나치킨|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1

        if page == 999: break       # 2019년1월 기준 114까지 있음
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2019/1)
def getStores2(browser_driver, intPageNo):
    # 'https://www.pelicana.co.kr/store/stroe_search.html?page=3&branch_name=&gu=&si='
    url = 'https://www.pelicana.co.kr'
    api = '/store/stroe_search.html'
    data = {
        'branch_name': '',
        'si': '',
        'gu': '',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    urls = url + api + '?' + params
    print(urls)  # for debugging

    browser_driver.get(urls)
    delay = 0
    browser_driver.implicitly_wait(delay)
    response = browser_driver.page_source
    #print(response)
    tree = html.fromstring(response)

    # 반환되는 값 중간에 이상한 문자들이 포함되어 있어 전체 결과를 엉망으로 만듦, 그래서 아래와 같이 이상한 문자들이 있는 부분을 제거
    idx = response.find('where a_si')
    tempresponse = response[:idx]
    response = response[idx:]
    idx = response.find('group by a_si')
    tempresponse += response[idx:]
    response = tempresponse
    #print(response)

    # 이상한 값 또 들어가 있어서 또 지움 ㅠㅠ (2017/7/10)   '032-887-9292<br/>E���� - 032-885-4658</td>' 이런 문자열 있음 => '032-887-9292</td>' 이렇게 고침
    idx = response.find('032-887-9292<br/>')
    if idx != -1:
        tempresponse = response[:idx+12]
        response = response[idx:]
        idx = response.find('</td>')
        tempresponse += response[idx:]
        response = tempresponse

    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//table[@class="table mt20"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 최소 4개 필드 있어야

        storeInfo = {}
        subname = "".join(infoList[0].itertext()).strip('\r\t\n')
        idx = subname.find('(')
        if idx != -1: subname = subname[:idx].rstrip()
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['newaddr'] = ''
        strtemp = "".join(infoList[1].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        storeInfo['pn'] = '';
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None:
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-')
            if storeInfo['pn'] == '--': storeInfo['pn'] = ''

        strtemp2 = infoList[2].text
        if strtemp2 != None:
            strtemp2 = strtemp2.rstrip().lstrip().replace('.', '-')
            if strtemp != strtemp2 and len(strtemp) > len(strtemp2):    # 전화번호가 2개 이상 있는 경우라면
                strtemp = strtemp[len(strtemp2):].lstrip()
                strtemp2 += ';';    strtemp2 += strtemp
                storeInfo['pn'] = strtemp2

        storeInfo['xcoord'] = '';   storeInfo['ycoord'] = ''
        other_info_list = infoList[3].xpath('.//a/@onclick')

        if len(other_info_list) < 1:
            storeList += [storeInfo]
            continue

        coords_info = other_info_list[0]
        idx = coords_info.find('view(')
        coords_info = coords_info[idx+5:]
        token_list = coords_info.split(',')

        if len(token_list) < 2:
            storeList += [storeInfo]
            continue

        storeInfo['xcoord'] = token_list[0].replace('\'', '').replace(' ', '')
        storeInfo['ycoord'] = token_list[1].replace('\'', '').replace(' ', '')

        storeList += [storeInfo]

    return storeList

# v1.0
def getStores(intPageNo):
    # 'https://www.pelicana.co.kr/store/stroe_search.html?page=3&branch_name=&gu=&si='
    url = 'https://www.pelicana.co.kr'
    api = '/store/stroe_search.html'
    data = {
        'branch_name': '',
        'si': '',
        'gu': '',
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    params = 'page=' + str(intPageNo) + '&branch_name=&gu=&si='
    # print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.3.12011320.1543944638; PHPSESSID=c86eeed4494b28dc0c7088e96d1cd3e8; _gid=GA1.3.291320396.1547019701; _gat=1',
        'Upgrade-Insecure-Requests': '`',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)

        #req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        #req.get_method = lambda: 'GET'
        #result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #response = response.decode('utf-8')
    #response = unicode(response, 'euc-kr')

    # 반환되는 값 중간에 이상한 문자들이 포함되어 있어 전체 결과를 엉망으로 만듦, 그래서 아래와 같이 이상한 문자들이 있는 부분을 제거
    idx = response.find('where a_si')
    tempresponse = response[:idx]
    response = response[idx:]
    idx = response.find('group by a_si')
    tempresponse += response[idx:]
    response = tempresponse
    #print(response)

    # 이상한 값 또 들어가 있어서 또 지움 ㅠㅠ (2017/7/10)   '032-887-9292<br/>E���� - 032-885-4658</td>' 이런 문자열 있음 => '032-887-9292</td>' 이렇게 고침
    idx = response.find('032-887-9292<br/>')
    if idx != -1:
        tempresponse = response[:idx+12]
        response = response[idx:]
        idx = response.find('</td>')
        tempresponse += response[idx:]
        response = tempresponse

    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//table[@class="table mt20"]//tbody//tr'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        infoList = entityList[i].xpath('.//td')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 최소 4개 필드 있어야

        storeInfo = {}
        subname = "".join(infoList[0].itertext()).strip('\r\t\n')
        idx = subname.find('(')
        if idx != -1: subname = subname[:idx].rstrip()
        storeInfo['subname'] = subname.rstrip().lstrip().replace(' ', '/')

        storeInfo['newaddr'] = ''
        strtemp = "".join(infoList[1].itertext()).strip('\r\t\n')
        if strtemp != None: storeInfo['newaddr'] = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        storeInfo['pn'] = '';
        strtemp = "".join(infoList[2].itertext()).strip('\r\t\n')
        if strtemp != None:
            storeInfo['pn'] = strtemp.rstrip().lstrip().replace('.', '-')
            if storeInfo['pn'] == '--': storeInfo['pn'] = ''

        strtemp2 = infoList[2].text
        if strtemp2 != None:
            strtemp2 = strtemp2.rstrip().lstrip().replace('.', '-')
            if strtemp != strtemp2 and len(strtemp) > len(strtemp2):    # 전화번호가 2개 이상 있는 경우라면
                strtemp = strtemp[len(strtemp2):].lstrip()
                strtemp2 += ';';    strtemp2 += strtemp
                storeInfo['pn'] = strtemp2

        storeInfo['xcoord'] = '';   storeInfo['ycoord'] = ''
        other_info_list = infoList[3].xpath('.//a/@onclick')

        if len(other_info_list) < 1:
            storeList += [storeInfo]
            continue

        coords_info = other_info_list[0]
        idx = coords_info.find('view(')
        coords_info = coords_info[idx+5:]
        token_list = coords_info.split(',')

        if len(token_list) < 2:
            storeList += [storeInfo]
            continue

        storeInfo['xcoord'] = token_list[0].replace('\'', '').replace(' ', '')
        storeInfo['ycoord'] = token_list[1].replace('\'', '').replace(' ', '')

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
