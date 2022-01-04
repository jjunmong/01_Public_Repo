import requests
import codecs
import sys
import time
import codecs
import random
import json
import bs4

def main():
    outfile = codecs.open('02_GoldenNail.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|\n' % store['tell'])
        page += 1
    outfile.close()

def getStoreInfo(pageNo):
    url = "http://www.golden-nail.co.kr/index.php?mid=store&page={}".format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    store_list = bsObj.findAll("tr")
    data = []
    for list in store_list:
        try :
            name = "골든네일"
            branch = list.find("td", {"class": "cell_title"}).text.replace(" ","").rstrip().lstrip().upper()
            addr = list.find("td", {"class": "cell_address"}).text.rstrip().lstrip().upper()
            tell = list.find("td", {"class": "cell_tel"}).text.rstrip().lstrip().upper()
        except :
            pass
        else :
            data.append({"name":name,"branch": branch,"addr": addr,"tell": tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()