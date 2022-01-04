import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('107_테라로사.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s\n' % store['addr'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo():
    url = 'https://dbdev.co.kr/Dbk/Front/Board/BoardList?location='
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ECSESSID=d268fe67d09bede378db5dd7023ee938; basketcount_1=0; atl_epcheck=1; atl_option=1%2C1%2CH; CUK45=cuk45_haksanshopping_d268fe67d09bede378db5dd7023ee938; CUK2Y=cuk2y_haksanshopping_d268fe67d09bede378db5dd7023ee938; CID=CID4f212dfae69cd287814e87e996cbcfe0; CID4f212dfae69cd287814e87e996cbcfe0=06159b2a5b079600197cbb8c010e1e7b%3A%3A%3A%3A%3A%3Ahttps%3A%2F%2Fwww.google.co.kr%2F%3A%3A%EA%B5%AC%EA%B8%80%3A%3A1%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%2F%3A%3A1597296294%3A%3A%3A%3Appdp%3A%3A1597296294%3A%3A%3A%3A%3A%3A%3A%3A; vt=1597296294; wcs_bt=s_4b9e1381a5ac:1597296296',
        'Host': 'terarosa.com',
        'Pragma': 'no-cache',
        'Referer': 'http://terarosa.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '테라로사'
            branch = info.find('span',{"class":"store-subject"}).text
            addr = str(info.select('span')[2]).replace('<span><span class="point">A</span>','').replace('</span>','')
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()