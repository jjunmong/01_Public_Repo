# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: sheayun (updated by jskyun)
'''

import sys
import time
import codecs
import urllib
import random
import json

sidocode_list2 = {
    '02': 'kwangju'
}

sidocode_list = {
    '01': 'seoul',
    '02': 'kwangju',
    '03': 'daegu',
    '04': 'daejeon',
    '05': 'busan',
    '06': 'ulsan',
    '07': 'incheon',
    '08': 'gyenggi',
    '09': 'gangwon',
    '10': 'kyungnam',
    '11': 'kyungbuk',
    '12': 'jeonnam',
    '13': 'jeonbuk',
    '14': 'chungnam',
    '15': 'chungbuk',
    '16': 'jeju',
    '17': 'sejong',
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('starbucks_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ID|ADDR|NEWADDR|FEAT|SINCE|XCOORD|YCOORD@@스타벅스\n")

    for sidocode in sidocode_list:

        storeList = getStores(sidocode)

        for store in storeList:
            outfile.write(u'스타벅스|')

            subname = store['s_name'].lstrip().rstrip()
            if not subname.endswith('점'): subname += '점'
            outfile.write(u'%s|' % subname.replace(' ', '/'))

            outfile.write(u'%s|' % store['tel'])
            outfile.write(u'%s|' % store['s_code'])

            store_addr = store['addr']
            store_addr = store_addr.replace('1층', ' 1층').replace('2층', ' 2층').replace('  ', ' ').lstrip().rstrip()
            outfile.write(u'%s|' % store_addr)

            outfile.write(u'%s|' % store['doro_address'])

            shop_feat = ''
            str_feat = store['theme_state']
            feat_list = str_feat.split('@')
            for i in range(len(feat_list)):
                feat_item = feat_list[i]
                if feat_item == None: continue
                elif feat_item == '': continue

                if feat_item == 'T03':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '스타벅스리저브'
                elif feat_item == 'T01':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '드라이브스루'
                elif feat_item == 'T12':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '커뮤니티스토어'
                elif feat_item == 'T06':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '프리미어푸드'
                elif feat_item == 'T09':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '주차'
                elif feat_item == 'T10':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '외화결제'
                elif feat_item == 'T04':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '에스프레소초이스'
                elif feat_item == 'T20':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '콜드브루커피'
                elif feat_item == 'T21':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '현금없는매장'
                elif feat_item == 'T22':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '나이트로콜드브루커피'
                elif feat_item == 'P10':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '공항내'
                elif feat_item == 'P50':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '해안가'
                elif feat_item == 'P20':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '대학가'
                elif feat_item == 'P60':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '터미널/기차역'
                elif feat_item == 'P70':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '병원'
                elif feat_item == 'P30':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '리조트'
                elif feat_item == 'P40':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '입점'
                elif feat_item == 'P80':
                    if shop_feat != '': shop_feat += ';'
                    shop_feat += '지하철인접'
                #else: shop_feat += feat_item   # 해석불가 feat는 표시하지 않음

            outfile.write(u'%s|' % shop_feat)
            outfile.write(u'%s|' % store['open_dt'])
            outfile.write(u'%s|' % store['lot'])
            outfile.write(u'%s\n' % store['lat'])

        delay_time = random.uniform(0.3, 1.1)
        time.sleep(delay_time)

    outfile.close()

def getStores(areaCode):

    url = 'http://www.istarbucks.co.kr'
    api = '/store/getStore.do'
    data = {
 #       "P10": 0,
 #       "P20": 0,
 #       "P30": 0,
 #       "P40": 0,
 #       "P50": 0,
 #       "P60": 0,
 #       "P70": 0,
 #       "P80": 0,
 #       "T01": 0,
 #       "T03": 0,
 #       "T04": 0,
 #       "T06": 0,
 #       "T09": 0,
 #       "T10": 0,
 #       "T12": 0,
 #       "T20": 0,
        "all_store": 0,
        "iend": "1000",
        "in_biz_cd": "",
        "in_biz_cds": 0,
        "in_distance": 0,
        "in_scodes": 0,
        "ins_lat": 37.56682,
        "ins_lng": 126.97865,
        "isError": True,
        "new_bool": 0,
        "p_gugun_cd": "",
        # "rndCod": "K0X18E62IP",
        "searchType": "C",
        "search_text": "",
        "set_date": "",
        "todayPop": 0
    }
    data['p_sido_cd'] = areaCode

    params = urllib.urlencode(data)
    print(params)   # for debugging

    try:
        result = urllib.urlopen(url + api, params)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)     # for debugging
    receivedData = json.loads(response)

    storeList = receivedData['list']
    return storeList


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
