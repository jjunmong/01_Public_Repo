# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import time
import codecs
import urllib
import random
#import json
from lxml import html
import xml.etree.ElementTree as ElementTree

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    outfile = codecs.open('nolboo_all_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|FEAT@@놀부보쌈\n")

    outfile2 = codecs.open('nolboo_bossam_utf8.txt', 'w', 'utf-8')
    outfile2.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|FEAT@@놀부보쌈\n")

    outfile3 = codecs.open('nolboo_budae_utf8.txt', 'w', 'utf-8')
    outfile3.write("##NAME|SUBNAME|TELNUM|ADDR|NEWADDR|OT|FEAT@@놀부부대찌개\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: break
        elif len(storeList) == 0:
            break

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['ot'])
            outfile.write(u'%s\n' % store['feat'])

            if store['name'].find('보쌈') != -1 or store['name'].find('EX') != -1:
                outfile2.write(u'%s|' % store['name'])
                outfile2.write(u'%s|' % store['subname'])
                outfile2.write(u'%s|' % store['pn'])
                outfile2.write(u'%s|' % store['addr'])
                outfile2.write(u'%s|' % store['newaddr'])
                outfile2.write(u'%s|' % store['ot'])
                outfile2.write(u'%s\n' % store['feat'])

            if store['name'].find('부대') != -1:
                outfile3.write(u'%s|' % store['name'])
                outfile3.write(u'%s|' % store['subname'])
                outfile3.write(u'%s|' % store['pn'])
                outfile3.write(u'%s|' % store['addr'])
                outfile3.write(u'%s|' % store['newaddr'])
                outfile3.write(u'%s|' % store['ot'])
                outfile3.write(u'%s\n' % store['feat'])

        page += 1

        if page == 299:     # 2018년6월 기준 144페이지까지 있음
            break
        elif len(storeList) < 5: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()
    outfile2.close()
    outfile3.close()

def getStores(intPageNo):
    url = 'http://www.nolboo.co.kr'
    api = '/pages/store/getStoreList.asp'
    data = {
        'menu_id': '',
        's_area': '',
        's_d_area': '',
        's_name': '',
        'brand': '',
        'map_s_area': ''
    }
    data['page'] = intPageNo
    params = urllib.urlencode(data)
    # print(params)

    try:
        # result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return None

    response = result.read()
    #response = '<?xml version="1.0" encoding="utf-8"?><lists><total><page>185</page></total><item>	<s_num><![CDATA[1721]]></s_num>	<menu_id><![CDATA[2]]></menu_id>	<s_name><![CDATA[가락부대점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 송파구 가락동 79-3 대동빌딩1층]]></s_address2>	<s_address3><![CDATA[서울 송파구 가락동 79-3 대동빌딩1층]]></s_address3>	<naver_address><![CDATA[서울 송파구 가락동 79-3 대동빌딩1층]]></naver_address>	<s_tel><![CDATA[02-443-8088]]></s_tel>	<s_reserve><![CDATA[가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[불가능]]></s_holiday>	<s_park><![CDATA[가능]]></s_park>	<menu_name><![CDATA[부대찌개&철판구이]]></menu_name>	<s_time><![CDATA[10:00 - 22:00]]></s_time></item><item>	<s_num><![CDATA[20665]]></s_num>	<menu_id><![CDATA[1]]></menu_id>	<s_name><![CDATA[가락쌍용프라자보쌈점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 송파구 가락동 140]]></s_address2>	<s_address3><![CDATA[서울 송파구 가락동 140]]></s_address3>	<naver_address><![CDATA[서울특별시 송파구 가락동 140]]></naver_address>	<s_tel><![CDATA[02-400-4745]]></s_tel>	<s_reserve><![CDATA[가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[가능]]></s_holiday>	<s_park><![CDATA[가능]]></s_park>	<menu_name><![CDATA[놀부보쌈]]></menu_name>	<s_time><![CDATA[11:00 - 22:00]]></s_time></item><item>	<s_num><![CDATA[20695]]></s_num>	<menu_id><![CDATA[6]]></menu_id>	<s_name><![CDATA[가락쌍용프라자유황오리점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 송파구 가락동 140번지 [서울 송...]]></s_address2>	<s_address3><![CDATA[서울 송파구 가락동 140번지 [서울 송파구 동남로 189 쌍용프라자 224호]]></s_address3>	<naver_address><![CDATA[서울특별시 송파구 가락동 140]]></naver_address>	<s_tel><![CDATA[02-400-4745]]></s_tel>	<s_reserve><![CDATA[가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[가능]]></s_holiday>	<s_park><![CDATA[가능]]></s_park>	<menu_name><![CDATA[유황오리진흙구이]]></menu_name>	<s_time><![CDATA[11:00 - 22:00]]></s_time></item><item>	<s_num><![CDATA[504]]></s_num>	<menu_id><![CDATA[2]]></menu_id>	<s_name><![CDATA[가산2단지부대점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 금천구 가산동 60-19 SJ테크노...]]></s_address2>	<s_address3><![CDATA[서울 금천구 가산동 60-19 SJ테크노빌지하1층 142]]></s_address3>	<naver_address><![CDATA[서울금천구가산동60-19]]></naver_address>	<s_tel><![CDATA[02-3397-0977]]></s_tel>	<s_reserve><![CDATA[불가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[불가능]]></s_holiday>	<s_park><![CDATA[가능]]></s_park>	<menu_name><![CDATA[부대찌개&철판구이]]></menu_name>	<s_time><![CDATA[11:30 - 23:00]]></s_time></item><item>	<s_num><![CDATA[465]]></s_num>	<menu_id><![CDATA[2]]></menu_id>	<s_name><![CDATA[가산3단지부대점]]></s_name>	<s_address1><![CDATA[서울]]></s_address1>	<s_address2><![CDATA[서울 금천구 가산동 426-5 월드메르디...]]></s_address2>	<s_address3><![CDATA[서울 금천구 가산동 426-5 월드메르디앙벤처센타2차 102호]]></s_address3>	<naver_address><![CDATA[서울금천구가산동426-5]]></naver_address>	<s_tel><![CDATA[02-2025-8298]]></s_tel>	<s_reserve><![CDATA[불가능]]></s_reserve>	<s_pojang><![CDATA[가능]]></s_pojang>	<s_holiday><![CDATA[불가능]]></s_holiday>	<s_park><![CDATA[불가능]]></s_park>	<menu_name><![CDATA[부대찌개&철판구이]]></menu_name>	<s_time><![CDATA[11:30 - 22:30]]></s_time></item></lists>'

    #print(response)        # for debugging
    #tree = html.fromstring(response)
    #root = etree.fromstring(response)
    root = ElementTree.fromstring(response)
    #root = tree.getroot()

    storeList = []

    for child in root:
        if child.tag == 'item':
            storeInfo = {}
            storeInfo['feat'] = ''

            item = child
            for child in item:
                #print(child.tag, child.text)

                if child.tag == 's_name':
                    storeInfo['subname'] = child.text.rstrip().lstrip()
                elif child.tag == 's_address3':         # 부정확한 경우 많음 ㅠㅠ
                    storeInfo['addr'] = child.text
                elif child.tag == 'naver_address':      # naver_address 필드에 보다 정확한 주소가 기재된 경우가 있으므로 이 정보도 추출
                    storeInfo['newaddr'] = child.text   # naver_address가 상대적으로 정확해 naver_address를 addr보다 우선순위가 높은 newaddr로 지정
                elif child.tag == 's_tel':
                    storeInfo['pn'] = child.text
                elif child.tag == 'menu_name':
                    if child.text != None: storeInfo['name'] = child.text.rstrip().lstrip()
                    else : storeInfo['name'] = ''
                elif child.tag == 's_time':
                    storeInfo['ot'] = child.text
                elif child.tag == 's_reserve':
                    if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                    storeInfo['feat'] += "예약" + child.text
                elif child.tag == 's_pojang':
                    if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                    storeInfo['feat'] += "포장" + child.text
                elif child.tag == 's_park':
                    if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                    storeInfo['feat'] += "주차" + child.text
                elif child.tag == 's_holiday':
                    if storeInfo['feat'] != '': storeInfo['feat'] += ';'
                    storeInfo['feat'] += "배달" + child.text

            if storeInfo['addr'] == None: storeInfo['addr'] = ''
            if storeInfo['newaddr'] == None: storeInfo['newaddr'] = ''
            if storeInfo['ot'] == None: storeInfo['ot'] = ''
            if storeInfo['pn'] == None: storeInfo['pn'] = ''

            if storeInfo['addr'] == '' and storeInfo['newaddr'] != '': storeInfo['addr'] = storeInfo['newaddr']
            if storeInfo['newaddr'] == '' and storeInfo['addr'] != '': storeInfo['newaddr'] = storeInfo['addr']

            # post-processing
            if storeInfo['name'] == '부대찌개&철판구이':
                storeInfo['name'] = '놀부' + storeInfo['name']
                if storeInfo['subname'].endswith('부대찌개&철판구이점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-10].rstrip() + '점'
                elif storeInfo['subname'].endswith('부대찌개&철판구이'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-9].rstrip() + '점'
                elif storeInfo['subname'].endswith('부대찌개점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-5].rstrip() + '점'
                elif storeInfo['subname'].endswith('부대찌개'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-4].rstrip() + '점'
                elif storeInfo['subname'].endswith('부대점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-3].rstrip() + '점'
                elif storeInfo['subname'].endswith('부대'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-2].rstrip() + '점'
            elif storeInfo['name'] == '놀부보쌈':
                if storeInfo['subname'].endswith('보쌈점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-3].rstrip() + '점'
            elif storeInfo['name'] == '유황오리진흙구이':
                storeInfo['name'] = '놀부' + storeInfo['name']
                if storeInfo['subname'].endswith('유황오리점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-5].rstrip() + '점'
            elif storeInfo['name'] == '족보EX':
                storeInfo['name'] = '놀부족발보쌈 익스프레스'
                if storeInfo['subname'].endswith('족발보쌈EX점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-7].rstrip() + '점'
                elif storeInfo['subname'].endswith('족보EX점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-5].rstrip() + '점'
                elif storeInfo['subname'].endswith('족보EX'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-4].rstrip() + '점'
                elif storeInfo['subname'].endswith('EX점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-3].rstrip() + '점'

                if storeInfo['subname'].startswith('놀부족발보쌈'):
                    storeInfo['subname'] = storeInfo['subname'][6:].lstrip()
            elif storeInfo['name'] == '옛날통닭':
                storeInfo['name'] = '놀부' + storeInfo['name']
                if storeInfo['subname'].endswith('옛날통닭점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-5].rstrip() + '점'
                elif storeInfo['subname'].endswith('옛날통닭'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-4].rstrip() + '점'
                elif storeInfo['subname'].endswith('통닭점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-3].rstrip() + '점'

                if storeInfo['subname'].startswith('놀부옛날통닭'):
                    storeInfo['subname'] = storeInfo['subname'][6:].lstrip()
            elif storeInfo['name'] == '공수간':
                if storeInfo['subname'].startswith('공수간'):
                    storeInfo['subname'] = storeInfo['subname'][3:].lstrip()
                elif storeInfo['subname'].endswith('공수간점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname']) - 4].rstrip() + '점'
            elif storeInfo['name'] == '놀부화덕족발':
                if storeInfo['subname'].endswith('화덕족발점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-5].rstrip() + '점'
                elif storeInfo['subname'].endswith('족발점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-3].rstrip() + '점'
            elif storeInfo['name'] == '항아리갈비':
                storeInfo['name'] = '놀부' + storeInfo['name']
                if storeInfo['subname'].endswith('항아리갈비점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-6].rstrip() + '점'
                elif storeInfo['subname'].endswith('항아리'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-3].rstrip() + '점'
            elif storeInfo['name'] == '레드머그':
                if storeInfo['subname'].startswith('레드머그'):
                    storeInfo['subname'] = storeInfo['subname'][4:].lstrip()
                elif storeInfo['subname'].endswith('레드머그커피점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname']) - 7].rstrip() + '점'
            elif storeInfo['name'] == '맑은설렁탕 담다':
                if storeInfo['subname'].endswith('맑은설렁탕담다점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-8].rstrip() + '점'
                elif storeInfo['subname'].endswith('담다점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-3].rstrip() + '점'
                elif storeInfo['subname'].endswith('담다'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname']) - 2].rstrip() + '점'
            elif storeInfo['name'] == '숱불애장닭':
                storeInfo['name'] = '놀부' + storeInfo['name']
                if storeInfo['subname'].endswith('숱불에장닭점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-6].rstrip() + '점'
                elif storeInfo['subname'].endswith('장닭점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-3].rstrip() + '점'
            elif storeInfo['name'] == '벨라빈스':
                if storeInfo['subname'].endswith('벨라빈스점'):
                    storeInfo['subname'] = storeInfo['subname'][:len(storeInfo['subname'])-5].rstrip() + '점'
            elif storeInfo['name'] == '':   # added on 2019/2/8 (''인 경우가 발생해서...)
                storeInfo['name'] == '놀부'

            storeInfo['name'] = storeInfo['name'].replace(' ', '/')
            if storeInfo['subname'] != None:
                storeInfo['subname'] = storeInfo['subname'].replace(' ', '/')

            if storeInfo['name'] == '기타': storeInfo['name'] = '놀부'
            if storeInfo['name'] == storeInfo['subname']: storeInfo['subname'] = ''

            storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
