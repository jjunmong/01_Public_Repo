import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('117_한신포차.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page+=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'http://theborndb.theborn.co.kr/wp-json/api/get_store/?state=9&category=270&depth1=&depth2=&paged={}&search_string='.format(intPageNo)
    pageString = requests.get(url).text
    jsonString = json.loads(pageString)
    try:
        entityList = jsonString['results']
        result = []
        for info in entityList:
            name = '한신포차'
            branch = info['store_name']
            addr = info['store_address']
            tell = info['store_phone']
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    except:pass
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()