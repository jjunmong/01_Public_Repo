# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: sheayun
'''

import sys
import time
import random
import urllib
import codecs
from lxml import html

featClasses = {
    'sevice01': u'24시간',
    'sevice02': u'택배',
    'sevice03': u'베이커리',
    'sevice04': u'튀김',
    'sevice05': u'커피',
    'sevice06': u'로또',
    'sevice07': u'스포츠토토',
    'sevice08': u'ATM',
}


def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    page = 1

    outfile = codecs.open('cu_utf8.txt', 'a', 'utf-8')

    if page == 1:
        outfile.close()
        outfile = codecs.open('cu_utf8.txt', 'w', 'utf-8')
        outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|ID|FEAT@@CU\n")

    while True:
        store_list = getStores(page)
        if store_list == None: break;
        elif len(store_list) == 0: break

        for store in store_list:
            outfile.write(u'CU|')
            store_subname = store['name'].lstrip().rstrip().replace(' ', '/')
            outfile.write(u'%s|' % store_subname)

            store_pn = store['pn'].lstrip().rstrip().replace('.', '-').replace(')', '-')
            outfile.write(u'%s|' % store_pn)

            outfile.write(u'%s|' % store['addr'])

            store_newaddr = store['newaddr'].lstrip().rstrip()
            outfile.write(u'%s|' % store_newaddr)

            outfile.write(u'%s|' % store['id'])

            store_feat = ''
            for c in sorted(featClasses):
                if store[c] == True:
                    if store_feat != '': store_feat += ';'
                    store_feat += featClasses[c]
            outfile.write(u'%s\n' % store_feat)

        page += 1
        time.sleep(random.uniform(0.3, 0.9))

        if page == 9999: break

    outfile.close()


def getStores(pageIndex):

    url = 'http://cu.bgfretail.com'
    api = '/store/list_Ajax.do'

    tableSelector = '//div[@id="dataTable"]//table'
    nameSelector = '//span[@class="name"]'
    telSelector = '//span[@class="tel"]'
    addrSelector = '//div[@class="detail_info"]/address/a'
    svcSelector = '//div[@class="detail_info"]/ul'

    data = {
        'listType': '',
        'jumpoCode': '',
        'jumpoLotto': '',
        'jumpoToto': '',
        'jumpoCash': '',
        'jumpoHour': '',
        'jumpoCafe': '',
        'jumpoDelivery': '',
        'jumpoBakery': '',
        'jumpoFry': '',
        'jumpoAdderss': '',
        'jumpoSido': '',
        'jumpoGugun': '',
        'jumpodong': ''
    }
    data['pageIndex'] = pageIndex

    params = urllib.urlencode(data)
    print(url+api+'?'+params)    # for debugging

    try:
        result = urllib.urlopen(url + api, params)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)     # for debugging
    tree = html.fromstring(response)

    dataTable = tree.xpath(tableSelector)[0]
    names = dataTable.xpath(nameSelector)
    tels = dataTable.xpath(telSelector)
    addrs = dataTable.xpath(addrSelector)

    storeList = []

    for i in range(len(names)):
        storeInfo = {}
        storeInfo['name'] = names[i].text or ''

        storeInfo['pn'] = tels[i].text or ''
        storeInfo['newaddr'] = addrs[i].text or ''

        storeInfo['addr'] = '';     storeInfo['id'] = ''
        temp_list = addrs[i].xpath('./@onclick')
        if len(temp_list) > 0:
            strtemp = temp_list[0]      # searchLatLng('전라북도 군산시 소룡동 1589-1번지', '11610'); return false;
            if strtemp != None:
                idx = strtemp.find('LatLng(')
                if idx != -1:
                    strtemp = strtemp[idx+7:]
                    idx = strtemp.find(');')
                    if idx != -1:
                        info_list = strtemp[:idx].split('\',')      # ''인천광역시 남구 도화2,3동 706-3번지', '26645' <= 주소에 ','가 있는 경우가 있어서 '\','로 쪼갬 ㅠㅠ
                        if len(info_list) > 0: storeInfo['addr'] = info_list[0].lstrip().rstrip()[1:]
                        if len(info_list) > 1: storeInfo['id'] = info_list[1].lstrip().rstrip()[1:-1]

        for c in sorted(featClasses):
            svc = dataTable.xpath(svcSelector)
            feat = svc[0].xpath('//li[contains(@class, "%s")]/@class' % c)[i]
            if feat[-2:] == 'on':
                storeInfo[c] = True
            else:
                storeInfo[c] = False

        if storeInfo['newaddr'] == '' and storeInfo['addr'] == '' and storeInfo['id'] != '':
            suburl = 'http://cu.bgfretail.com/store/view.do?jumpo=' + storeInfo['id']
            time.sleep(random.uniform(0.3, 0.9))
            try:
                print(suburl)  # for debugging
                subresult = urllib.urlopen(suburl)
            except:
                print('Error calling the suburl');
                storeList += [storeInfo]
                continue

            code = subresult.getcode()
            if code != 200:
                print('suburl HTTP request error (status %d)' % code);
                storeList += [storeInfo]
                continue

            subresponse = subresult.read()
            #print(subresponse)
            subtree = html.fromstring(subresponse)

            subinfo_list = subtree.xpath('//ul[@class="storeInfo"]')
            for j in range(len(subinfo_list)):
                value_list = subinfo_list[j].xpath('.//li')

                if len(value_list) < 3: break

                strtemp = "".join(value_list[0].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                    if strtemp.startswith('도로명'): strtemp = strtemp[3:].lstrip()
                    if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
                    storeInfo['newaddr'] = strtemp

                strtemp = "".join(value_list[1].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                    if strtemp.startswith('지번'): strtemp = strtemp[2:].lstrip()
                    if strtemp.startswith('주소'): strtemp = strtemp[2:].lstrip()
                    storeInfo['addr'] = strtemp

                strtemp = "".join(value_list[2].itertext())
                if strtemp != None:
                    strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
                    if strtemp.startswith('연락처'): strtemp = strtemp[3:].lstrip()
                    storeInfo['pn'] = strtemp.replace('.', '-').replace(')', '-')

                break

        storeList += [storeInfo]

    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
