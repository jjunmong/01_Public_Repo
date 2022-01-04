import sys
import requests
import bs4
import codecs
import time
import random
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def main():

    outfile = codecs.open('84_명랑핫도그.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종', '제주']
    for sido in sido_list:
        storeList = getStoreInfo(sido)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
def getStoreInfo(regionList):
    url = 'https://myungranghotdog.com/kor/store/list.do'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '23',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=E150B0145144F328CF5DFEA2C6B19D54',
        'Host': 'myungranghotdog.com',
        'Origin': 'https://myungranghotdog.com',
        'Pragma': 'no-cache',
        'Referer': 'https://myungranghotdog.com/kor/store/list.do',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    data = {}
    data['area'] = regionList
    print(regionList)
    pageString = requests.post(url,data=data ,headers = headers, verify = False).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find('div',{"class":"list"})
    li = div.find_all('li')
    result = []
    for info in li:
        try:
            name = '명량시대쌀핫도그'
            branch = info.find('p',{"class":"store name"}).text
            addr = info.find('p',{"class":"add"}).text
            tell = info.find('p',{"class":"call"}).text
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()