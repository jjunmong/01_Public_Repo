import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('23_훌리카훌리카.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list ==[] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])

        page +=1

    outfile.close()

def getStoreInfo(intPageNo):
    url = "http://www.holikaholika.co.kr/FrontStore/PointBBS/iBoardList.phtml?bbsid=pbbs_store&iCategory=0&_oSName=0&_oSSubject=0&_oSContents=0&_oSAddr=1&_oSearchText=%BC%AD%BF%EF&iPage={}".format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    print(url, intPageNo)
    ul = bsObj.find('ul',{"class":"ty_ul"})
    li = ul.find_all('li')
    result = []
    for info in li:
        try:
            name = '홀리카홀리카'
            branch = info.find('dt').text.replace(' ','')
            addr = info.find('span',{"class":"address"}).text.replace('주소 : ','')
            tell = info.find('em').text
            time = info.find('span',{"class":"time"}).text.replace('영업시간 : ','')
        except: pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
