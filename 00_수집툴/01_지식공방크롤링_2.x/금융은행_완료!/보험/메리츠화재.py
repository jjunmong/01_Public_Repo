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

sido_list2 = {      # 테스트용 시도 목록
    '대전': '042'
}

sido_list = {
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

    outfile = codecs.open('insurance_meritzfire_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|ADDR|NEWADDR@@메리츠화재\n")

    for sido_name in sorted(sido_list):
        store_list = getStores(sido_name)
        if store_list != None:
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['subname'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['pn'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['newaddr'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStores(sido_name):
    urls = 'https://www.meritzfire.com/json.smart'
    data = {"header":{"encryDivCd":"0","globId":"","rcvmsgSrvId":"f.cg.he.cm.ft.o.bc.SvcNtkBc.retrieveCenterBranchList","resultRcvmsgSrvId":"","esbIntfId":"","exsIntfId":"","ipv6Addr1":"","ipv6Addr2":"","teleMsgMacAdr":"","envirInfoDivCd":"","firstTranssLcatgBizafairCd":"","transsLcatgBizafairCd":"","reqRespnsDivCd":"Q","syncDivCd":"S","teleMsgReqDttm":"","prcesResultDivCd":"","teleMsgRespnsDttm":"","clienTrespnsDttm":"","handcapLcatgBizafairCd":"","teleMsgVerDivCd":"","langDivCd":"KR","belongGrpCd":"","empNo":"","empId":"","dptCd":"","hgrkDptCd":"","nxupDptCd":"","transGrpCd":"F","screenId":"/footer/service-network.do","lowrnkScreenId":"/","resveLet":""},"body":{"inqSidoNm":"경기","inqSgkNm":""}}
    data['body']['inqSidoNm'] = sido_name
    params = json.dumps(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        #'Cookie': 'WMONID=jlhhbtA-SbY; PCID=14938233263036540236156; hpssessionid=1hjHO9794Q2PiiYJEHzNtiTWot5s6vrwRzshyfU5Noos1kAR9gJJqdotZK6P1h6m.cswas1p_servlet_hps2; _ga=GA1.2.1384152388.1493823326; _gid=GA1.2.529967309.1493910535',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url+api, params, headers=hdr)
        req = urllib2.Request(urls, params, headers=hdr)
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)

    response_json = json.loads(response)
    entity_list = response_json['body']['resList']

    store_list = []
    for i in range(len(entity_list)):
        store_info = {}

        store_info['name'] = '메리츠화재'
        strtemp = entity_list[i]['brchOrgNm'].lstrip().rstrip()
        store_info['orgname'] = strtemp
        store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = entity_list[i]['adrMap']['DEPT_CD']

        store_info['addr'] = entity_list[i]['adrMap']['addr']
        store_info['newaddr'] = entity_list[i]['adrMap']['raddr']
        store_info['pn'] = entity_list[i]['adrMap']['tel'].replace(' ', '').replace(')', '-').replace('.', '-')
        idx = store_info['pn'].find(',')
        if idx > 0:
            store_info['pn'] = store_info['pn'][:idx].rstrip()

        store_list += [store_info]

    return store_list


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
