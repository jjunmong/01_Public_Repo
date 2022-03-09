import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('108_폴바셋.txt', 'w', 'utf-8')
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
    url = 'https://www.baristapaulbassett.co.kr/store/getStoreList.pb'
    data = {
        'searchType': '',
        'surDistance': '',
        'myLocLati': '37.5157921',
        'myLocLongi': '127.12317879999999',
        'areaCd': '',
        'cityCd': '',
        'listSort': 'D',
        'shopName': '',
    }
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        try:
            name = '폴바셋'
            branch = str(info['shopName']).replace(' ','')
            addr = info['address']
            tell = info['tel']
            cordx = info['locLongi']
            cordy = info['locLati']
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'cordx':cordx,'cordy':cordy})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()