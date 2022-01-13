import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('77_죠스떡볶이.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")


    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s\n' % store['addr'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
def getStoreInfo():
    url = 'http://www.jawsfood.co.kr/store/store_search.html'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'E2481=20181010; _ga=GA1.3.977774334.1593678248; _gid=GA1.3.720277203.1593678248; wcs_bt=s_2ae26e167f3f:1593678416',
        'Host': 'www.jawsfood.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://www.jawsfood.co.kr/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    tr = bsObj.find('div',{"class":"list"})
    li = tr.find_all('li')
    result = []
    for info in li:
        name = '죠스떡볶이'
        branch = info.find('p',{"class":"name"}).text.replace(' ','')
        addr = info.find('p',{"class":"address"}).text.replace('\xa0','')
        result.append({'name':name,'branch':branch,'addr':addr})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()