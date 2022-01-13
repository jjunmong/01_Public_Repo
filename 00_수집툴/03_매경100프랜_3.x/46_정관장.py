import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('46_정관장.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['time'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    outfile.close()

def getStoreInfo():
    url = 'https://www.kgc.co.kr/intro/store/searchStore.do?param1=&param2=&param3=&param4=&param5=&param6=&param7=P0001&isAllow=false&_=1606798972669'
    pageString = requests.post(url).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        name = '정관장'
        branch = info['storeName']
        addr1 = info['sido']
        if addr1 ==None : addr1 = ''
        addr2 = info['gugun']
        if addr2 == None: addr2 = ''
        addr3 = info['address']
        if addr3 == None: addr3 = ''
        addr = addr1+ ' ' + addr2 + ' ' + addr3
        addr = addr.replace('  ',' ')
        tell = info['storePhone']
        time = info['operationHourInfo']
        xcord = info['longitude']
        ycord = info['latitude']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
