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

    outfile = codecs.open('crematory_ehaneul_all_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|NEWADDR|TYPE|ETC|FEAT|XCOORD|YCOORD|SOURCE2@@화장시설\n")

    # 화장시설 (60곳)
    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['etcinfo'])
            outfile.write(u'%s|' % store['feat'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s|' % store['ycoord'])
            outfile.write(u'%s\n' % u'보건복지부장사정보시스템')

        page += 1

        if page == 199: break
        elif len(store_list) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

# 화장시설
def getStores(intPageNo):
    # 'http://www.ehaneul.go.kr/portal/fnlFac/fnlFacList.do'
    url = 'http://m.ehaneul.go.kr'
    api = '/fnl/fnlFacList.ajax'
    data = {
        'facilityDivCd': '4',   # 1=장례식장, 2=공원묘원, 4=화장시설
        'pageInqCnt': '',
        'sidoCd': '',
        'gunguCd': '',
        'publicCode': '',
        'companyName': '',
        'latitude': '37.5723772025',
        'longitude': '127.0142857103',
    }
    data['curPageNo'] = intPageNo
    params = urllib.urlencode(data)
    params = 'facilityDivCd=4&curPageNo=' + str(intPageNo) + '&sidoCd=&gunguCd=&publicCode=&companyName=&latitude=37.5723772025&longitude=127.0142857103'
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,fr;q=0.5,it;q=0.4,zh-CN;q=0.3,zh;q=0.2',
        'Connection': 'keep-alive',
        #'Content-Length': '30',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'noPop=1; JSESSIONID=0000rp4VFjYRAGRVyChlEOfopKm:-1',
        #'Cookie': 'JSESSIONID=0000rp4VFjYRAGRVyChlEOfopKm:-1',
        #'Host': 'm.ehaneul.go.kr',
        #'Origin': 'http://m.ehaneul.go.kr',
        #'Referer': 'http://m.ehaneul.go.kr/fnl/fnlFacList.do?type=22',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    cookies = {'JSESSIONID': '0000rp4VFjYRAGRVyChlEOfopKm:-1', 'noPop': '1'}

    try:
        #res = requests.post(url+api, data=params, headers=hdr, cookies=cookies)

        req = urllib2.Request(url+api, params, headers=hdr)
        #req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    #code = res.status_code
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    response_json = json.loads(response)  # json 포맷으로 결과값 반환
    #response_json = res.json()
    entity_list = response_json['result']['facList']

    store_list = []
    for i in range(len(entity_list)):

        store_info = {}
        store_info['name'] = ''
        store_info['type'] = '화장시설'
        store_info['subname'] = ''
        store_info['etcinfo'] = ''
        strtemp = entity_list[i]['companyname']
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            strtemp = strtemp.replace('(주)', '').replace('(유)', '').replace('(재)', '').replace('(학)', '').replace('(복)', '').rstrip().lstrip()
            strtemp = strtemp.replace('재단법인', '').replace('(묘지)', ' 묘지').rstrip().lstrip()

            if strtemp.endswith(')'):
                idx = strtemp.rfind('(')
                if idx > 0:
                    store_info['etcinfo'] = strtemp[idx+1:-1].lstrip().rstrip()
                    strtemp = strtemp[:idx].rstrip()

            store_info['name'] = strtemp.replace(' ', '/')


        store_info['feat'] = entity_list[i]['manageclassdiv']
        store_info['newaddr'] = entity_list[i]['fulladdress']

        store_info['pn'] = ''
        strtemp = entity_list[i]['telephone']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            store_info['pn'] = strtemp.replace('.', '-').replace(')', '-').replace(' ', '-')


        store_info['id'] = entity_list[i]['facilitycd']
        store_info['xcoord'] = entity_list[i]['longitude']
        store_info['ycoord'] = entity_list[i]['latitude']

        # 다른 정보도 많이 있음 (필요할 때 추출할 것)

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
