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
#import json
from lxml import html

sido_sggcount2 = {
    2: 16,
}

sido_sggcount = {
    1: 25,
    2: 16,
    3: 8,
    4: 10,
    5: 5,
    6: 5,
    7: 5,
    8: 12,
    9: 44,
    10: 18,
    11: 13,
    12: 17,
    13: 15,
    14: 22,
    15: 24,
    16: 22,
    17: 2,
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('kyochonchicken_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR@@교촌치킨\n")

    for idx in sido_sggcount:

        page = 1
        while page <= sido_sggcount[idx]:
            storeList = getStores2(idx, page)
            if storeList == None:
                page += 1;      continue
            elif len(storeList) == 0:
                page += 1;      continue

            for store in storeList:
                outfile.write(u'교촌치킨|')
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['newaddr'])

            page += 1

            if page == 999: break
            #elif len(storeList) < 10: break

            time.sleep(random.uniform(0.3, 0.9))

        time.sleep(random.uniform(1, 2))

    outfile.close()

# v2.0 (2019/1)
def getStores2(sido_code, intPageNo):
    url = 'http://www.kyochon.com'
    api = '/shop/domestic.asp'
    data = {
        'txtsearch': '',
    }
    data['sido1'] = sido_code
    data['sido2'] = intPageNo

    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API')
        return None

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@class="shopSchList"]//li/a'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        subname_info = entityList[i].xpath('.//span[@class="store_item"]//strong')
        if len(subname_info) < 1: continue

        subname = "".join(subname_info[0].itertext())
        if subname == None: continue
        subname = subname.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

        storeInfo = {}
        subname = subname.rstrip().lstrip()
        if subname.endswith(')'): pass
        elif not subname.endswith('점'): subname += '점'
        storeInfo['subname'] = subname.replace(' ', '/')

        storeInfo['addr'] = ''; storeInfo['newaddr'] = ''; storeInfo['pn'] = ''
        other_info_list = entityList[i].xpath('.//em')

        if len(other_info_list) < 1: continue

        other_info = "".join(other_info_list[0].itertext())
        if other_info == None:
            storeList += [storeInfo];   continue

        other_info = other_info.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

        idx = other_info.find('(')
        if idx != -1:
            storeInfo['addr'] = other_info[:idx].rstrip()
            other_info = other_info[idx+1:].lstrip()
            idx = other_info.rfind(')')
            if idx != -1:
                strtemp = other_info[:idx].rstrip()
                if strtemp.find(')(') != -1:
                    idx2 = strtemp.find(')(')
                    storeInfo['addr'] += ' (' + strtemp[:idx2+1]
                    storeInfo['newaddr'] = strtemp[idx2+2:].lstrip()
                else: storeInfo['newaddr'] = strtemp

                other_info = other_info[idx + 1:].lstrip()
                storeInfo['pn'] = other_info.replace(' ', '')

        storeList += [storeInfo]

    return storeList


# v1.0
def getStores(sido_code, intPageNo):
    url = 'http://www.kyochon.com'
    api = '/shop/domestic.asp'
    data = {
        'txtsearch': '',
    }
    data['sido1'] = sido_code
    data['sido2'] = intPageNo

    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API')
        return None

    code = result.getcode()
    if code != 200:
        #errExit('HTTP request error (status %d)' % code)
        print('HTTP request error (status %d)' % code)
        return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)
    ##tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entitySelector = '//div[@class="shopSchList"]//li/a'
    entityList = tree.xpath(entitySelector)

    storeList = []
    for i in range(len(entityList)):
        subname_info = entityList[i].xpath('.//dt')
        if len(subname_info) < 1: continue

        subname = subname_info[0].text
        if subname == None: continue

        storeInfo = {}
        subname = subname.rstrip().lstrip()
        if subname.endswith(')'): pass
        elif not subname.endswith('점'): subname += '점'
        storeInfo['subname'] = subname.replace(' ', '/')

        storeInfo['addr'] = ''; storeInfo['newaddr'] = ''; storeInfo['pn'] = ''
        other_info_list = entityList[i].xpath('.//dd')

        if len(other_info_list) < 1: continue

        other_info = "".join(other_info_list[0].itertext()).strip('\r\t\n')
        #other_info = other_info_list[0].text
        if subname == None:
            storeList += [storeInfo];   continue

        other_info = other_info.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')

        idx = other_info.find('(')
        if idx != -1:
            storeInfo['addr'] = other_info[:idx].rstrip()
            other_info = other_info[idx+1:].lstrip()
            idx = other_info.rfind(')')
            if idx != -1:
                strtemp = other_info[:idx].rstrip()
                if strtemp.find(')(') != -1:
                    idx2 = strtemp.find(')(')
                    storeInfo['addr'] += ' (' + strtemp[:idx2+1]
                    storeInfo['newaddr'] = strtemp[idx2+2:].lstrip()
                else: storeInfo['newaddr'] = strtemp

                other_info = other_info[idx + 1:].lstrip()
                storeInfo['pn'] = other_info.replace(' ', '')

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
