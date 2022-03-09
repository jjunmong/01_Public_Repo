import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('112_봉구비어.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        print(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page +=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://bonggubeer.com/store/guide/?pageid={}'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.1591114649.1585203911; PHPSESSID=r8ljpiskkb2b0glfr2kqmlc250; _gid=GA1.2.781155713.1597366208; wcs_bt=74f6a89354315:1597368658; _gat_gtag_UA_116906577_1=1',
        'Host': 'bonggubeer.com',
        'Pragma': 'no-cache',
        'Referer': 'http://bongubeer.com/store/guide/?pageid=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '봉구비어'
            branch = info.find('div',{"class":"kboard-store-cut-strings"}).text.replace('\n','').replace('\t','').replace('\xa0','').lstrip().rstrip()
            addr = info.find('td',{"class":"kboard-list-address"}).text
            tell = info.find('td',{"class":"kboard-list-tel"}).text
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()