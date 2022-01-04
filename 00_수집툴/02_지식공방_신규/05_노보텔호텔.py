import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('05_노보텔호텔.txt', 'w', 'utf-8')
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
    url = 'https://www.ambatel.com/ko/hotel/selBrandHotelList.do?page=1&selBrandCode=&PROD_TYPE=M0801%2523%2523%2523M0802&USE_YN=Y&brandHotelList=H0010&_=1585116545558'
    pageString = requests.get(url).text
    jsonString = json.loads(pageString)
    entityList = jsonString['hotel_list']
    result = []
    for info in entityList:
        name = info['HOTEL_BRAND_NM']
        branch = info['BRANCH_NAME']
        addr = info['BRANCH_ADDRESS']
        tell = info['BRANCH_TEL']
        xcord = info['LONGITUDE']
        ycord = info['LATITUDE']
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()