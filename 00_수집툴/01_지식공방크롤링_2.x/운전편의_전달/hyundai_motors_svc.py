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

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('hyundai_motors_svc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|TYPE|NEWADDR|FEAT@@현대자동차서비스센터\n")

    outfile2 = codecs.open('hyundai_motors_svc_bluehands_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|ID|TELNUM|TYPE|NEWADDR|FEAT@@현대자동차서비스블루핸즈\n")


    page = 1
    while True:
        store_list = getStores(page)
        if store_list == None: break
        elif len(store_list) == 0: break

        for store in store_list:
            if store['type'].find('서비스센터') != -1:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s\n' % store['feat'])
            else:
                outfile2.write(u'%s|' % store['name'])
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['id'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['type'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s\n' % store['feat'])

        page += 1

        if page == 199:      # 2018년 6월 기준 139페이지까지 있음
            break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()

# v2.0 (2018/2)
def getStores(intPageNo):
    url = 'https://www.hyundai.com'
    api = '/wsvc/kr/front/biz/serviceNetwork.list.do'
    data = {
        'searchWord': '',
        'snGubunListSearch': '',
        'selectBoxCitySearch': '',
        'selectBoxTownShipSearch': '',
        'wkDtlSbc': '전체',
        'selectBoxCity': '',
    }
    data['pageNo'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, params, None)
        req = urllib2.Request(url + api, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    response_json = json.loads(response)  # json 포맷으로 결과값 반환
    entity_list = response_json['data']['result']

    store_list = []
    for i in range(len(entity_list)):

        store_info = {}

        store_info['type'] = entity_list[i]['apimCeqPlntNm'].lstrip().rstrip()
        strtemp = entity_list[i]['asnNm']

        store_info['name'] = store_info['type']
        store_info['subname'] = ''
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            strtemp = strtemp.replace('(합)', '').replace('(자)', '').replace('(주)', '').replace('㈜', '').replace('(유)', '').lstrip().rstrip()
            if strtemp.startswith('주)'): strtemp = strtemp[2:].lstrip()
            if strtemp.endswith('서비스센터'): pass
            elif strtemp.endswith('서비스') or strtemp.endswith('써비스') or strtemp.endswith('공업사'): pass
            elif strtemp.endswith('센타') or strtemp.endswith('센터') or strtemp.endswith('모터스'): pass
            elif not strtemp.endswith('점') and len(strtemp) <= 4: strtemp += '점'
            store_info['subname'] = strtemp.replace(' ', '/')

        # 이름 교정
        if store_info['type'] == '전문블루핸즈':
            store_info['name'] = '현대차블루핸즈'     # 공식 명칭 맞음?
        elif store_info['type'].endswith('서비스센터'):
            store_info['name'] = '현대자동차'
        elif store_info['type'] == '종합블루핸즈':
            store_info['name'] = '현대차블루핸즈'

        # 지점명 교정
        if store_info['subname'].startswith('현대자동차'):
            store_info['subname'] = store_info['subname'][5:].lstrip()
        elif store_info['subname'].endswith('현대자동차'):
            store_info['subname'] = store_info['subname'][:-5].rstrip()
        elif store_info['subname'].endswith('현대자동차점'):
            store_info['subname'] = store_info['subname'][:-6].rstrip()
        elif store_info['subname'].endswith('점현대자동차점') and len(store_info['subname']) >= 9:
            store_info['subname'] = store_info['subname'][:-6].rstrip()
        elif store_info['subname'].endswith('점현대자동차서비스') and len(store_info['subname']) >= 11:
            store_info['subname'] = store_info['subname'][:-8].rstrip()
        elif store_info['subname'].endswith('점현대자동차블루핸즈') and len(store_info['subname']) >= 11:
            store_info['subname'] = store_info['subname'][:-9].rstrip()
        elif store_info['subname'].endswith('점현대자동차서비스점') and len(store_info['subname']) >= 12:
            store_info['subname'] = store_info['subname'][:-9].rstrip()
        elif store_info['subname'].endswith('점현대자동차블루핸즈점') and len(store_info['subname']) >= 13:
            store_info['subname'] = store_info['subname'][:-10].rstrip()

        #if not store_info['subname'].endswith('점'):
        #    store_info['subname'] += '점'

        # 기타 정보 채워넣기
        store_info['id'] = entity_list[i]['asnCd']

        store_info['newaddr'] = entity_list[i]['pbzAdrSbc']
        store_info['pn'] = ''
        if entity_list[i].get('repnTn'):
            store_info['pn'] = entity_list[i]['repnTn'].lstrip().rstrip().replace(' ', '-')

        store_info['feat'] = ''
        if entity_list[i].get('wkDtlSbc'):
            store_info['feat'] = entity_list[i]['wkDtlSbc'].replace('/', ';')

        store_list += [store_info]

    return store_list

'''
# v1.0
def getStores(intPageNo):
    url = 'http://bluemembers.hyundai.com'
    api = '/oc/action.do'
    data = {
        'fw_serviceName': 'NetworkFacade.searchAsaList',
        'fw_appName': 'OC_HNET',
        'searchType': 'textBy',
        'searchTypeSub': '',
        'siDoCd': '',
        'siDoNm': '',
        'siGunGuCd': '',
        'siGunGuNm': '',
        'schText': '',
        'schTextType': '',
        'selectType': '',
        'pacScnCd': '',
        'mdlNm': '',
        'th1GYn': '',
        'th2GYn': '',
        'th3GYn': '',
        'th4GYn': ''
    }
    data['currPage'] = intPageNo

    params = urllib.urlencode(data)
    # print(params)

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
    #print(response)    # for debugging
    #response = unicode(response, 'euc-kr').encode('utf-8')     # 이렇게 호출하면 한글 깨짐
    response = unicode(response, 'euc-kr')                     # 제대로 동작함
    #print(response)    # for debugging
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="euc-kr"?> ' + response)

    tableSelector = '//table[@class="board-list map_bod"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody//tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = len(entityList) / 4
    for i in range(loop_count):
        storeInfo = {}

        infoList = entityList[i*4].xpath('.//td')       # 기본 정보 수록
        featList = entityList[i*4 + 3].xpath('.//td')   # 정비가능영역 정보 있음, 필요하면 나중에 추출할 것!!

        if(infoList == None): continue;     # for safety
        if (len(infoList) < 6): continue    # 6개 필드 있음

        strName = "";   strSubName="";      strFeature=""
        strNameInfo = "".join(infoList[0].itertext()).strip('\r\t\n').rstrip().lstrip()
        strNameInfo = strNameInfo.replace('\r', '').replace('\t', '').replace('\n', '')   # 앞의 strip('\r\t\n') 명령으로 잘 지워지지 않음 (이유 모름 ㅠㅠ)
        strNameInfo = strNameInfo.rstrip().lstrip()
        #print strNameInfo       # for debugging

        if strNameInfo.endswith('전문블루핸즈'):
            strName = '현대차블루핸즈'     # 공식 명칭 찾아서 바꿀것!!!
            strSubName = strNameInfo[:len(strNameInfo) - 6].rstrip()
            if strSubName.endswith('현대자동차'): strSubName = strSubName[:len(strSubName)-5].rstrip()
            strFeature = '전문블루핸즈'
        elif strNameInfo.endswith('직영서비스센터'):
            strName = '현대자동차'
            strSubName = strNameInfo[:len(strNameInfo) - 7].rstrip().replace(' ', '/')
            strFeature = '직영서비스센터'
        elif strNameInfo.endswith('종합블루핸즈'):
            strName = '현대차블루핸즈'
            strSubName = strNameInfo[:len(strNameInfo) - 6].rstrip().replace(' ', '/')
            strFeature = '종합블루핸즈'

        storeInfo['name'] = strName

        strSubName = strSubName.replace('(합)', '').replace('(자)', '').replace('(주)', '').replace('㈜', '').replace('(유)', '').lstrip().rstrip()
        if strSubName.startswith('주)'): strSubName = strSubName[2:].lstrip()
        strSubName = strSubName.replace(' ', '/')
        storeInfo['subname'] = strSubName

        storeInfo['feat'] = strFeature

        storeInfo['newaddr'] = infoList[1].text
        storeInfo['pn'] = infoList[2].text
        strtemp = infoList[3].text
        if strtemp != None:
            storeInfo['feat'] += ';'
            storeInfo['feat'] += strtemp

        storeList += [storeInfo]

    return storeList
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
