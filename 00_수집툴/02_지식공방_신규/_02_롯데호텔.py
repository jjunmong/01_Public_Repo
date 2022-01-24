import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('02_롯데호텔.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getStoreInfo():
    url = 'https://www.lottehotel.com/global/ko/hotel-finder.html'
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    li = bsObj.find_all('li',{"class":"d596-hotel__item"})
    result =[]
    for info in li:
        try:
            name = '롯데호텔'
            branch = info.find('strong').text.replace('\n','').replace(' ','')
            addr = info.find('p',{"class":"d596-hotel__address"}).text.replace('\n','')
            tell = info.find('p',{"class":"d596-hotel__tel"}).text.replace(' ','').replace('+82-','0').replace('\n','').replace('전화걸기','')
        except: pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()