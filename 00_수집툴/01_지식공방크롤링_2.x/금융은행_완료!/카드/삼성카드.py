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

    outfile = codecs.open('samsung_card_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@삼성카드\n")

    driver = webdriver.Chrome('C:\chromedriver.exe')

    page = 1
    while True:
        store_list = getStores(driver, page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 2: break     # 한번 호출로 모든 지점 정보 얻을 수 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(browser_driver, intPageNo):
    urls = 'https://www.samsungcard.com/personal/customer-service/infomation/UHPPCC0251M0.jsp?click=gnb_customer_informaiton'
    print(urls)

    #browser_driver = webdriver.Chrome('C:\Python27\chromedriver.exe')
    browser_driver.get(urls)
    delay = 3
    browser_driver.implicitly_wait(delay)

    response = browser_driver.page_source
    #print(response)
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="link_info"]')

    store_list = []
    for i in range(0, len(entity_list), 1):

        name_list = entity_list[i].xpath('.//p')
        info_list = entity_list[i].xpath('.//dd')
        if len(name_list) < 1 or len(info_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}

        store_info['name'] = '삼성카드'
        store_info['subname'] = ''
        store_info['feat'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.find('바로발급') != -1:
                store_info['feat'] = '바로발급'
                strtemp = strtemp.replace('바로발급', '').rstrip().lstrip()

            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['newaddr'] = ''
        strtemp = "".join(info_list[1].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            store_info['newaddr'] = strtemp

        store_info['pn'] = ''
        strtemp = "".join(info_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
