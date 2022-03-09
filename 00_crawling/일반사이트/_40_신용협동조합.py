import sys
import time
import codecs
import requests
import random
import json
import bs4
import urllib.parse

def main():

    outfile = codecs.open('40_신용협동조합.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    code_list = getStore_List()
    for code in code_list:
        store_list = getStoreInfo(code['code1'],code['code2'])
        print(code['code1'],code['code2'])
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStore_Code(sidocode, intPageNo):
    url = 'http://www.cu.co.kr/cu/ad/cuSearch.do'
    data = {
        # 'currPage': '23',
        'maxSn': '10',
        'useInfoCd': '',
        'searchTxt': '',
        'sysId': 'cu',
        'cuMbrCd': '',
        'cuSearchTab': '1',
        'searchTy': '',
        'mi': '100076',
        # 'ctprvn': 'sido02',
        'minSn': '0',
        'cuNo': '',
        'signgu': '',
    }
    data['currPage']=intPageNo
    data['ctprvn']=sidocode
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '130',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=gMHXImS53fcEqzOCmANze79N0ADHzXwq2DBFcFOaVKJmK9B1JwFFW2K41TRFeGxi.amV1c19kb21haW4vbmhtaG9tZTE=; JSESSIONID=amea1CSWFapE4O7umMj8pFyKfaeZqLK32AwEOkBCCVtIV0VuJC1AYG9RIs3AE3Ll.deliever1_servlet_engine2',
        'Host': 'www.cu.co.kr',
        'Origin': 'http://www.cu.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://www.cu.co.kr/cu/ad/cuSearch.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    }
    pageString = requests.post(url, data = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    table = bsObj.find('table')
    tr = table.find_all('tr')
    result = []
    for info in tr:
        try:
            code = info.find('a')['onclick']
            code = str(code).split("'")
            code1 = code[1]
            code2 = code[3]
        except:pass
        else:
            result.append({'code1':code1,'code2':code2})
    return result

def getStore_List():
    sido_list = ['sido01', 'sido02', 'sido03', 'sido04', 'sido05', 'sido06', 'sido07', 'sido08', 'sido09', 'sido10',
                 'sido11', 'sido12', 'sido13', 'sido14', 'sido15', 'sido16', 'sido17']
    result = []

    for sido in sido_list:
        page = 1
        while True:
            result = result + getStore_Code(sido,page)
            print(sido, page)
            page+=1
            if getStore_Code(sido, page) == [] : break
            time.sleep(random.uniform(0.3, 0.9))
    return result

def getStoreInfo(code1, code2):
    url = 'http://www.cu.co.kr/cu/ad/assc.do'
    data = {}
    data['cuNo'] = code1
    data['cuMbrCd'] = code2
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    name = '신용협동조합'
    branch = jsonString['cuNm']
    addr = jsonString['mnbrDongAddr']
    tell = jsonString['ownTelNo']
    xcord = jsonString['x']
    ycord = jsonString['y']
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()