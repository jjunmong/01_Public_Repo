import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('08_토마토도시락.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list ==[] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page +=1

    outfile.close()

def getStoreInfo(pageNo):
    url = 'http://www.tomatodosirak.co.kr/board/index.php?board=map_01&sca=all&type=list&select=&search=&page={}'.format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, pageNo)
    ul = bsObj.find('ul',{"class":"store_ul"})
    li = ul.find_all('li')
    result = []
    for info in li :
        try:
            name = '토마토도시락'
            branch = info.find('p',{"class":"store_name"}).text.lstrip().rstrip()
            addr =  info.find('dd',{"class":"addr ellipsis"}).text.lstrip().rstrip()
            tell =  info.find('dd',{"class":"tel ellipsis"}).text.replace(')','-').lstrip().rstrip()
        except:
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()