import sys
import requests
import bs4
import codecs
import time
import random
import json
def main():

    outfile = codecs.open('100_호치킨.txt', 'w', 'utf-8')
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

def getStoreInfo_url_list():
    url = 'http://hochicken.co.kr/map'
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    h3 = bsObj.find_all('h3',{"style":"margin-left:5px;"})
    result = []
    for info in h3:
        try:
            a = info.find('a')['href']
        except: pass
        else:
            result.append(a)
    return result

def getStoreInfo(url):
    full_url = 'http://hochicken.co.kr'+url
    pageString = requests.get(full_url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    print(full_url)
    result=[]
    name = '호치킨'
    branch = bsObj.find('h5').text.replace(' 매장정보 ','')
    infos = bsObj.find('p',{"class":"co_ddd"}).text
    infos = infos.split('|')
    addr = str(infos[0]).lstrip().rstrip()
    tell = str(infos[1]).lstrip().rstrip()
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()