# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import codecs
import urllib
import urllib2,cookielib
import json
import time
import random
import Tkinter
import tkFileDialog

from lxml import html

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    Tkinter.Tk().withdraw()  # Close the root window

    opts = {}
    opts['filetypes'] = [('txt files', '.txt'), ('all files', '.*')]
    opts['initialfile'] = 'input.txt'
    opts['title'] = 'select input file'

    #infilename = tkFileDialog.askopenfilename(**opts)
    #print infilename

    opts['initialfile'] = 'output.txt'
    opts['title'] = 'select output file'
    #outfilename = tkFileDialog.asksaveasfilename(**opts)
    #print outfilename

    #infile = open(infilename, 'r')
    #outfile = open(outfilename, 'w')

    while True:

        #line = infile.readline()
        #if not line: break;

        # convert ANSI to UTF-8
        #line = unicode(line, "cp949").encode("utf-8")
        #line = line.strip('\n\t\r')

        #itemList = GetItemList(line)
        #query_code = itemList[0]
        #qurey_address = itemList[1]

        query_word = '';   query_category = "";     query_category2 = "";   query_category3 = "";
        query_word = '코텔 숙박'
        query_category = ''
        query = query_word

        outfile = codecs.open('kotel_utf8.txt', 'w', 'utf-8')
        outfile.write("##NAME|SUBNAME|TELNUM|CAT|ADDR|NEWADDR|KATECX|KATECY@@코텔\n")

        page = 1
        while True:
            store_list = getQueryResult(query, query_category, query_category2, query_category3, page)
            if store_list == None: break;

            for store in store_list:
                if store['name'] == 'xxx': continue
                #if store['category'].find(query_category) != -1: pass
                #else: continue

                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['category'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])

            page += 1

            if page == 9: break
            elif len(store_list) < 30:
                break

            time.sleep(random.uniform(0.3, 0.9))

        outfile.close()
        break


def getQueryResult(query, req_category, req_category2, req_category3, page_no):
    url = 'https://openapi.naver.com'
    api = '/v1/search/local.xml'

    data = {
        'display': 30,
        #'start': 1,
        'sort': 'random'
        #'X-Naver-Client-Id': '0xJFo47EAUOFvSnr4ccm',
        #'X-Naver-Client-Secret': '353X0spbNW',
    }
    data['start'] = (page_no-1)*30 + 1
    #data['query'] = '서울특별시 강남구 청담동 100-14'     # 이렇게 입력하면 아무 결과도 반환하지 않음
    #data['query'] = '도산대로 536 호텔'      # 이렇게 입력하면 주소로 처리됨
    # data['query'] = '호텔 도산대로 536'     # 이렇게 입력하면 결과 반환
    data['query'] = query

    params = urllib.urlencode(data)
    #print(params)

    urls = url + api + '?' + params
    print(urls)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'X-Naver-Client-Id': '0VCqkhk9tqO2b1AO44RQ',
        'X-Naver-Client-Secret': 'ME7758VQWx',
    }

    try:
        req = urllib2.Request(urls, headers=hdr)
        result = urllib2.urlopen(req)

        # result = urllib.urlopen(urls)
        # result = urllib.urlopen(url + api, params)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        response = result.read()
        #print(response)
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    print(response)

    tree = html.fromstring(response)

    tableSelector = '//channel'
    dataTable = tree.xpath(tableSelector)[0]

    nameSelector = '//item//title'
    catSelector = '//item//category'
    telnumSelector = '//item//telephone'
    addrSelector = '//item//address'
    newaddrSelector = '//item//roadaddress'    # 결과에는 <roadAddress> 라고 되어 있는데 여기서는 소문자로 표기해야 함 (태그를 전부 다 소문자로 정규화하는 듯...)
    mapxSelector = '//item//mapx'
    mapySelector = '//item//mapy'

    nameList = dataTable.xpath(nameSelector)
    catList = dataTable.xpath(catSelector)
    telnumList = dataTable.xpath(telnumSelector)
    addrList = dataTable.xpath(addrSelector)
    newaddrList = dataTable.xpath(newaddrSelector)
    mapxList = dataTable.xpath(mapxSelector)
    mapyList = dataTable.xpath(mapySelector)

    store_list = []

    for i in range(len(nameList)):
        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''

        strtemp = "".join(nameList[i].itertext())  # 내용 중 tag는 빼고 text만 기록 (<b></b> 태그 남음
        #strtemp = strtemp.replace('<b>', '').replace('착한빵집', '').lstrip().rstrip()
        strtemp = strtemp.replace('<b>', '').replace('</b>', '').lstrip().rstrip()

        if not strtemp.startswith('코텔'):
            store_info['name'] = 'xxx'
            store_list += [store_info]
            continue

        if strtemp.startswith('코텔야자'):
            store_info['name'] = '코텔야자'
            store_info['subname'] = strtemp[4:].lstrip().replace(' ', '/')
        else:
            store_info['name'] = '코텔'
            store_info['subname'] = strtemp[2:].lstrip().replace(' ', '/')

        #store_info['name'] = poiInfo['name'].replace('<b>', '').replace('</b>', '')
        #store_info['name'] = nameList[i].text or ''
        store_info['category'] = catList[i].text or ''
        store_info['pn'] = telnumList[i].text or ''
        store_info['addr'] = addrList[i].text or ''
        store_info['newaddr'] = newaddrList[i].text or ''
        store_info['xcoord'] = mapxList[i].text or ''
        store_info['ycoord'] = mapyList[i].text or ''

        store_list += [store_info]

    return store_list


def GetItemList(strSourceAddr):
    #            0     1                     2                          3
    #tempstr = u'11102,서울 종로구 낙원동 75,서울 종로구 삼일대로26길 7,호텔에메랄드'
    tempstr = strSourceAddr

    words = {}
    words = tempstr.split(',')

    wordslen = len(words)

    if(wordslen < 3):
        result_item_list = []
        result_item_list.append('')
        result_item_list.append('')
        result_item_list.append('')
        result_item_list.append('')
        return result_item_list

    if(wordslen < 4):
        result_item_list = []
        result_item_list.append(words[0])
        result_item_list.append(words[1])
        result_item_list.append(words[2])
        result_item_list.append('')
        return result_item_list

    result_item_list = []
    result_item_list.append(words[0])
    result_item_list.append(words[1])
    result_item_list.append(words[2])
    result_item_list.append(words[3])

    return result_item_list



def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
