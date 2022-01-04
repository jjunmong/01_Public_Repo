import requests
import codecs
import sys
import time
import codecs
import random
import json
import bs4

def main():
    outfile = codecs.open('07_꼬지사께.txt', 'w', 'utf-8')
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
            outfile.write(u'%s\n' % store['tell'])
        page += 1
    outfile.close()


def getStoreInfo(pageNo):
    url = "http://www.kkojisakke.com/new/board/index.php?board=map_01&sca=all&type=list&select=&search=&page={}&now_date=oIj6T".format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    tbody = bsObj.find("ul",{"class":"storeList"})
    data = []
    for tr in tbody :
        try:
            name = "꼬지사께"
            branch = tr.find("p").text.replace(" ","").rstrip().lstrip().upper()
            addr = tr.select("dd")[0].text.replace("\xa0","").rstrip().lstrip().upper()
            tell = tr.select("dd")[1].text.replace("\xa0","").rstrip().lstrip().upper().replace(")","-")
        except TypeError :
            pass
        except AttributeError :
            pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()