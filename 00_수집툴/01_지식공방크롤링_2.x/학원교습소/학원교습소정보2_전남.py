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
import requests
import random
import json
from lxml import html
import xml.etree.ElementTree as ElementTree
from selenium import webdriver
from seleniumrequests import PhantomJS
from seleniumrequests import Chrome
from seleniumrequests import Firefox
import BeautifulSoup

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

api_dict2 = {
    #'https://hakwon.sen.go.kr/scs_ica_cr91_005.ws': '1168',  # 서울
    #'https://hakwon.goe.go.kr/scs_ica_cr91_005.ws': '4182',  # 경기
    #'https://hakwon.pen.go.kr/scs_ica_cr91_005.ws': '2144',  # 부산
    #'https://hakwon.dge.go.kr/scs_ica_cr91_005.ws': '2220',  # 대구
    #'https://hakwon.ice.go.kr/scs_ica_cr91_005.ws': '2871',  # 인천
    'https://hakwon.gen.go.kr/scs_ica_cr91_005.ws': '2420',  # 광주 (API 호출 오류 발생 ㅠㅠ)
    #'https://hakwon.dje.go.kr/scs_ica_cr91_005.ws': '1168',  # 대전
    #'https://hakwon.use.go.kr/scs_ica_cr91_005.ws': '1168',  # 울산
    #'https://hakwon.sje.go.kr/scs_ica_cr91_005.ws': '1168',  # 세종
    #'https://hakwon.kwe.go.kr/scs_ica_cr91_005.ws': '1168',  # 강원
    #'https://hakwon.cbe.go.kr/scs_ica_cr91_005.ws': '1168',  # 충북
    #'https://hakwon.cne.go.kr/scs_ica_cr91_005.ws': '1168',  # 충남
    'https://hakwon.jbe.go.kr/scs_ica_cr91_005.ws': '1168',  # 전북 (API 호출 오류 발생 ㅠㅠ)
    'https://hakwon.jne.go.kr/scs_ica_cr91_005.ws': '1168',  # 전남 (API 호출 오류 발생 ㅠㅠ)
    #'https://hakwon.gbe.kr/scs_ica_cr91_005.ws': '1168',  # 경북
    #'https://hakwon.gne.go.kr/scs_ica_cr91_005.ws': '1168',  # 경남
    #'https://hakwon.jje.go.kr/scs_ica_cr91_005.ws': '1168',  # 제주
}

