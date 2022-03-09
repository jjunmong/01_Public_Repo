import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('123_바디프랜드.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 0
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page +=10
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(inPageNo):
    url = 'https://m.bodyfriend.co.kr/api/company/getAllStore?lat=37.4813233&lng=127.0440003&firstLimitIndex={}&lastLimitIndex=10&sido=&gu=&searchTxt='.format(inPageNo)
    pageString = requests.get(url).text
    jsonString = json.loads(pageString)
    entityList = jsonString['resultData']
    result = []
    for info in entityList:
        name = '바디프랜드'
        branch = info['branch_nm']
        branch = branch.replace(' ','')
        addr = info['addr']
        tell = info['tel']
        time = info['business_hour']
        cordx = info['lng']
        cordy = info['lat']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time,'cordx':cordx,'cordy':cordy})
    return result


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()