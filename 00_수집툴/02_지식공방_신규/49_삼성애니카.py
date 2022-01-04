import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('49_삼성애니카.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|CORDX|CORDY\n")

    code_list = getStoreInfo_code()
    for code in code_list:
        store_list = getStoreInfo(code)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['time'])
            outfile.write(u'%s|' % store['cordx'])
            outfile.write(u'%s\n' % store['cordy'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo_code():
    url = 'https://myanycar.com/CR_MyAnycarWeb/data/VD.HDSM0096.do'
    data ={
        'sidoGubun' : '',
        'gusiGubun' : '',
        'corpGubun' : '7',
        'serviceType' : '',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '691',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': 'DSESSIONID=L0z9-cymOYxRmTj9ysQNLx9qJAzjeqleCipbI2zctQUGv6SyXKgl!-1367315392!-968409439; _ga=GA1.2.706907754.1593398907; _gid=GA1.2.1374111756.1593398907; type=0_0_000; param=00000000000; _gat=1',
        'Host': 'myanycar.com',
        'Origin': 'https://myanycar.com',
        'Pragma': 'no-cache',
        'Referer': 'https://myanycar.com/CR_MyAnycarWeb/page/VD.MPDG0222.do?tab=3',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-SFMI-INTLOG': 'N72010-000910^^Y^^^^^^^^^^^^^^^^^',
    }
    pageString = requests.post(url, data = data, headers = headers).text
    jsonstring = json.loads(pageString)
    entityList = jsonstring['responseMessage']['body']['DATA']
    result = []
    for info in entityList:
        code = info['DEPT_CD']
        result.append(code)
    return result

def getStoreInfo(code):
    url = 'https://myanycar.com/CR_MyAnycarWeb/data/VD.HDSM0097.do'
    data={}
    data['KEY_CD'] = code
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '691',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': 'DSESSIONID=L0z9-cymOYxRmTj9ysQNLx9qJAzjeqleCipbI2zctQUGv6SyXKgl!-1367315392!-968409439; _ga=GA1.2.706907754.1593398907; _gid=GA1.2.1374111756.1593398907; type=0_0_000; param=00000000000; _gat=1',
        'Host': 'myanycar.com',
        'Origin': 'https://myanycar.com',
        'Pragma': 'no-cache',
        'Referer': 'https://myanycar.com/CR_MyAnycarWeb/page/VD.MPDG0222.do?tab=3',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-SFMI-INTLOG': 'N72010-000910^^Y^^^^^^^^^^^^^^^^^',
    }
    print(code)
    pageString = requests.post(url, data = data, headers = headers).text
    jsonstring = json.loads(pageString)
    entityList = jsonstring['responseMessage']['body']
    result = []
    name = '애니카랜드'
    branch = entityList['corp_name']
    branch = branch.replace('애니카랜드 ','').replace('(주)','')
    addr = entityList['corp_addr1'] + ' ' + entityList['corp_addr2']
    tell = entityList['corp_tel']
    time = entityList['BAS_BSNS_TIME']
    cordx = entityList['corp_longitude']
    cordy = entityList['corp_latitude']
    result.append({"name":name, "branch":branch,"addr":addr,"tell":tell,"time":time,"cordx":cordx,"cordy":cordy})
    return result


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

