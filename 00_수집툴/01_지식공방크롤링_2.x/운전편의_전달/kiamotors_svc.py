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

    outfile = codecs.open('kiamotors_svc_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ID|NEWADDR|FEAT|COMMENTS|XCOORD|YCOORD@@기아자동차서비스센터\n")

    outfile2 = codecs.open('kiamotors_svc_autoq_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|ID|NEWADDR|TYPE|COMMENTS|XCOORD|YCOORD@@기아자동차오토큐\n")

    page = 1
    while True:
        storeList = getStores(page)
        if len(storeList) == 0:
            break

        for store in storeList:
            if store['type'].find('직영서비스센터') != -1:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['type'])
                outfile.write(u'%s|' % store['comments'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])
            else:
                outfile2.write(u'%s|' % store['name'])
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['id'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s|' % store['type'])
                outfile2.write(u'%s|' % store['comments'])
                outfile2.write(u'%s|' % store['xcoord'])
                outfile2.write(u'%s\n' % store['ycoord'])

        page += 1
        if page == 149: break       # 2018년 6월 기준 83페이지까지 있음
        elif len(storeList) < 10: break

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    outfile2.close()

def getStores(intPageNo):
    # v2.0 (2017/10)
    url = 'http://red.kia.com'
    api = '/kr/knet/searchAsaList.do'
    data = {
        'funcobj': 'goPage_comm',
        'searchType': '',
        'searchTypeSub': '',
        'siDoCd': '',
        'siDoNm': '',
        'siGunGuCd': '',
        'siGunGuNm': '',
        'schText': '',
        'schTextType': '',
        'selectType': '',
        'asnCd': '',
        'schTextTemp': '',
        'selectTypeTemp': 'all',
        'siDoCdTemp': '',
        'siGunGuCdTemp': '',
        'pagesize': 10,
        'from_qnet': 'qnet_asn_prct_index_btnSelect'
    }
    data['currpage'] = intPageNo
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }

    try:
        urls = url + api
        #req = urllib2.Request(urls, params)
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        errExit('Error calling the API')

    code = result.getcode()
    if code != 200:
        errExit('HTTP request error (status %d)' % code)

    response = result.read()
    #print(response)
    response_json = json.loads(response)
    entity_list = response_json['searchAsaList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        strNameInfo = entity_list[i]['poiName']
        if strNameInfo != None:
            strNameInfo = strNameInfo.replace('\r', '').replace('\t', '').replace('\n', '').replace('기아 오토큐', '기아오토큐').rstrip().lstrip()

        strType = entity_list[i]['poiClassName']
        if strType != None:
            strType = strType.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()

        if strType == '직영서비스센터':
            strName = '기아자동차서비스'
            strSubName = strNameInfo.replace(' ', '/')
        elif strType == '전문서비스' or strType == '종합서비스':
            strName = '기아오토큐'
            strSubName = strNameInfo
            if strSubName.startswith('주)'): strSubName = strSubName[2:].lstrip()
            strSubName = strSubName.replace('주식회사', '').replace('(주)', '').replace('㈜', '').replace('(합)', '').replace('(자)', '').replace('(유)', '').lstrip().rstrip()
            strSubName = strSubName.replace('기아오토큐', '').replace('기아오토 큐', '').lstrip().rstrip().replace(' ', '/')
        else:   # type 정보 없는 경우에 대비해서...
            strName = '기아오토큐'
            strSubName = strNameInfo.lstrip().rstrip().replace(' ', '/')

        store_info['name'] = strName
        store_info['subname'] = strSubName
        store_info['type'] = strType

        store_info['newaddr'] = entity_list[i]['addr'].rstrip().lstrip()

        store_info['pn'] = ''
        strtemp = entity_list[i]['telNo']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            store_info['pn'] = strtemp.replace(' ', '').replace(')', '').replace('.', '')

        store_info['xcoord'] = entity_list[i]['displayX']
        store_info['ycoord'] = entity_list[i]['displayY']

        store_info['id'] = entity_list[i]['poiId']
        store_info['comments'] = ''
        strtemp = entity_list[i]['rprTypeNm']
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
            store_info['comments'] = strtemp

        store_list += [store_info]

    return store_list

"""
    # v1.0
    url = 'http://red.kia.com'
    api = '/kr/action.do'
    data = {
        'fw_serviceName': 'NetworkFacade.searchAsaList',
        'fw_appName': 'OC_KNET',
        'searchType': '',
        'searchTypeSub': '',
        'siDoCd': '',
        'siDoNm': '',
        'siGunGuCd': '',
        'siGunGuNm': '',
        'schText': '',
        'schTextType': '',
        'selectType': '',
        'listCnt': 10,
        'from_qnet': 'qnet_asn_prct_index_btnSelect'
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
    #print(response)
    #response = unicode(response, 'euc-kr').encode('utf-8')     # 이렇게 호출하면 한글 깨짐
    response = unicode(response, 'euc-kr')                     # 제대로 동작함
    #print(response)
    tree = html.fromstring(response)
    #tree = html.fromstring('<?xml version="1.0" encoding="euc-kr"?> ' + response)

    tableSelector = '//div[@class="tableSt04"]'
    dataTable = tree.xpath(tableSelector)[0]

    entitySelector = './/tbody//tr'
    entityList = dataTable.xpath(entitySelector)

    storeList = []

    loop_count = 0      # for debugging
    for i in range(len(entityList)):
        storeInfo = {}

        infoList = entityList[i].xpath('.//td')

        if(infoList == None): continue;     # for safety
        if (len(infoList) < 5): continue    # 5개 필드 있음

        strName = "";   strSubName="";      strFeature=""
        strNameInfo = "".join(infoList[0].itertext())
        strNameInfo = strNameInfo.replace('\r', '').replace('\t', '').replace('\n', '').replace('기아 오토큐', '기아오토큐').rstrip().lstrip()   # 앞의 strip('\r\t\n') 명령으로 잘 지워지지 않음 (이유 모름 ㅠㅠ)
        #print strNameInfo       # for debugging
        idx = strNameInfo.find("(종합서비스)")
        if idx >= 4:    # 이름은 최소 4글자는 된다고 가정
            strName = strNameInfo[0:idx].lstrip().rstrip()
            strFeature = '기아자동차서비스;종합서비스'
        idx = strNameInfo.find("(직영서비스센터)")
        if idx >= 4:    # 이름은 최소 4글자는 된다고 가정
            strName = '기아자동차서비스'
            strSubName = strNameInfo[0:idx].lstrip().rstrip()
            strFeature = '기아자동차서비스;직영서비스센터'
        idx = strNameInfo.find("(전문서비스)")
        if idx >= 4:    # 이름은 최소 4글자는 된다고 가정
            strName = '기아오토큐'
            strSubName = strNameInfo[0:idx].lstrip().rstrip()
            if strSubName.endswith('기아오토큐'): strSubName = strSubName[:len(strSubName)-5].lstrip().rstrip()
            strFeature = '기아자동차서비스;전문서비스'
        if strNameInfo.endswith('기아오토큐'):
            strName = '기아오토큐'
            strSubName = strNameInfo[:-5].rstrip()

        strName = strName.replace('주식회사', '').replace('(주)', '').replace('㈜', '').replace('(합)', '').replace('(자)', '').replace('(유)', '').lstrip().rstrip()
        if strName.find('버스전담') != -1:
            strName = strName.replace('(버스전담)', '').lstrip().rstrip()
            if strFeature != '': strFeature += ';'
            strFeature +=  '버스전담'

        if strName == '': strName = '기아오토큐'     # 맞음?

        storeInfo['name'] = strName

        strSubName = strSubName.replace('주식회사', '').replace('(주)', '').replace('㈜', '').replace('(합)', '').replace('(자)', '').replace('(유)', '').lstrip().rstrip()
        if strSubName.startswith('주)'): strSubName = strSubName[2:].lstrip()

        storeInfo['subname'] = strSubName
        storeInfo['feat'] = strFeature

        altInfo = infoList[0].xpath('.//img/@alt')
        if len(altInfo) > 0:
            if altInfo[0] == 'K9':
                storeInfo['feat'] += ';'
                storeInfo['feat'] += '마스터오토큐'

        storeInfo['newaddr'] = "".join(infoList[1].itertext()).strip('\r\t\n').rstrip().lstrip()
        storeInfo['pn'] = "".join(infoList[2].itertext()).strip('\r\t\n').rstrip().lstrip()
        strtemp = "".join(infoList[3].itertext()).strip('\r\t\n')
        if strtemp != None: strtemp.rstrip().lstrip()
        storeInfo['comments'] = strtemp.replace('\r', '').replace('\t', '').replace('\n', '')   # 앞의 strip('\r\t\n') 명령으로 잘 지워지지 않음 (이유 모름 ㅠㅠ)
        store_id = infoList[4].xpath('.//a/@href')[0]    # 상세정보 페이지에서의 정보 추출은 나중에...

        storeList += [storeInfo]

    return storeList
"""

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