api_dict = {
    #'https://hakwon.gen.go.kr/scs_ica_cr91_005.ws': '2420',  # 광주 (API 호출 오류 발생 ㅠㅠ)
    #'https://hakwon.jbe.go.kr/scs_ica_cr91_005.ws': '1168',  # 전북 (API 호출 오류 발생 ㅠㅠ)
    'https://hakwon.jne.go.kr/scs_ica_cr91_005.ws': '1168',  # 전남 (API 호출 오류 발생 ㅠㅠ)
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    #outfile = codecs.open('private_academy_gj_utf8.txt', 'w', 'utf-8')
    #outfile = codecs.open('private_academy_jb_utf8.txt', 'w', 'utf-8')
    outfile = codecs.open('private_academy_jn_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|TELNUM|NEWADDR|ID|ID2|TYPE|SIZE|SUBJ1|SUBJ2|SUBJ3|SUBJ4@@PACADEMY\n")

    for api_item in sorted(api_dict):

        # get cookie info
        cookie = ''
        #cookie = 'WMONID=VnlQEa6UtHU; JSESSIONID=ateQFBy1x3laN49k7z9DAks5HGHc55HcewGQMcUmyRcFfMq70rwJkLMEbd3ytK8l.gen-pacwas1_servlet_hkwwas'
        #cookie = 'WMONID=VnlQEa6UtHU; JSESSIONID=uIqIw1Enw8DogDpS7rS7R7QfLqjvWiw9TOQkNnmyDof44YNJ0XkdW4kixaHThJ31.gen-pacwas2_servlet_hkwwas'
        idx = api_item.rfind('/')
        url = api_item[:idx]
        if cookie == '':
            try:
                urls = url + '/edusys.jsp?page=scs_m80000'
                print(urls)  # for debugging
                #result = urllib.urlopen(urls)
                result = requests.get(urls, verify=False)
            except:
                print(urls + ' Error calling the API');     continue

            #code = result.getcode()
            code = result.status_code
            if code != 200:
                print(urls + ' HTTP request error (status %d)' % code);     continue

            strtemp = result.headers.get('Set-Cookie')
            temp_list = strtemp.split(';')
            for idx in range(len(temp_list)):
                strtemp = temp_list[idx].replace('\'', '').lstrip().rstrip()
                if strtemp.startswith('Path=/'): strtemp = strtemp[6:].lstrip()
                if strtemp.startswith(','): strtemp = strtemp[1:].lstrip()

                if strtemp.startswith('WMONID'):
                    if cookie != '': cookie += '; '
                    cookie += strtemp
                elif strtemp.startswith('JSESSIONID'):
                    if cookie != '': cookie += '; '
                    cookie += strtemp

            print('cookie = ' + cookie)

        # get sub district code info
        sub_district_list = getSubDistrictInfo(url + '/scs_ica_cr91_001.ws', cookie)
        #sub_district_list = [2420, 2415, 2411, 2417, 2414] # 광주는 API 호출 오류???
        print('sub district info collected!')

        # 학원, 교습소 정보 수집
        for idx in range(len(sub_district_list)):

            if sub_district_list[idx] == '1168': continue  # 임시 예외처리를 위한 코드...

            # 학원 정보 수집
            page = 1
            retry_count = 0
            while True:
                storeList = getStores(api_item, sub_district_list[idx], cookie, 1, page)
                if storeList == None:
                    retry_count += 1
                    if retry_count >= 2: break
                    else: continue
                elif len(storeList) == 0: break

                retry_count = 0

                for store in storeList:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['pn'])
                    outfile.write(u'%s|' % store['newaddr'])
                    outfile.write(u'%s|' % store['id'])
                    outfile.write(u'%s|' % store['id2'])
                    outfile.write(u'%s|' % store['type1'])
                    outfile.write(u'%s|' % store['count1'])     # 선생님수
                    outfile.write(u'%s|' % store['type2'])      # 아래 항목들은 교과목 관련 정보
                    outfile.write(u'%s|' % store['type3'])
                    outfile.write(u'%s|' % store['type4'])
                    outfile.write(u'%s\n' % store['type5'])

                page += 1

                if page == 3999: break
                elif len(storeList) < 10: break

                time.sleep(random.uniform(0.3, 0.9))

            # 교습소 정보 수집
            page = 1
            retry_count = 0
            while True:
                storeList = getStores(api_item, sub_district_list[idx], cookie, 2, page)
                if storeList == None:
                    retry_count += 1
                    if retry_count >= 2: break
                    else: continue
                elif len(storeList) == 0:
                    break

                retry_count = 0

                for store in storeList:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['pn'])
                    outfile.write(u'%s|' % store['newaddr'])
                    outfile.write(u'%s|' % store['id'])
                    outfile.write(u'%s|' % store['id2'])
                    outfile.write(u'%s|' % store['type1'])
                    outfile.write(u'%s|' % store['count1'])  # 선생님수
                    outfile.write(u'%s|' % store['type2'])  # 아래 항목들은 교과목 관련 정보
                    outfile.write(u'%s|' % store['type3'])
                    outfile.write(u'%s|' % store['type4'])
                    outfile.write(u'%s\n' % store['type5'])

                page += 1

                if page == 3999:
                    break
                elif len(storeList) < 10:
                    break

                time.sleep(random.uniform(0.1, 0.3))

            time.sleep(random.uniform(1, 2))

        time.sleep(random.uniform(2, 4))

    outfile.close()


