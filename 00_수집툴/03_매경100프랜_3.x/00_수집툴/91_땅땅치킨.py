import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('91_땅땅치킨.txt', 'w', 'utf-8')
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
    url = 'http://www.codd.co.kr/site/tt/sub02/sub02_02.html?page={}&keyword=&search=&area=&area2=&f_ar=&wifi=&card=&cafe=&smok=&orderby='.format(intPageNo)
    pageString = requests.get(url)
    print(intPageNo, url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    ul = bsObj.find('table',{"class":"me_search"})
    tr = ul.find_all('tr')
    result = []
    for info in tr:
        try:
            a = str(info.find('a')['href']).replace('./sub02_02','/sub02_02')
        except : pass
        else:
            result.append(a)
    return result

def getStoreInfo_url_list():
    result = []
    page = 1
    while True:
        result = result + getStoreInfo_url(page)
        if len(getStoreInfo_url(page)) < 10: break
        page +=1
        time.sleep(random.uniform(0.3, 0.9))
    return result

def getStoreInfo(url_list):
    url = 'http://www.codd.co.kr/site/tt/sub02/'+url_list
    pageString = requests.get(url)
    print(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    table = bsObj.find('table',{"class":"storeinfo"})
    result = []
    name = '땅땅치킨'
    try:
        branch = str(table.select('td')[1]).replace('<td>','').replace('</td>','').replace(' ','')
        addr = str(table.select('td')[9]).split('\n')[2]
        addr = str(addr).lstrip().rstrip().replace('                               ','').replace(' </td>','')
        tell = str(table.select('td')[5]).replace('<td>','').replace('</td>','').replace(' ','')
    except : pass
    else:
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()