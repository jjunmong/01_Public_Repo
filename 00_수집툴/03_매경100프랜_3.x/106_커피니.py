import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('106_커피니.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.coffeenie.co.kr/techboard/bbs/board.php?bo_table=stores&gugun=&wr_2=&wr_6=&wr_30=&wr_29=&page={}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '커피니'
            branch = str(info.select('td')[1]).replace('<td align="center" valign="middle">','').replace('</td>','')
            addr = info.find('a').text
            tell = str(info.select('td')[4]).replace('<td align="center" valign="middle">','').replace('</td>','')
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()