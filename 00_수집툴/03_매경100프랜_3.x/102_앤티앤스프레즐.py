import sys
import requests
import bs4
import codecs
import time
import random
import json
def main():

    outfile = codecs.open('102_앤티앤스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True :
        storeList = getStoreInfo(page)
        if storeList == []  : break
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page +=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://auntieannes.co.kr/store-map/?nowPage={}&shop_wantAddr1_si=&shop_wantAddr1_gu=&search_name='.format(intPageNo)
    pageString = requests.post(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    div = bsObj.find('div',{"class":"st-wrap"})
    li = div.find_all('li')
    result = []
    for info in li:
        try:
            name = '앤티앤스'
            branch = info.find('h3').text
            branch = branch.replace(' ','')+'점'
            addr = info.find('address').text.lstrip().rstrip()
            tell = info.find('p',{"class":"tel-num"}).text.lstrip().rstrip()
            if tell == '-' : tell = ''
            time = info.find('p',{"class":"open-time"}).text.lstrip().rstrip()
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()