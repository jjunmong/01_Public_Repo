import requests
import json
import codecs
import time
import random

def main():
    outfile = codecs.open('제로페이(강남구).txt', 'w', 'utf-8')
    dict_keys1 = getStoreInfo(1,1,10)[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys','').replace('[','').replace(']','').replace('(','').replace(')','').replace(',','|').replace("'","").replace(' ','')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)
    page = 1
    firstIndex = 1
    lastIndex = 10
    while True:
        store_list = getStoreInfo(page,firstIndex, lastIndex)[0]
        print(page, firstIndex, lastIndex)
        if store_list == [] : break
        for store in store_list:
            column_num = 0
            while True:
                if column_num == len(key_list) : break
                elif column_num == len(key_list)-1 :
                    outfile.write(u'%s\n' % store['%s' % key_list[column_num]])
                else:
                    outfile.write(u'%s|' % store['%s' % key_list[column_num]])
                column_num +=1
        time.sleep(random.uniform(0.2, 0.3))
        page +=1
        firstIndex += 10
        lastIndex += 10
    outfile.close()

def getStoreInfo(intPageNo, firstIndex, lastIndex):
    url = 'https://www.zeropay.or.kr/intro/frncSrchList_json.do'
    data ={
        # 'pageIndex': '1',
        'recordCountPerPage': '10',
        # 'firstIndex': '1',
        # 'lastIndex': '10',
        'searchCondition': '',
        'tryCode': '01',
        'skkCode': '01',
        'pobsAfstrName': '',
        'pobsBaseAddr': '',
        'bztypName': '',
        'frc_se': '',
        'bztypTxt': '',
        '_csrf': '64f14583-9cac-4769-b490-5fabdef719b5',
    }
    headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '199',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_xm_webid_1_=758034826; JSESSIONID=E0ydiRQQ7JO7lwCyx5jbdsPGKQGprGFj1qJH2BykUdg9PZSHphnZ67CPgrIPuBS2.enBheV9kb21haW4venBheS1ob21lcGFnZS0x; ACEUACS=1579483474047131591; AUAZ1A78776=1640588355851225022%7C2%7C1640588355851225022%7C1%7C1640588355833M005M; ACEUCI=1; ACEFCID=UID-61C96443F991ADDC1FD3AF96; _gcl_au=1.1.1865351886.1640588356; _ga=GA1.3.374619496.1640588356; _gid=GA1.3.1215463375.1640588356; _gat_gtag_UA_156020264_1=1; wcs_bt=s_4ab8cf5ec090:1640588375; ARAZ1A78776=httpswwwzeropayorkrmaindopgmIdPGM0081httpswwwzeropayorkrmaindopgmIdPGM0081; ASAZ1A78776=1640588355851225022%7C1640588379499646490%7C1640588355851225022%7C0%7Cbookmark',
        'Host': 'www.zeropay.or.kr',
        'Origin': 'https://www.zeropay.or.kr',
        'Pragma': 'no-cache',
        'Referer': 'https://www.zeropay.or.kr/main.do?pgmId=PGM0081',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['pageIndex'] = intPageNo
    data['firstIndex'] = firstIndex
    data['lastIndex'] = lastIndex
    pageString = requests.post(url, data = data , headers = headers).text
    jsonString = json.loads(pageString)
    list = jsonString['list']
    data = []
    dict_key = ''
    for info in list:
        try:
            bztypName = info['bztypName']
            pobsAfstrName = info['pobsAfstrName']
            pobsBaseAddr = info['pobsBaseAddr']
            pobsDtlAddr = info['pobsDtlAddr']
            pobsGnrlTelno = info['pobsGnrlTelno']
            data_dict = {'bztypName':bztypName,'pobsAfstrName':pobsAfstrName,'pobsBaseAddr':pobsBaseAddr,'pobsDtlAddr':pobsDtlAddr,'pobsGnrlTelno':pobsGnrlTelno}
            dict_key= data_dict.keys()
        except:pass
        else:
            data.append(data_dict)
    return data, dict_key
main()
