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
import ast
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

    outfile = codecs.open('autooasis_utf8.txt', 'w', 'utf-8')
    outfile.write("##NAME|SUBNAME|TELNUM|ADDR|OFFDAY\n")

    page = 1
    while True:
        storeList = getStores(page)
        if storeList == None: continue;

        for store in storeList:
            outfile.write(u'오토오아시스|')
            outfile.write(u'%s|' % store['subname'])
            outfile.write(u'%s|' % store['pn'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['offday'])

        page += 1

        if page == 999: break
        elif len(storeList) < 6: break

        time.sleep(random.uniform(0.3, 1.1))

    outfile.close()

def getStores(intPageNo):
    url = 'http://www.autooasis.com'
    api = '//Maintenance/Branch/Default.aspx?CategoryNo=T1&AOC_CallBack=true'
    data = {
        'CategoryNo': 'T1',
        'AOC_CallBack': 'true',
    }
    params = urllib.urlencode(data)
    print(intPageNo)

    hdr2 = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'ko-KR,ko;en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }

    params = 'AOC_UpdatePage=true&__VIEWSTATE=%2FwEPDwUKMTc1ODgxMTQ4Nw8WAh4LQ3VycmVudFBhZ2UCBhYCZg9kFgICBQ9kFgYCAw8WAh4Dc3JjBTIvaW1hZ2VzL2F1dG9vYXNpcy9pbWFnZXMvY29udGVudHMvc3ViX3Zpc3VhbF9ULmdpZmQCBQ8PFgIeB1Zpc2libGVnZBYCAgIPDxYCHwJnZGQCBw9kFgoCAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQhSZWdpb25fTB4ORGF0YVZhbHVlRmllbGQFCFJlZ2lvbl9MHgtfIURhdGFCb3VuZGdkEBUSBuyghOyytAbshJzsmrgG6rCV7JuQBuuMgOyghAbstqnrgqgG7IS47KKFBuy2qeu2gQbsnbjsspwG6rK96riwBuq0keyjvAbsoITrgqgG7KCE67aBBuu2gOyCsAbqsr3rgqgG7Jq47IKwBuygnOyjvAbrjIDqtawG6rK967aBFRIABuyEnOyauAbqsJXsm5AG64yA7KCEBuy2qeuCqAbshLjsooUG7Lap67aBBuyduOyynAbqsr3quLAG6rSR7KO8BuyghOuCqAbsoITrtoEG67aA7IKwBuqyveuCqAbsmrjsgrAG7KCc7KO8BuuMgOq1rAbqsr3rtoEUKwMSZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgFmZAIDDxAPFgIfBWdkEBUBDuq1rC%2FqtbAg7ISg7YOdFQEAFCsDAWcWAWZkAgUPDxYEHgRUZXh0ZR4OU2NyaXB0RnVuY05hbWUFDEVtdHlTY3JpcHQoKRYCHgpvbmtleXByZXNzBU5yZXR1cm4gcHJlc3NFbnRlcignRW10eVNjcmlwdCgpJywgJ2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjIkaWJ0U2VhcmNoJywgdHJ1ZSlkAgkPFgIeC18hSXRlbUNvdW50AgYWDGYPZBYMZg8VAQRGNDE4ZAIBDxUBD%2Bq0keyjvOyGoeygleygkGQCAw8VAQRGNDE4ZAIEDw8WBB4ISW1hZ2VVcmwFW2h0dHA6Ly9maWxldXAubWlsZXN0b3J5LmNvbS9pbWFnZTIuYXNoeD9GaWxlPSZ3aWR0aD0xMDgmaGVpZ2h0PTgxJm5vSW1hZ2U9YW9fbm9faW1hZ2UwMy5qcGceDUFsdGVybmF0ZVRleHQFD%2Bq0keyjvOyGoeygleygkGRkAgUPFQEERjQxOGQCBg8VBA%2FqtJHso7zshqHsoJXsoJAu6rSR7KO8IOq0keyCsOq1rCDrj4TsgrDrj5kgODM3LTco7Iah64%2BE66GcMTcyKQwwNjItOTQxLTk4MTEd7LKr7Ke47KO8L%2ByFi%2BynuOyjvCDsnbzsmpTsnbxkAgEPZBYMZg8VAQRGMDYxZAIBDxUBD%2Bq0keyjvOyImOyZhOygkGQCAw8VAQRGMDYxZAIEDw8WAh8KBVtodHRwOi8vZmlsZXVwLm1pbGVzdG9yeS5jb20vaW1hZ2UyLmFzaHg%2FRmlsZT0md2lkdGg9MTA4JmhlaWdodD04MSZub0ltYWdlPWFvX25vX2ltYWdlMDMuanBnZGQCBQ8VAQRGMDYxZAIGDxUED%2Bq0keyjvOyImOyZhOygkCXqtJHso7wg6rSR7IKw6rWsIOyepeuNleuPmSAxMjU167KI7KeADDA2Mi02NTQtNTI3NR3ssqvsp7jso7wv7IWL7Ke47KO8IOydvOyalOydvGQCAg9kFgxmDxUBBEY0NDdkAgEPFQEJ6rSR7KeE7KCQZAIDDxUBBEY0NDdkAgQPDxYEHwoFW2h0dHA6Ly9maWxldXAubWlsZXN0b3J5LmNvbS9pbWFnZTIuYXNoeD9GaWxlPSZ3aWR0aD0xMDgmaGVpZ2h0PTgxJm5vSW1hZ2U9YW9fbm9faW1hZ2UwMy5qcGcfCwUJ6rSR7KeE7KCQZGQCBQ8VAQRGNDQ3ZAIGDxUECeq0keynhOygkCDshJzsmrgg6rSR7KeE6rWsIOq1rOydmOuPmSA2OS0xOQswMi00NTgtMzQwMB3ssqvsp7jso7wv7IWL7Ke47KO8IOydvOyalOydvGQCAw9kFgxmDxUBBEEyOTRkAgEPFQEP6rWs66Gc6re466aw7KCQZAIDDxUBBEEyOTRkAgQPDxYCHwoFhgFodHRwOi8vZmlsZXVwLm1pbGVzdG9yeS5jb20vaW1hZ2UyLmFzaHg%2FRmlsZT0vVXBsb2FkL0F1dG8vRXRjLzIwMTMvNC8yMy%2FqtazroZzqt7jrprAuanBnJndpZHRoPTEwOCZoZWlnaHQ9ODEmbm9JbWFnZT1hb19ub19pbWFnZTAzLmpwZ2RkAgUPFQEEQTI5NGQCBg8VBA%2FqtazroZzqt7jrprDsoJAi7ISc7Jq4IOq1rOuhnOq1rCDqtazroZzrj5kgMTAwLTEwLgswMi04NTgtNTQzMh3ssqvsp7jso7wv7IWL7Ke47KO8IOydvOyalOydvGQCBA9kFgxmDxUBBEEwNzNkAgEPFQEP6rWs66%2B46rO164uo7KCQZAIDDxUBBEEwNzNkAgQPDxYEHwoFfmh0dHA6Ly9maWxldXAubWlsZXN0b3J5LmNvbS9pbWFnZTIuYXNoeD9GaWxlPS9VcGxvYWQvQXV0by9BTy9QYXJ0L09hc2lzL0EwNzMuanBnJndpZHRoPTEwOCZoZWlnaHQ9ODEmbm9JbWFnZT1hb19ub19pbWFnZTAzLmpwZx8LBQ%2Fqtazrr7jqs7Xri6jsoJBkZAIFDxUBBEEwNzNkAgYPFQQP6rWs66%2B46rO164uo7KCQH%2Bqyveu2gSDqtazrr7jsi5wg6rO164uo64%2BZIDIwOC4MMDU0LTQ2Mi0xMDEyHeyyq%2BynuOyjvC%2FshYvsp7jso7wg7J287JqU7J28ZAIFD2QWDGYPFQEERjQ5MWQCAQ8VAQnqtazslZTsoJBkAgMPFQEERjQ5MWQCBA8PFgIfCgVbaHR0cDovL2ZpbGV1cC5taWxlc3RvcnkuY29tL2ltYWdlMi5hc2h4P0ZpbGU9JndpZHRoPTEwOCZoZWlnaHQ9ODEmbm9JbWFnZT1hb19ub19pbWFnZTAzLmpwZ2RkAgUPFQEERjQ5MWQCBg8VBAnqtazslZTsoJAs64yA6rWsIOu2geq1rCDqtazslZTrj5kgODA1LTQo6rWs7JWU66GcIDM0MCkMMDUzLTMyMS05MTAwHeyyq%2BynuOyjvC%2FshYvsp7jso7wg7J287JqU7J28ZAILDw8WCB4NVG90YWxSb3dDb3VudALwAx4MQ3VycmVudEluZGV4AgYeCExpc3RTaXplAgYeCFBhZ2VTaXplAgVkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUjY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMiRpYnRTZWFyY2icWloSgJK9IPp4d9RN0teBrIEr3g%3D%3D&__VIEWSTATEGENERATOR=A83CB214&ctl00$ContentPlaceHolder2$ddlRegion=&ctl00$ContentPlaceHolder2$ddlCity=&ctl00$ContentPlaceHolder2$txtSearch=&__EVENTTARGET=ctl00%24ContentPlaceHolder2%24pagerG&__EVENTARGUMENT='
    params += str(intPageNo)

    try:
        req = urllib2.Request(url + api, params, headers=hdr2)  # POS 방식일 땐 이렇게 호출해야 함!!!
        req.get_method = lambda: 'POST'
        result = urllib2.urlopen(req)
    except:
        print('Error calling the API');
        return None

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);
        return None

    response = result.read()
    #print(response)    # for debugging
    idx = response.find('Holder2$repCenter":"')
    if idx == -1: return None

    response = response[idx+20:]
    idx = response.find('","ctl00$ContentPlaceHolder2$')
    if idx == -1: return None
    response = response[:idx]
    #response = response[:idx].replace('\\r', '').replace('\\t', '').replace('\\n', '').replace('\\"', '"')

    # 한글코드 변환을 위해 json 라이브러리 임시로 사용
    teststr = '{ "abc": "' + response + '" }'
    test_json = json.loads(teststr)
    response = test_json['abc'].lstrip().rstrip()
    #print(response)

    tree = html.fromstring('<head><meta charset="utf-8"/></head>' + response)
    #tree = html.fromstring('<?xml version="1.0" encoding="utf-8"?> ' + response)

    entityList = tree.xpath('//div[@class="office_info"]')

    storeList = []
    for i in range(len(entityList)):
        infoList = entityList[i].xpath('.//ul//li')

        if (infoList == None): continue;  # for safety
        elif (len(infoList) < 4): continue  # 최소 5개 필드 있어야

        storeInfo = {}
        subname = "".join(infoList[0].itertext()).lstrip().rstrip()
        if subname.startswith('지점 :'): subname = subname[4:].lstrip()
        storeInfo['subname'] = subname.replace(' ', '/')

        storeInfo['addr'] = ''
        strtemp = "".join(infoList[1].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('주소 :'): strtemp = strtemp[4:].lstrip()
            storeInfo['addr'] = strtemp

        storeInfo['pn'] = ''
        strtemp = "".join(infoList[2].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('전화 :'): strtemp = strtemp[4:].lstrip()
            storeInfo['pn'] = strtemp.replace('.', '-').replace(')', '-')

        storeInfo['offday'] = ''
        strtemp = "".join(infoList[3].itertext())
        if strtemp != None:
            strtemp = strtemp.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if strtemp.startswith('휴일 :'): strtemp = strtemp[4:].lstrip()
            storeInfo['offday'] = strtemp

        storeList += [storeInfo]

    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
