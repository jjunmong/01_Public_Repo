import sys
import time
import codecs
import requests
import random
import json
import bs4

sido_list = ['117', '118', '122', '116', '125', '127', '124', '129', '121', '131', '126', '120', '128', '132', '123', '130', '119']


def main():

    outfile = codecs.open('33_ABC마트.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCODR|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    outfile.close()

def getStoreInfo():
    url = 'https://www.a-rt.com/board/store/list?areaNo=&areaDtlSeq=&storeGbnCode=&storeServiceCode=&storeSearchWord=&_=1587518662167'
    pageString = requests.get(url).text
    jsonString = json.loads(pageString)
    list  = jsonString['list']
    result = []
    for info in list:
        name = 'ABC마트'
        branch = info['storeName']
        branch = str(branch).replace(' ','')
        addr = info['postAddrText']
        tell = info['telNoText']
        if tell == '000-0000-0000' : tell = ''
        xcord = info['ypointText']
        ycord = info['xpointText']
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()