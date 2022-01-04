import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('114_새마을식당.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        print(page)
        if storeList == None : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page +=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://theborndb.theborn.co.kr/wp-json/api/get_store/?state=9&category=267&depth1=&depth2=&paged={}&search_string='.format(intPageNo)
    pageString = requests.get(url).text
    jsonString = json.loads(pageString)
    entityList = jsonString['results']
    result = []
    try:
        for info in entityList:
            name = '새마을식당'
            branch = info['store_name']
            addr = info['store_address']
            tell = info['store_phone']
            time = info['store_hours']
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    except : pass
    else:
        return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()