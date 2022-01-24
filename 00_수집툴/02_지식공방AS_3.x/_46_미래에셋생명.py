import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('46_미래에셋생명.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page+=1
        if store_list == [] : break
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(intPageNo):
    url ="https://life.miraeasset.com/home/portal/HO030801010000.do"
    data = {
        # 'pageNum': '4',
        'srchOpt': '1',
        'srchTxt': '',
        'addr': '',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'AJAX': 'true',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '34',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'WMONID=DKMY9iYCdkX; JSESSIONID=nE4fiW2vu52UeRZgFQwUhQaEkjWydD61b6fEsmdibQxLbWDFJAqksbSmMaUl7aVj.Y21zX2RvbWFpbi92dXBhY21zMDFfSG9tZUFwcDEz; PCID=8c3fb7b0-22d2-ba0e-509b-3a3c584daf86-1612938596756; acTime=1612940548743',
        'Host': 'life.miraeasset.com',
        'Origin': 'https://life.miraeasset.com',
        'Pragma': 'no-cache',
        'Referer': 'https://life.miraeasset.com/home/index.do?page=7&txtKeyField=&txtKeyWord=&txtKeyWord2=&txtKeyWord3=&kind=',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['pageNum'] = intPageNo
    pageString = requests.post(url, data = data, headers = headers).text
    jsonString = json.loads(pageString)
    entityList = jsonString['list']
    result = []
    for info in entityList:
        try:
            name= '미래에셋생명'
            branch = info['BR_NM']
            addr = info['ADDR1']
            tell = info['TEL_NO']
            time = info['WORK_DTM']
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()