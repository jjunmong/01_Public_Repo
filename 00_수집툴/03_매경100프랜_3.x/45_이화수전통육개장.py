import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('45_이화수전통육개장.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    url = getUrlList()
    for info in url :
        store_list = getStoreInfo(info)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        time.sleep(random.uniform(0.9, 0.9))
    outfile.close()

def getUrl(pageNo):
    url = 'http://ihwasoo.com/bbs/board.php?bo_table=offshop&page={}'.format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    td = bsObj.find_all('td',{"class":"subject"})
    result = []
    for info in td:
        url = info.find('a')['href']
        result.append(url)
    return result

def getUrlList():
    result = []
    page = 1
    while True:
        result = result + getUrl(page)
        if getUrl(page) == [] : break
        page += 1
        if page == 30:
            break
    results = list(set(result))
    return results

def getStoreInfo(url):
    url = url
    print(url)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    result = []
    name = '이화수전통육개장'
    branch = bsObj.find('p',{"class":"p1"}).text
    addr = bsObj.find('p',{"class":"p2"}).text
    tell = bsObj.select('div.bov_info > div.bov_list > ul > li:nth-child(1)')
    tell = str(tell).replace('[<li><span>전화번호</span>','').replace('</li>]','')
    time = bsObj.select('div.bov_info > div.bov_list > ul > li:nth-child(5)')
    time = str(time).replace('[<li><span>영업시간</span>','').replace('</li>]','')
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

