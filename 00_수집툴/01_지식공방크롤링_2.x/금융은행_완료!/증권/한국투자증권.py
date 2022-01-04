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
from selenium import webdriver
import bs4

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

    outfile = codecs.open('hangook_investock_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|NEWADDR@@한국투자증권\n")

    driver = webdriver.Chrome('C:\chromedriver.exe')

    page = 1
    while True:
        store_list = getStores(driver, page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['newaddr'])

        page += 1

        if page == 19: break     # 2018년4월30일 기준 9까지 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(browser_driver, intPageNo):
    urls = 'https://www.truefriend.com/main/customer/guide/branch/branch.jsp?cmd=branch_listed_default&currentPage=' + str(intPageNo)
    print(urls)

    #browser_driver = webdriver.Chrome('C:\Python27\chromedriver.exe')
    browser_driver.get(urls)
    delay = 3
    browser_driver.implicitly_wait(delay)

    response = browser_driver.page_source
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="tableDefault"]//tbody//tr')

    store_list = []
    for i in range(0, len(entity_list), 2):

        info_list = entity_list[i].xpath('.//td')
        addr_list = entity_list[i+1].xpath('.//td')
        if len(info_list) < 4 or len(addr_list) < 1: continue  # 최소 필드 수 체크

        store_info = {}

        store_info['name'] = '한국투자증권'
        store_info['subname'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            strtemp = strtemp.replace('일반업무', '').replace('처리불가', '').replace('*', '').rstrip().lstrip()
            if strtemp.endswith('센터'): pass
            elif strtemp.endswith('점'): pass
            else: strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_info['id'] = ''
        temp_list = info_list[3].xpath('.//a/@href')
        if len(temp_list) > 0:
            strtemp = temp_list[0]
            idx = strtemp.find('doView(')
            if idx != -1:
                strtemp = strtemp[idx+7:]
                idx = strtemp.find(')')
                strtemp = strtemp[:idx].lstrip().rstrip()[1:-1]
                store_info['id'] = strtemp

        store_info['addr'] = ''
        strtemp = "".join(addr_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            strtemp = strtemp.replace('(구주소)', '').rstrip().lstrip()
            store_info['addr'] = strtemp

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
