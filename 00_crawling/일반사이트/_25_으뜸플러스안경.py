import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('25_으뜸플러스안경.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    url_list = getStore_list_all()
    for url in url_list:
        store_list = getStoreInfo(url)
        for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['tell'])
                outfile.write(u'%s\n' % store['time'])
    outfile.close()

def getStore_list(intPageNo):
    url = "http://www.top-plus.co.kr/bbs/board.php"
    data = {
        'tbl': 'store',
        'category': '',
        'findType': 'title',
        'findWord': '',
        'sort1': '',
        'sort2': '',
        'it_id': '',
        'shop_flag': '',
        'mobile_flag': '',
        'sh': '',
        # 'page': '12',
    }
    data['page'] = intPageNo
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, intPageNo)
    ul = bsObj.find('ul',{"class":"loca_list"})
    a= ul.find_all('a')
    result = []
    for info in a:
        href = info['href']
        result.append(href)
    results = list(set(result))
    return results

def getStore_list_all():
    result = []
    page = 1
    while True:
        result = result + getStore_list(page)
        if getStore_list(page) ==[] : break
        page +=1
    return result

def getStoreInfo(list_url):
    url = 'http://www.top-plus.co.kr'+list_url
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    print(url)
    result =[]
    div = bsObj.find('div',{"class":"lvtxt"})
    names = div.find('h3').text
    names= names.split(' ')
    name = '으뜸플러스안경'
    branch = names[1]
    addr = bsObj.select('div > div > div > div.view_top.clfix > div.lvtxt > ul > li:nth-child(2) > p')
    addr = str(addr).replace('[<p>','').replace('</p>]','')
    tell = bsObj.select('div > div > div > div.view_top.clfix > div.lvtxt > ul > li:nth-child(3) > p')
    tell = str(tell).replace('[<p>','').replace('</p>]','')
    time = bsObj.select('div > div > div > div.view_top.clfix > div.lvtxt > ul > li:nth-child(1) > p')
    time = str(time).replace('[<p>','').replace('</p>]','')
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
