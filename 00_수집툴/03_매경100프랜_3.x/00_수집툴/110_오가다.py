import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('110_오가다.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        print(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page +=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
def getStoreInfo(intPageNo):
    url = 'http://ogada.co.kr/store/page/{}/'.format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '오가다'
            branch = str(info.select('a')[1]).split('>')[1].replace('</a','')
            addr = info.find('span',{"class":"address"}).text
            tell = info.find('a',{"class":"mobile_tel"}).text.replace('\n','').replace('\t','').replace('\xa0','')
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()