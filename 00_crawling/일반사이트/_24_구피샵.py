import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('24_구피샵.txt', 'w', 'utf-8')
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
    url = "http://www.gupishop.com/bbs/board.php?bo_table=shop&page={}".format(intPageNo)
    headers ={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=ds76ps2tjlgrvh479k6ogikqp0; e1192aefb64683cc97abb83c71057733=c2hvcA%3D%3D; 2a0d2363701f23f8a75028924a3af643=MTEyLjE2OS4zMy42Nw%3D%3D',
        'Host': 'www.gupishop.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.gupishop.com/bbs/board.php?bo_table=shop&page=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    pageString = requests.get(url, headers= headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    print(url, intPageNo)
    result = []
    for info in tr:
        try:
            name = '구피샵'
            branch = info.select('a')[0]
            branch = str(branch).split('>')
            branch = str(branch[1]).replace(' ','').replace('</a','')
            addr = info.select('a')[2]
            addr = str(addr).split('>')
            addr = str(addr[1]).replace('</a','')
            tell = info.select('a')[1]
            tell = str(tell).split('>')
            tell = str(tell[1]).replace('</a','')
            time = info.select('a')[3]
            time = str(time).split('>')
            time = str(time[1]).replace('</a','')

        except: pass
        else:
            if time == '<b': pass
            else:
                result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
