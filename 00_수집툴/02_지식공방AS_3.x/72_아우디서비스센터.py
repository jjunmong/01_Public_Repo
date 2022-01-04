import sys
import time
import requests
import random
import codecs
import bs4
import json

def main():

    outfile = codecs.open('72_아우디서비스센터.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    url_list = getStore_list()

    for url in url_list:
        store_list = getStoreInfo(url)
        print(url)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStore_list():
    url = 'https://www.audi.co.kr/kr/web/ko/service/service-center.20210406055130.headless.html'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    a = bsObj.find_all('a',{"class":"nm-layerLink nm-link nm-el-lk nm-el-lk-01 nm-at-lk-b nm-el-lk-ast"})
    result = []
    for info in a:
        link_lsit = info['href']
        link = str(link_lsit).split('/servicepopup/')[1].replace('.html','')
        result.append(link)
    return result

def getStoreInfo(url_list):
    url = 'https://www.audi.co.kr/kr/web/ko/service/service-center/servicepopup/{}.20210406055130.headless.html'.format(url_list)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = '아우디서비스센터'
    infos = bsObj.find('div',{"class":"audi-copy-m nm-content-paragraph__text"}).text
    infos = infos.split(':')
    print(infos)
    branch = bsObj.find('h3').text
    addr = str(infos[1]).replace('T e l ','').lstrip().rstrip()
    tell = str(infos[2]).replace('e-mail ','').replace('E-mail','').lstrip().rstrip()
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()