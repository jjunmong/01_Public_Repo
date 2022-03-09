import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('125_드림디포.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo():
    url = 'https://www.dreamdepot.co.kr/shop/chain.php?ps_mode=search&ps_area1=&ps_area2=&ps_search='
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('li')
    result = []
    for info in tr:
        try:
            name = '드림디포'
            branch = info.find('span',{"class":"smb_name pointer"}).text
            addr = str(info.select('p')[1]).replace('<p>','').replace('</p>','').replace(' .','')
            tell = str(info.select('td')[1]).replace('<td>','').replace('</td>','')
            xcord = info.find('span',{"class":"sr-only smb_mapx"}).text
            ycord = info.find('span', {"class": "sr-only smb_mapy"}).text
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()