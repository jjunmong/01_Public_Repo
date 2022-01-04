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

    outfile = codecs.open('fsb_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|NEWADDR|FEAT@@저축은행\n")

    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['feat'])

        page += 1

        if page == 2: break     # 한번 호출로 전국점포 정보 모두 얻을 수 있음
        elif len(store_list) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(intPageNo):
    # 'https://www.fsb.or.kr/bank/finding_bank.do
    url = 'https://www.fsb.or.kr'
    api = '/bank/finding_bank.do'
    data = {
    }
    params = urllib.urlencode(data)
    # print(params)

    try:
        #urls = url + api + '?' + params
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

    entity_list = tree.xpath('//dl[@class="srhBankSt step2"]//ul//li')

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = ''
        store_info['subname'] = ''
        strtemp = "".join(entity_list[i].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').replace('선택됨', '').rstrip().lstrip()
            idx = strtemp.find('[')
            if idx != -1:
                store_info['name'] = strtemp[:idx].rstrip()
                if not store_info['name'].endswith('은행'): store_info['name'] += '저축은행'
                strtemp = strtemp[idx+1:].replace(']', '').lstrip().rstrip()
                if strtemp.startswith('(출)'): strtemp = strtemp[3:].lstrip() + '출장소'
                elif strtemp.endswith('영업부'): pass
                elif strtemp.endswith('출장소'): pass
                elif not strtemp.endswith('점'): strtemp += '지점'
                store_info['subname'] = strtemp.replace(' ', '/')
            else:
                store_info['name'] = strtemp
                if not store_info['name'].endswith('은행'): store_info['name'] += '저축은행'


                idx = strtemp.find(']')
                if idx != -1:
                    strtemp = strtemp[idx+1:].lstrip()

        store_info['id'] = ''
        store_info['addr'] = ''
        store_info['newaddr'] = ''
        store_info['pn'] = ''
        store_info['feat'] = ''

        temp_list = entity_list[i].xpath('.//a/@onclick')
        if len(temp_list) < 1:
            store_list += [store_info];     continue

        strtemp = temp_list[0].lstrip().rstrip()      # 'bankInfo('318','fb058');
        idx = strtemp.find('bankInfo(')
        if idx == -1:
            store_list += [store_info];     continue

        temp_list = strtemp[idx+9:-2].lstrip().rstrip().split(',')
        if len(temp_list) < 2:
            store_list += [store_info];     continue

        store_id = temp_list[0][1:-1]
        store_key = temp_list[1][1:-1]
        store_info['id'] = store_id

        suburls = 'https://www.fsb.or.kr/bank/finding_bank.do'
        subdata = {
            'areaCode': '',
            'type': '1',
            'queryType': 'bank_name',
            'queryWord': '',
        }
        subdata['seq'] = store_id
        subdata['bank_code'] = store_key
        subparams = urllib.urlencode(subdata)
        print(subparams)

        try:
            time.sleep(random.uniform(0.3, 0.9))
            subreq = urllib2.Request(suburls, subparams)
            # subreq = urllib2.Request(suburls, subparams, headers=hdr)
            subreq.get_method = lambda: 'POST'
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the subAPI');
            store_list += [store_info];
            continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % code);
            store_list += [store_info];
            continue

        subresponse = subresult.read()
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        subinfo_list = subtree.xpath('//dd[@class="pRight"]//ul//li')

        for j in range(len(subinfo_list)):
            strtemp = "".join(subinfo_list[j].itertext())
            if strtemp != None:
                strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if strtemp.startswith('전화번호'):
                    strtemp = strtemp[4:].replace(':', '').lstrip().rstrip()
                    idx = strtemp.find('/')
                    if idx != -1:
                        strtemp = strtemp[:idx].rstrip()
                    store_info['pn'] = strtemp
                elif strtemp.startswith('지번주소'):
                    strtemp = strtemp[4:].replace(':', '').lstrip().rstrip()
                    store_info['addr'] = strtemp
                elif strtemp.startswith('도로명주소'):
                    strtemp = strtemp[5:].replace(':', '').lstrip().rstrip()
                    store_info['newaddr'] = strtemp

        tag_list = subtree.xpath('//div[@class="dlType"]//dt')
        value_list = subtree.xpath('//div[@class="dlType"]//dd')

        for j in range(len(tag_list)):
            str_tag = "".join(tag_list[j].itertext())
            str_value = "".join(value_list[j].itertext())
            if str_tag != None and str_value != None:
                str_tag = str_tag.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                str_value = str_value.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
                if str_tag == '자동화기기':
                    if store_info['feat'] != '': store_info['feat'] += ';'
                    store_info['feat'] += str_value
                elif str_value != '불가능':
                    if store_info['feat'] != '': store_info['feat'] += ';'
                    store_info['feat'] += str_tag

        store_list += [store_info]

    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
