import sys
import time
import codecs
import requests
import random
import bs4
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():

    outfile = codecs.open('68_장례식장.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page+= 1

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(intPagNo):
    url = 'https://www.15774129.go.kr/portal/fnlfac/facList.ajax'
    data = {
        'pageInqCnt': '12',
        'curPageNo': '2',
        'sidocd': '',
        'gungucd': '',
        'companyname': '',
        'facilitygroupcd': 'TBC0700001',
        'publiccode': 'A',
    }
    data['curPageNo'] = intPagNo
    response = requests.post(url, data = data, verify = False).text
    jsonString = json.loads(response)
    entityList = jsonString['list']
    result = []
    for info in entityList:
        name = ''
        branch = info['companyname']
        addr = info['fulladdress']
        tell = info['telephone']
        xcord = info['longitude']
        ycord = info['latitude']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()