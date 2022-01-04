import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('63_메가마트.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo():
    url = 'http://home.megamart.com/boardApi/query'
    data = {
        'storeCode': '',
        'method': 'store.selectStore',
        'applyCamelCase': 'true',
    }
    response = requests.post(url, data = data).text
    jsonString = json.loads(response)
    result = []
    for info in jsonString:
        name = '메가마트'
        branch = info['storeName']
        addr = info['address']
        tell = info['telNumber']
        xcord = info['lon']
        ycord = info['lat']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()