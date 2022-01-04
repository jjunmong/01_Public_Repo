# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: sheayun
'''

import sys
import time
import random
import codecs
import urllib
import urllib2
import json

sido_list2 = {      # 테스트용 시도 목록
    '서울': '11',     # 1
}

sido_list = {
    '서울': '11',     # 1
    '광주': '24',     # 2
    '대구': '23',
    '대전': '25',
    '부산': '21',
    '울산': '26',
    '인천': '22',
    '경기': '31',
    '강원': '32',     # 3
    '경남': '38',
    '경북': '37',
    '전남': '36',
    '전북': '35',
    '충남': '34',
    '충북': '33',
    '제주': '39',
    '세종': '41'
}
def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    #outfile_all = codecs.open('hira_test_utf8.txt', 'w', 'utf-8')
    outfile_all = codecs.open('hira_all_utf8.txt', 'w', 'utf-8')
    outfile_all.write("##NAME|ORGNAME|ETCNAME|TELNUM|NEWADDR|TYPE|FEAT|KEY@@HIRA\n")

    log_outfile = codecs.open('hira_log_utf8.txt', 'a', 'utf-8')

    for sido_name in sorted(sido_list):
        sido_code = sido_list[sido_name]

        gugun_namelist, gugun_codelist = get_gugun_namelist_codelist(sido_code)
        if gugun_namelist == None or gugun_codelist == None: continue

        #for idx in range(0, len(gugun_namelist)):
        for idx in range(len(gugun_namelist)):
            gugun_name = gugun_namelist[idx]
            gugun_code = gugun_codelist[idx]

            page = 1
            prev_key = ''
            retry_count = 0

            while True:
                #storeList = getStores(sido_name, sido_list[sido_name], gugun_name, gugun_code, '연세이비인후과의원', page)  # '예외처리용' 질의
                storeList = getStores(sido_name, sido_list[sido_name], gugun_name, gugun_code, '', page)
                if storeList == None:
                    retry_count += 1
                    if retry_count >= 3: break
                    else: continue
                elif len(storeList) == 0: break

                retry_count = 0
                curr_key = storeList[0]['yadmNm'] + '|' + storeList[0]['telNo'] + '|' + storeList[0]['addr']
                if prev_key == curr_key:
                    print('duplication : page = %d : %s' % (page, curr_key));       log_outfile.write('duplication : page = %d : %s\n' % (page, curr_key))
                    #page += 1;     continue

                prev_key = curr_key

                for store in storeList:
                    store_nm = '';  store_pn = '';  store_addr = '';    store_cd = '';  store_cdnm = '';    store_id = ''
                    if store.get('yadmNm'): store_nm = store['yadmNm']
                    if store.get('telNo'): store_pn = store['telNo']
                    if store.get('addr'): store_addr = store['addr']
                    if store.get('clCd'): store_cd = store['clCd']
                    if store.get('clCdNm'): store_cdnm = store['clCdNm']
                    if store.get('ykiho'): store_id = store['ykiho']
                    if store_cd == '': continue

                    store_orgname = store_nm

                    # myutil의 것 사용하도록 수정하거나, 수집시에는 호출하지 않도록 고칠 것!!
                    store_nm, store_etcname = pp_hira_name(store_nm)

                    # to do : myutil의 이름 후처리 함수들을 활용한 이름 후처리 한번 더 할까???
                    store_nm = store_nm.rstrip().lstrip().replace(' ', '/')

                    outfile = outfile_all

                    outfile.write(u'%s|' % store_nm)
                    outfile.write(u'%s|' % store_orgname)
                    outfile.write(u'%s|' % store_etcname)
                    outfile.write(u'%s|' % store_pn)
                    outfile.write(u'%s|' % store_addr)
                    outfile.write(u'%s|' % store_cd)
                    outfile.write(u'%s|' % store_cdnm)
                    outfile.write(u'%s\n' % store_id)

                page += 1
                if page == 10000:     # 2018년9월 기준 약 9293페이지까지 정보 있음
                    break

                time.sleep(random.uniform(0.1, 0.3))

            time.sleep(random.uniform(1, 2))

    outfile_all.close()
    log_outfile.close()


def getStores(sido_name, sido_code, gugun_name, gugun_code,  query_word, pageNo):
    url = 'https://www.hira.or.kr'
    api = '/rd/hosp/hospSrchListAjax.do'    # 병원리스트
    # api = '/rd/hosp/hospAjax.do'              # 병원상세정보

    data = {
        'pages': '',
        'sidoCdNm': '',
        'sgguCdNm': '',
        #'sortOrdr': '',
        'sortOrdr': 'nmAsc',
        'totalSrhYn': 'N',
        'sno': '',
        'clCd': '',
        'srchCd': '',
        'ykiho': '',
        'srchMode': 'general',
        'isProfessional': '',
        'isJongItem': '',
        'isPharmacyItem': '',
        'isPharmacy': 'N',
        'isHouseholdMedicine': 'N',
        'isPlcr': '',
        'mode': '',
        'xPosWGS84': '',
        'yPosWGS84': '',
        'isDgsMap': '',
        'isEmyMap': '',
        'isNightMap': '',
        'isRecuMap': '',
        'isPlcrMap': '',
        'sidoCd': '',
        'sgguCd': '',
        'emdongNm': '',
        'yadmNm': '',
        'greenYn': '',
        #'pageSize': '100',
        #'pageUnit': '100',
    }
    data['sgguCd'] = gugun_code
    data['sgguCdNm'] = gugun_name
    data['sidoCdNm'] = sido_name
    data['sidoCd'] = sido_code + '0000'
    data['yadmNm'] = query_word
    data['pageIndex'] = pageNo
    #data['pages'] = 9246
    #data['ykiho'] = "JDQ4MTg4MSM1MSMkMiMkNCMkMDAkNDgxMzUxIzUxIyQxIyQxIyQ5OSQ0NjE0ODEjNzEjJDEjJDgjJDgz"

    params = urllib.urlencode(data)
    #print(params)

    hdr = {
        #'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #'Content-Length': '30',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'WMONID=PqN8ejCF5HR; INTERSESSIONID=VJK2hHNitl7FCYI2Z1z0wwaUx3oTB9Eltq36M88ce_1cABtdv02d!153987708!-169574721',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        #result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params;
        print(urls)     # for debugging
        #result = urllib.urlopen(urls)

        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    try:
        response = result.read()
        #print(response)         # for debugging
        receivedData = json.loads(response)
        #print(receivedData)     # for debugging
    except:
        print('invalid return value');      return None

    storeList = []

    if receivedData.get('data'): dataList = receivedData['data']
    else: dataList = []

    if dataList.get('hospSrchList'): storeList = dataList['hospSrchList']
    else: storeList = []

    return storeList

def get_gugun_namelist_codelist(sido_code):
    url = 'https://www.hira.or.kr'
    api = '/rd/hosp/selectSgguListAjax.do'
    data = {}
    data['sidoCd'] = sido_code
    params = urllib.urlencode(data)
    #print(params)

    hdr = {
        #'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #'Content-Length': '30',
        #'Content-Type:': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'WMONID=PqN8ejCF5HR; INTERSESSIONID=VJK2hHNitl7FCYI2Z1z0wwaUx3oTB9Eltq36M88ce_1cABtdv02d!153987708!-169574721',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        #'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        #result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params;
        print(urls)     # for debugging
        #result = urllib.urlopen(urls)

        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(url+api, params)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)         # for debugging
    response_json = json.loads(response)
    entity_list = response_json['data']

    gugun_namelist = []
    gugun_codelist = []
    for i in range(len(entity_list)):
        gugun_namelist += [entity_list[i]['commCdNm']]
        gugun_codelist += [entity_list[i]['commCd']]

    return gugun_namelist, gugun_codelist

def pp_hira_name(store_nm):
    store_etcname = ''

    # 이름 전처리
    if store_nm.startswith('('):
        idx = store_nm.find(')')
        if idx != -1 and idx <= 5:
            store_nm = store_nm[idx + 1:].lstrip()
        else:
            store_nm = store_nm[1:idx] + ' ' + store_nm[idx + 1:]

    if store_nm.endswith(')'):
        idx = store_nm.rfind('(')
        store_etcname = store_nm[idx + 1:-1]
        store_nm = store_nm[:idx].rstrip()

    idx = store_nm.find(')')
    if idx != -1 and idx <= 1: store_nm = store_nm[idx + 1:]  # '사)', '재)'와 같은 것들 처리

    store_nm = store_nm.replace('사단법인', '').replace('의료재단법인', '').replace('재단법인', '').replace('의료법인', '').replace('사회복지법인', '')
    store_nm = store_nm.replace('비영리특수법인', '').replace('학교법인', '')
    store_nm = store_nm.replace('(사)', ' ').replace('(재)', ' ').replace('주식회사', '(주)').replace('㈜', '(주)').replace('(주)', ' ') \
        .replace('  ', ' ').replace('  ', ' ').lstrip().rstrip()

    if store_nm.startswith(')'): store_nm = store_nm[1:].lstrip()

    if store_nm.find('학원부설') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('학원부설')
        if idx + 8 <= len(store_nm):  # '학원부설' 뒤의 이름이 최소 4자
            strtail = store_nm[idx + 4:].lstrip()
            if not strtail.startswith('치과') and not strtail.startswith('요양'):
                if store_etcname != '': store_etcname += ';'
                store_etcname += store_nm[:idx + 4]
                store_nm = strtail
    elif store_nm.find('부설') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('부설')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            strtail = store_nm[idx+2:].lstrip()
            if not strtail.startswith('치과') and not strtail.startswith('요양'):
                if store_etcname != '': store_etcname += ';'
                store_etcname += store_nm[:idx + 2]
                store_nm = strtail
    elif store_nm.find('부속') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('부속')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            strtail = store_nm[idx+2:].lstrip()
            if not strtail.startswith('치과') and not strtail.startswith('요양'):
                if store_etcname != '': store_etcname += ';'
                store_etcname += store_nm[:idx + 2]
                store_nm = strtail
    elif store_nm.find('학원') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('학원')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('재단') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('재단')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('지회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('지회')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('지부') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('지부')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('협회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('협회')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('원불교') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('원불교')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('관음종') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('관음종')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('수녀회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('수녀회')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('수도회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('수도회')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('선교회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('선교회')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('연합회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('연합회')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('의료공단') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('의료공단')
        if idx + 8 <= len(store_nm):  # '의료공단' 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 4]
            store_nm = store_nm[idx + 4:].lstrip()
    elif store_nm.find('협동조합') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('협동조합')
        if idx + 8 <= len(store_nm):  # '협동조합' 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 4]
            store_nm = store_nm[idx + 4:].lstrip()

    return store_nm, store_etcname


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
