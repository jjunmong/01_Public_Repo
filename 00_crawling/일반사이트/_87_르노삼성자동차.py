import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('86_재규어.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|DEALER|CAT|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['dealer'])
        outfile.write(u'%s|' % store['cat'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo():
    url = 'https://local.jaguarkorea.co.kr:8443/dealer/w/dealer.asp'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',}
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    tr = bsObj.find_all('tr')
    for info in tr:
        try:
            name = '재규어'
            branch = info.select('td')[0].text
            dealer = info.select('td')[1].text
            cat = info.select('td')[2].text
            addr = info.select('td')[3].text.replace('<br>','').replace('\r','').replace('\n','').replace('  ','')
            tell = info.select('td')[4].text.strip()
        except : pass
        else:
            result.append({'name':name,'branch':branch,'dealer':dealer,'cat':cat,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()