import sys
import time
import codecs
import requests
import random
import json
import bs4


def main():

    outfile = codecs.open('67_홍익돈까스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    storeList = StoreList_all()
    for store in storeList:
        store_list = getStoreInfo(store)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getRegion():
    url = 'https://hongikdonkatsu.com/find_shop'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find('div',{"class":"item-element"})
    div_all = div.find_all('div',{"class":"galleryWrapper image"})
    result = []
    for info in div_all:
        regionName = info.find('a')['href']
        result.append(regionName)
    return result

def getStoreList(regionName):
    url = 'https://hongikdonkatsu.com'+regionName
    pageString = requests.get(url).text
    print(url,regionName)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div_all = bsObj.find_all('div',{"class":"galleryWrapper image"})
    result = []
    for info in div_all:
        storeName = info.find('a')['href']
        result.append(storeName)
    return result

def StoreList_all():
    regionList = getRegion()
    result = []
    for region in regionList:
        result  = result + getStoreList(region)
    return result

def getStoreInfo(storeName):
    url = 'https://hongikdonkatsu.com'+storeName
    pageString = requests.get(url).text
    print(url, storeName)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = '홍익돈까스'
    infos = bsObj.find('div',{"class":"item-wrapper text-title"}).text
    infos = str(infos).split('.')
    branch = infos[0]
    branch = str(branch).replace('Add','').lstrip().rstrip()
    addr = infos[1]
    addr = str(addr).replace('\xa0', ' ').replace('Tel','').lstrip().rstrip()
    try:
        tell = infos[2]
    except:
        tell = ''
    tell = str(tell).lstrip().rstrip()
    result.append({"name":name, "branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()