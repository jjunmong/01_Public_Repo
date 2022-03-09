import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('18_영풍문고.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    url_list = getStoreList()
    for list in url_list:
        store_list = getStoreInfo(list)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])

    outfile.close()

def getStoreList():
    url = 'https://www.ypbooks.co.kr/m_store.yp'
    pageString = requests.get(url).text
    print(url)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('div',{"class":"store-list"})
    li = tbody.find_all('li')
    result = []
    for info in li:
        branch_info = info.find('a')['href']
        result.append(branch_info)
    return result

def getStoreInfo(branch_rul):
    url = 'https://www.ypbooks.co.kr/'+branch_rul
    pageString = requests.get(url).text
    print(url,branch_rul)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = '영풍문고'
    branch = bsObj.select('#container > section > header')
    branch = str(branch).replace('[<header class="s-tit">', '').replace('</header>]', '')
    addr = bsObj.select('#container > section > div > dl:nth-child(2) > dd > ul > li')
    addr = str(addr).replace('[','').replace(']','').replace('<li>','').replace('</li>','')
    tell = bsObj.select('#container > section > div > div > a:nth-child(1)')
    tell = str(tell).replace('[<a href="tel:','').replace('"><span><em class="btn_call">전화하기</em></span></a>]','')
    time = bsObj.select('#container > section > div > dl:nth-child(1) > dd > ul > li')
    time = str(time).replace('[','').replace(']','').replace('<li>','').replace('</li>','')
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
