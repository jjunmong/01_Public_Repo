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
    '경기': '41',
}

sido_list = {
    '서울': '11',
    '광주': '29',
    '대구': '27',
    '대전': '30',
    '부산': '26',
    '울산': '31',
    '인천': '28',
    '경기': '41',
    '강원': '42',
    '경남': '48',
    '경북': '47',
    '전남': '46',
    '전북': '45',
    '충남': '44',
    '충북': '43',
    '제주': '50',
    '세종': '36'
}

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('kwangjubank_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|ID|TELNUM|TYPE|NEWADDR|XCOORD|YCOORD@@광주은행\n")


    for sido_name in sorted(sido_list):

        store_list = getStores(sido_list[sido_name])
        if store_list == None: continue

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['type'])
            outfile.write(u'%s|' % store['newaddr'] + ' ' + store['addr_details'])
            outfile.write(u'%s|' % store['xcoord'])
            outfile.write(u'%s\n' % store['ycoord'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


# v2.0 (2018/2)
def getStores(area_cd):
    url = 'https://www.kjbank.com'
    api = '/ib20/act/BHPBKIF010402A10?ib20_cur_mnu=BHPBKIF010402&ib20_cur_wgt=BHPBKIF010402V10'
    data = {
        # 'BOB_STCD_VAL': '0',
        #'INBN_MCP_CD': '11',
        'INBN_CCW_CD': '',
        # 'BOB_NM': '',
        'CHECK_TRAN_KEY': '20210127104048827',
        'action_type': 'act',
        'ib20_cur_mnu': 'BHPBKIF010402',
        'ib20_cur_wgt': 'BHPBKIF010402V10',
        'PROCS_DIV_S1': '1',
        #'INBN_BZOP_BRCD': '0210',
        # 'INBN_BZOP_BRCD': '',
        'b_page_id': '',
    }
    data['INBN_MCP_CD'] = area_cd
    params = urllib.urlencode(data)
    print(params)

    hdr = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': '__smVisitorID=jLjDZPJm46J; PCID=16117104363817047922514; RC_COLOR=24; RC_RESOLUTION=1920*1080; _ga=GA1.2.426286766.1611711337; _gid=GA1.2.564106193.1611711337; _gat_gtag_UA_162190149_1=1; iTracerAF=5e8583507adaf14a7974bbc7c04f609c5291be688f202868309d1ed838bb819fbe026f2ef4ff31ff484a37cd2435f13bce233d241c21652500582790969fee604f671e520ca22b7f9263f7783007d6f400d94f394ee485fc80fa233d3133241c216525110000T177417b7f6a; JSESSIONID=PBH82ehtBP1M1eityxWh2o38ot1wORWs8meVZK7wE0I4WygCRc5a!1356172045; IB20SESSID=BHP1201||PBH82ehtBP1M1eityxWh2o38ot1wORWs8meVZK7wE0I4WygCRc5a!1356172045!1611711352545',
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
    response = urllib.unquote(urllib.unquote(response))
    #print(response)
    data_list = json.loads(response)  # json 포맷으로 결과값 반환

    entity_list = data_list['_msg_']["_body_"]["LOOP"]

    store_list = []
    for i in range(len(entity_list)):
        shop_nm = entity_list[i]['BOB_NM']
        shop_id = entity_list[i]['INBN_BZOP_BRCD']

        suburls = 'https://www.kjbank.com/ib20/act/BHPBKIF010402A10?ib20_cur_mnu=BHPBKIF010402&ib20_cur_wgt=BHPBKIF010402V10'
        subdata = {
            'BOB_STCD_VAL': '0',
            #'INBN_MCP_CD': '11',
            'INBN_CCW_CD': '',
            'BOB_NM': '',
            'CHECK_TRAN_KEY': '20180208175604522',
            'action_type': 'act',
            'ib20_cur_mnu': 'BHPBKIF010402',
            'ib20_cur_wgt': 'BHPBKIF010402V10',
            'PROCS_DIV_S1': '2',
            #'INBN_BZOP_BRCD': '0210',
            'b_page_id': '',
        }
        subdata['INBN_MCP_CD'] = area_cd
        subdata['INBN_BZOP_BRCD'] = shop_id
        subparams = urllib.urlencode(subdata)
        print(subparams)

        try:
            # req = urllib2.Request(url + api, params, None)
            subreq = urllib2.Request(suburls, subparams, headers=hdr)
            subreq.get_method = lambda: 'POST'
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib2.urlopen(subreq)
        except:
            print('Error calling the subAPI');  continue

        subcode = subresult.getcode()
        if subcode != 200:
            print('HTTP request error (status %d)' % subcode);      continue

        subresponse = subresult.read()
        subresponse = urllib.unquote(urllib.unquote(subresponse))
        #print(subresponse)
        subdata_list = json.loads(subresponse)  # json 포맷으로 결과값 반환

        # 결과값 유효성 체크 (added on 2018/3)
        if not subdata_list.get('_msg_'): continue
        temp_list = subdata_list['_msg_']
        if not temp_list.get('_body_'): continue

        info_list = subdata_list['_msg_']["_body_"]

        store_info = {}
        store_info['name'] = '광주은행'

        store_info['subname'] = ''
        strtemp = info_list['BOB_NM']
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith('(출)'): strtemp = strtemp[:-3] + '출장소'
            elif strtemp.endswith('센터'): pass
            elif strtemp.endswith('영업부'): pass
            elif not strtemp.endswith('지점'): strtemp += '지점'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = shop_id

        store_info['newaddr'] = info_list['ADDR'].replace('+', ' ').lstrip().rstrip()
        store_info['pn'] = info_list['TLNO']
        store_info['addr_details'] = info_list['DTAD'].replace('+', ' ').lstrip().rstrip()
        store_info['type'] = info_list['BOB_STCD_VAL_NM']
        store_info['xcoord'] = info_list['INSL_BRN_LOTDE_VAL'].lstrip().rstrip()
        store_info['ycoord'] = info_list['INSL_BRN_LATDE_VAL'].lstrip().rstrip()

        store_list += [store_info]

    return store_list

'''
# v1.0
def getStores(intPageNo):
    url = 'http://www.kjbank.com'
    api = '/banking/homepage/kj_info/infor/bank08_01.jsp'
    data = {}
    params = urllib.urlencode(data)
    #print(params)

    hdr = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }

    try:
        #req = urllib2.Request(url + api, None, headers=hdr)
        req = urllib2.Request(url + api, None)
        req.get_method = lambda: 'GET'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #print(response)
    tree = html.fromstring(response)

    suburl_list = tree.xpath('//a[@target="branch"]/@href')

    store_list = []
    for i in range(len(suburl_list)):
        suburls = url + suburl_list[i]

        try:
            print(suburls)  # for debugging
            time.sleep(random.uniform(0.3, 0.9))
            subresult = urllib.urlopen(suburls)
        except:
            print('Error calling the subAPI');
            continue

        code = result.getcode()
        if code != 200:
            print('HTTP request error (status %d)' % code);
            continue

        subresponse = subresult.read()
        subresponse = unicode(subresponse, 'euc-kr')
        #print(subresponse)
        subtree = html.fromstring(subresponse)

        name_list = subtree.xpath('//div[@class="right"]//h4')
        info_list = subtree.xpath('//table[@class="tb_list"]//tr')
        if len(name_list) < 1 or len(info_list) < 2: continue  # 최소 필드 수 체크

        store_info = {}
        store_info['name'] = '광주은행'

        store_info['subname'] = ''
        strtemp = "".join(name_list[0].itertext())
        if strtemp != None:
            strtemp = strtemp.replace('\r', '').replace('\t', '').replace('\n', '').rstrip().lstrip()
            if strtemp.endswith('(출)'): strtemp = strtemp[:-3] + '출장소'
            store_info['subname'] = strtemp.replace(' ', '/')

        store_info['id'] = '';      store_info['newaddr'] = ''
        store_info['pn'] = '';      store_info['feat'] = ''
        for j in range(len(info_list)):
            tagvalue_list = info_list[j].xpath('.//td')
            if len(tagvalue_list) < 2: continue

            tag = "".join(tagvalue_list[0].itertext())
            value = "".join(tagvalue_list[1].itertext())
            if tag == None or value == None: continue

            tag = tag.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').lstrip().rstrip()
            value = value.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

            if tag == '주소': store_info['newaddr'] = value
            elif tag == '전화':
                if value.startswith('('): value = value[1:].lstrip()
                store_info['pn'] = value.replace(')', '-')
            elif tag == '지점번호': store_info['id'] = value
            elif tag == '365코너':
                if value == "있음":
                    store_info['feat'] = '365코너'

        store_list += [store_info]

    return store_list
'''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
