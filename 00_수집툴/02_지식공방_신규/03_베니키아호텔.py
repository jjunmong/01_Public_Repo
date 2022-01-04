import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('03_베니키아호텔.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|ROOMCNT|HOTELNO\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['roomcnt'])
        outfile.write(u'%s\n' % store['hotelNo'])

    outfile.close()

def getStoreInfo():
    url = 'https://www.benikea.com/common/proxy.jsp'
    data = {
        'url': 'http://api.benikea.com/hotel/getChainHotels',
        'langCd': 'KOR',
        'channelCd': '0000000001',
        'regionCd': '1',
        'sort': '4',
    }
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    entityList = jsonString['data']['hotelList']
    result = []
    for info in entityList:
        branch = info['hotelNm']
        if branch.endswith('호텔'): branch = branch.replace('호텔', '').replace('베니키아', '베니키아호텔|').replace(' ','')
        else: branch = branch.replace(' ','').replace('호텔','호텔|').replace('베니키아홈더제주리조트','베니키아호텔|홈더제주리조트')
        addr = info['addrName']
        tell = info['bsnsTelNo']
        roomcnt = info['roomCnt']
        hotelNo = info['hotelNo']
        result.append({"branch":branch,"addr":addr,"tell":tell,"roomcnt":roomcnt,"hotelNo":hotelNo})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()