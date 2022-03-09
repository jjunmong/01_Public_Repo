import sys
import requests
import bs4
import codecs
import time
import random
import json
def main():

    outfile = codecs.open('99_푸라닭치킨.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    url_list = getStoreInfo_url_list()
    for url in url_list:
        storeList = getStoreInfo(url)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
def getStoreInfo_url(intPageNo):
    url = 'http://puradak.com/index.php?CurrentPage={}&module=Shop&action=SiteShop&sMode=SELECT_FORM&sSearchField=&sSearchValue=&iShopNo=1&sSearchValue1=&sSearchValue2=&sSearchValue3=&iZipCd=&sDiQu=&sGuGun=&z='.format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    print(intPageNo)
    result = []
    for info in tr:
        try:
            a = info.find('a')['href']
        except: pass
        else:
            result.append(a)
    return result

def getStoreInfo_url_list():
    result = []
    page = 1
    while True :
        result = result + getStoreInfo_url(page)
        if getStoreInfo_url(page) == [] : break
        page +=1
        time.sleep(random.uniform(0.3, 0.9))
    return result

def getStoreInfo(url):
    Full_url = 'http://puradak.com/index.php'+url
    pageString = requests.get(Full_url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find('tbody')
    print(url)
    result = []
    name = '푸라닭치킨'
    branch = str(tbody.select('td')[0]).replace('<td>','').replace('</td>','')
    addr =str(tbody.select('td')[1]).replace('<td>','').replace('</td>','')
    tell =str(tbody.select('td')[2]).replace('<td>','').replace('</td>','')
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()