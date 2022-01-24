import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('09_닭익는마을.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

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
    url = 'https://www.ckpalace.co.kr/shop/shopListJs.asp'
    data = {
        'lat': '37.494839',
        'lng': '127.121911',
        'search_text': '',
    }
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        name = '닭익는마을'
        branch = info['branch_name']
        addr = info['branch_address']
        tell = info['branch_tel']
        xcord = info['wgs84_x']
        ycord = info['wgs84_y']
        result.append({"name":name, "branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
