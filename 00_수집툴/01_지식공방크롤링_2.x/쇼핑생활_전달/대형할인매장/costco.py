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

    outfile = codecs.open('costco_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|NEWADDR|OT|FEAT|XCOORD|YCOORD\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'코스트코|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        page += 1
        if page == 2: break     # 한 페이지에 전국 점포정보 다 있음
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# v2.0 (2018/2)
def getStores(intPageNo):
    url = 'https://www.costco.co.kr'
    api = '/store-finder/search'
    data = {
        'q': 'Korea, Republic of',
        'page': '0',
    }
    params = urllib.urlencode(data)
    print(params)

    try:
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    response_json = json.loads(response)  # json 포맷으로 결과값 반환
    entity_list = response_json['data']

    store_list = []
    for i in range(len(entity_list)):

        store_info = {}

        store_info['name'] = '코스트코'
        store_info['subname'] = entity_list[i]['displayName'].lstrip().rstrip().replace(' ', '')

        store_info['newaddr'] = entity_list[i]['line1']
        if entity_list[i].get('line2'):
            store_info['newaddr'] += ' ' + entity_list[i]['line2']

        store_info['pn'] = entity_list[i]['phone'].lstrip().rstrip().replace('+82-', '').replace(' ', '-')

        store_info['xcoord'] = entity_list[i]['longitude']
        store_info['ycoord'] = entity_list[i]['latitude']

        store_info['ot'] = ''
        store_info['feat'] = ''
        feat_list = entity_list[i]['features']
        for j in range(len(feat_list)):
            if j != 0: store_info['feat'] += ';'
            store_info['feat'] += feat_list[j]

        store_list += [store_info]

    return store_list


'''
# v1.0
def getStores(intPageNo):
    url = 'https://www.costco.co.kr'
    api = '/store-finder'
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
    tree = html.fromstring(response)

    entity_list = tree.xpath('//div[@class="store-list"]//li/a')

    result_list = []
    for i in range(len(entity_list)):
        temp_list = entity_list[i].xpath('./@code')
        if len(temp_list) == 0: continue

        shop_code = temp_list[0]
        subname = entity_list[i].text

        subdata = {}
        subdata['code'] = shop_code
        subparams = urllib.urlencode(subdata)

        try:
            suburl = url + '/store-finder/store' + '?' + subparams
            print(suburl)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburl)
        except:
            print('Error calling the suburl');      continue

        code = subresult.getcode()
        if code != 200:
            print('suburl HTTP request error (status %d)' % code);      continue

        subresponse = subresult.read()
        #print(subresponse)
        subresponse_json = json.loads(subresponse)
        shop_dic = subresponse_json['data'][0]

        store_info = {}
        store_info['subname'] = subname.lstrip().rstrip().replace(' ', '/')

        store_info['pn'] = shop_dic['phone'].replace('+82-', '').replace('.', '-').replace(')', '-')
        store_info['newaddr'] = shop_dic['line1'] + ' ' + shop_dic['line2']
        store_info['xcoord'] = shop_dic['longitude']
        store_info['ycoord'] = shop_dic['latitude']
        store_info['ot'] = shop_dic['openings'][''].replace(' ', '')

        store_info['feat'] = ''
        feat_list = shop_dic['features']

        for j in range(len(feat_list)):
            if j != 0: store_info['feat'] += ';'
            store_info['feat'] += feat_list[j]

        result_list += [store_info]

    return result_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