def getStores(url, area_code, cookie, academy_type, intPageNo):
    #data = {"pageIndex":"1","pageSize":10,"checkDomainCode":"","juOfcdcCode":"","acaAsnum":"","gubunCode":"","searchYn":"1","searchGubunCode":"1","searchName":"","searchZoneCode":"1168","searchKindCode":"","searchTypeCode":"","searchCrseCode":"","searchCourseCode":"","searchClassName":""}
    data = {"pageIndex":"2","pageSize":10,"checkDomainCode":"","juOfcdcCode":"","acaAsnum":"","gubunCode":"","searchYn":"1","searchGubunCode":"1","searchName":"","searchZoneCode":"2420","searchKindCode":"","searchTypeCode":"","searchCrseCode":"","searchCourseCode":"","searchClassName":""}
    data['pageIndex'] = intPageNo
    data['searchZoneCode'] = area_code
    data['searchGubunCode'] = academy_type     # 1 (학원), 2 (교습소)
    params = json.dumps(data)
    print(params)  # for debugging

    # Cookie값 없으면 호출 실패
    hdr = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,fr;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        #'Cache-Control': 'max-age=0',
        #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #'Cookie': 'WMONID=My5Yu9p9Itm; JSESSIONID=k9vzvGGghu9Y21BHIsEgGBH16CU9AMjLRDazw225QQVx32Dz0D4lNO1NekG8sOIA.sen-pacwas2_servlet_hkwwas',
        #'Host': 'hakwon.gen.go.kr',
        #'Origin': 'https://hakwon.gen.go.kr',
        #'Referer': 'https://hakwon.gen.go.kr/edusys.jsp?page=scs_m83000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    hdr['Cookie'] = cookie

    try:
        #req = urllib2.Request(url, params)
        #req = urllib2.Request(url, params, headers=hdr)
        #req.get_method = lambda: 'POST'
        #result = urllib2.urlopen(req)

        result = requests.post(url,data=params, headers=hdr, verify=False)
    except:
        print('Error calling the API');     return None

    #code = result.getcode()
    code = result.status_code
    if code != 200:
        print('HTTP request error (status %d)' % code);
        return None

    try:
        # response = result.read()
        # response_json = json.loads(response)
        response_json = result.json()
        entity_list = response_json['resultSVO']['hesIcaCr91M00DVO']
    except:
        print('invalid return value');      return None

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = entity_list[i]['acaNm']
        store_info['subname'] = ''
        store_info['id'] = entity_list[i]['acaAsnum']

        store_info['newaddr'] = entity_list[i]['totalJuso']
        store_info['id2'] = entity_list[i]['regAsnum']
        store_info['count1'] = entity_list[i]['teacherCnt']
        store_info['type1'] = entity_list[i]['kindNm']
        store_info['type2'] = entity_list[i]['fieldNm']
        store_info['type3'] = entity_list[i]['gmNm']
        store_info['type4'] = entity_list[i]['leSbjtNm']
        store_info['type5'] = entity_list[i]['orderNm']
        store_info['pn'] = entity_list[i]['faTelno']

        store_list += [store_info]

    return store_list

def getSubDistrictInfo(url, cookie):
    #driver = webdriver.Chrome('C:\Python27\chromedriver.exe')
    #driver.get('https://hakwon.sen.go.kr/scs_ica_cr91_001.ws')
    #driver.get('https://hakwon.sen.go.kr/edusys.jsp?page=scs_m83000')
    #delay = 3
    #driver.implicitly_wait(delay)
    #response = driver.page_source
    #print(response)

    # Cookie값 없으면 호출 실패
    hdr = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,fr;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        #'Cache-Control': 'max-age=0',
        #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #'Cookie': 'WMONID=My5Yu9p9Itm; JSESSIONID=k9vzvGGghu9Y21BHIsEgGBH16CU9AMjLRDazw225QQVx32Dz0D4lNO1NekG8sOIA.sen-pacwas2_servlet_hkwwas',
        #'Host': 'hakwon.gen.go.kr',
        #'Origin': 'https://hakwon.gen.go.kr',
        #'Referer': 'https://hakwon.gen.go.kr/edusys.jsp?page=scs_m83000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    hdr['Cookie'] = cookie

    #browser = Chrome()
    #resp = browser.request('POST', url, data=None, headers=hdr)
    #resp = browser.request('POST', url, data=None, headers=hdr, verify=False)

    try:
        #req = urllib2.Request(url, params)
        #req = urllib2.Request(url, None, headers=hdr)
        #req.get_method = lambda: 'POST'
        #result = urllib2.urlopen(req)

        result = requests.post(url, headers=hdr, verify=False)
    except:
        print('Error calling the API');     return None

    #code = result.getcode()
    code = result.status_code
    if code != 200:
        print('HTTP request error (status %d)' % code);
        return None

    #response = result.read()
    #response_json = json.loads(response)
    response_json = result.json()
    entity_list = response_json['resultSVO']['searchZoneCodeList']

    district_list = []
    for i in range(len(entity_list)):
        district_list.append(entity_list[i]['zoneCode'])

    return district_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
