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


area_dict = {
    9: '서울 강남',     # 1
    10: '서울 강북',    # 1
}

# 하위 지역명까지 검색하면 더 많이 얻어올 수 있음... (그럴까???)
area_dict2 = {
    1: '강원',    # 2 ~
    2: '경기',
    3: '경남',
    4: '경북',
    5: '광주',
    6: '대구',
    7: '대전',
    8: '부산',
    9: '서울 강남',     # 1
    10: '서울 강북',    # 1
    11: '울산',   # 3 ~
    12: '인천',
    13: '전남',
    14: '전북',
    15: '제주',
    16: '충남',
    17: '충북',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('siksin1_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ID|NEWADDR|ADDR|TYPE|ORGNAME|SOURCE2@@식신맛집\n")

    driver = webdriver.Chrome('C:\chromedriver.exe')

    for area_code in sorted(area_dict):
        page = 1
        while True:
            store_list = getStores(driver, area_code, page)
            if store_list == None: break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['orgname'])
                outfile.write(u'%s\n' % u'식신')

            page += 1

            if page == 99: break
            elif len(store_list) < 30: break

            time.sleep(random.uniform(1, 2))

        time.sleep(random.uniform(2, 4))

    outfile.close()

def getStores(browser_driver, area_code, intPageNo):
    # 'https://www.siksinhot.com/taste?upHpAreaId=10&hpAreaId=&isBestOrd=Y'
    url = 'https://www.siksinhot.com'
    api = '/taste'
    data = {
        #'upHpAreaId': '10',
        'hpAreaId': '',
        'isBestOrd': 'Y',
    }
    data['upHpAreaId'] = area_code
    data['idx'] = (intPageNo-1)*30
    params = urllib.urlencode(data)
    print('%d : %d' % (area_code, intPageNo))  # for debugging

    urls = url + api + '?' + params
    browser_driver.get(urls)
    delay = 3
    browser_driver.implicitly_wait(delay)

    response = browser_driver.page_source
    #print(response)
    idx = response.find('[{"pid"')
    contents = ''
    if idx != -1:
        contents = response[idx:]
        idx = contents.find('}],"api"')
        if idx != -1:
            contents = contents[:idx+2]
            #print(contents)
            entity_list = json.loads(contents)

    if contents == '': return None

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = ''
        strtemp = entity_list[i]['pname'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['subname'] = ''
        store_info['name'] = strtemp.replace(' ', '/')

        store_info['addr'] = entity_list[i]['addr']
        store_info['newaddr'] = entity_list[i]['addr2']
        store_info['pn'] = ''
        store_info['id'] = entity_list[i]['pid']
        store_info['type'] = entity_list[i]['hpSchCateNm']

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
