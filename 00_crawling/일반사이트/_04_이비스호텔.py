import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('04_이비스호텔.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo_1()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    store_list = getStoreInfo_2()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    store_list = getStoreInfo_3()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    outfile.close()

def getStoreInfo_1():
    url = 'https://www.ambatel.com/ko/hotel/selBrandHotelList.do?page=1&selBrandCode=&PROD_TYPE=M0801%2523%2523%2523M0802&USE_YN=Y&brandHotelList=H0020&_=1585112484879'
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


def getStoreInfo_2():
    url = 'https://www.ambatel.com/ko/hotel/selBrandHotelList.do?page=1&selBrandCode=&PROD_TYPE=M0801%2523%2523%2523M0802&USE_YN=Y&brandHotelList=H0060&_=1585116293185'
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


def getStoreInfo_3():
    url = 'https://www.ambatel.com/ko/hotel/selBrandHotelList.do?page=1&selBrandCode=&PROD_TYPE=M0801%2523%2523%2523M0802&USE_YN=Y&brandHotelList=H0050&_=1585116293186'
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