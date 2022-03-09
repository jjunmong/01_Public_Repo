import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('105_아티제.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|CORDX|CORDY\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['cordx'])
        outfile.write(u'%s\n' % store['cordy'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo():
    url = 'https://api.flyground.co.kr/cafeartisee/web/store'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://www.cafeartisee.com',
        'pragma': 'no-cache',
        'referer': 'https://www.cafeartisee.com/store/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        name = '아티제'
        branch = info['name']
        addr = info['addr1'] + ' ' + info['addr2']
        tell = info['tel']
        cordx = info['longitude']
        cordy = info['latitude']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'cordx':cordx,'cordy':cordy})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()