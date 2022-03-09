import requests
import codecs
import time
import sys
import random
import bs4
import json


def main():

    outfile = codecs.open('20_더샘.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|ID\n")

    page = 1
    while True :
        store_list = getStoreInfo(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['id'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = "https://www.thesaemcosmetic.com/api/retail/local?q.area=&q.clsf=&q.retailKeyword=&currentPage={}".format(intPageNo)
    pageString = requests.get(url).text
    jsonString = json.loads(pageString)
    print(url, intPageNo)
    result = []
    for info in jsonString:
        try:
            id = info['id']
            name = '더샘'
            branch =info['name']
            branch = str(branch).replace(' ','')
            addr1 = info['addr1']
            addr2 = info['addr2']
            addr3 = info['addr3']
            addr = addr1 + ' ' + addr2 + ' ' + addr3
            tell = info['tel']
        except: pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"id":id})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()