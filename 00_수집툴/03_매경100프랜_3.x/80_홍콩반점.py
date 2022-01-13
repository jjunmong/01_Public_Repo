import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('80_홍콩반점.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True :
        storeList = getStoreInfo(page)
        if storeList == None : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://theborndb.theborn.co.kr/wp-json/api/get_store/?state=9&category=268&depth1=&depth2=&paged={}&search_string='.format(intPageNo)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'theborndb.theborn.co.kr',
        'Origin': 'http://www.theborn.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://www.theborn.co.kr/store/domestic-store/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    print(intPageNo, url)
    pageString = requests.get(url, headers = headers).text
    jsonString = json.loads(pageString)
    entityList = jsonString['results']
    result = []
    try:
        for info in entityList:
            name = '홍콩반점0410+'
            branch = info['store_name']
            addr = info['store_address']
            tell = info['store_phone']
            time = info['store_hours']
            result.append({'name':name, 'branch':branch,'addr':addr,'tell':tell,'time':time})
    except :pass
    else:
        return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()