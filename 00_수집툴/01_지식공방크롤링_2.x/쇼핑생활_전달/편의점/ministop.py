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

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('ministop_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|FEAT@@미니스톱\n")

    sidocode = 1
    while True:
        storeList = getStores(sidocode)
        if len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'미니스톱|')
            info_list = store['fields']
            outfile.write(u'%s|' % info_list[0])
            outfile.write(u'%s|' % info_list[2])
            outfile.write(u'%s|' % info_list[1])
            if info_list[3] == '1': outfile.write(u'소프트크림\n')
            else: outfile.write(u'\n')

        sidocode += 1

        if sidocode == 18:
            break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(sidocode):
    url = 'https://www.ministop.co.kr'
    api = '/MiniStopHomePage/page/querySimple.do'
    data = {
        'pageId': 'store/store',
        'sqlnum': 3,    # 뭔지 모르겠음
        'pageNum': 1,
        'sortGu': '',
        'tm': ''
    }
    data['paramInfo'] = str(sidocode) + ':'

    params = urllib.urlencode(data)
    #print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)

    receivedData = json.loads(response)     # json 포맷으로 결과값 반환

    if receivedData.get('recordList'): storeList = receivedData['recordList']
    else: storeList = []

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
