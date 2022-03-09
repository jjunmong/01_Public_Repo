import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('111_오설록.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|\n")

    page = 0
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
    url = 'https://www.osulloc.com/kr/ko/store?sort=new&p={}'.format(intPageNo)
    headers ={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'WMONID=z7kP0_uzyN9; JSESSIONID=0000iNcP8cUEJ7Rq55YN20yGvpq:1cu3j3obv; RB_PCID=1597308848834532837; _ga=GA1.2.632592590.1597308849; _gid=GA1.2.1167307059.1597308849; _gcl_au=1.1.97315525.1597308849; RB_GUID=1811fe13-f9d2-4b86-bbb1-a56c25f8f847; _gat_UA-110770460-6=1; RB_SSID=kHA4lUS3e0; wcs_bt=s_bf516546e48:1597309120; _dc_gtm_UA-110770460-6=1',
        'Host': 'www.osulloc.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.osulloc.com/kr/ko/store?sort=new&p=1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '오설록'
            branch = info.find('a',{"class":"store-name"}).text.replace(' ','')
            addr = info.find('td',{"class":"store-address"}).text
            tell = info.find('div',{"class":"tel"}).text
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()