import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('06_이베코.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|CODE\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s\n' % store['agencycode'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo():
    url = 'https://www.kaida.co.kr/ko/brand/exhibitionListAjax.do'
    data = {
        'searchShape': 'asCVYn',
        'siDoCode': '',
        'saleCarType': 'CV',
        'brandId': '034',
    }
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    entityList = jsonString['result']
    result = []
    for info in entityList :
        name = '이베코'
        branch = info['name']
        addr = info['address']
        tell = info['telNo']
        agencycode = info['asAgencySeq']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'agencycode':agencycode})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

