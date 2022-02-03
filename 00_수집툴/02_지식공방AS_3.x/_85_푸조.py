import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('85_푸조.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|DEALER|ADDR|TELL|URL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['dealer'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s\n' % store['url'])

    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo():
    url = 'https://base.epeugeot.co.kr/home/dealers'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',}
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    table = bsObj.find('table',{"id":"list"})
    result = []
    tr = table.find_all('tr')
    for info in tr:
        try:
            name = '푸조'
            branch = info.find('td',{"class":"first"}).text
            dealer = info.select('td')[1].text.replace('(주)','')
            addr = info.select('td')[2].text
            tell = info.select('td')[3].text
            url = info.find('a')['href']
        except : pass
        else:
            result.append({'name':name,'branch':branch,'dealer':dealer,'addr':addr,'tell':tell,'url':url})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()