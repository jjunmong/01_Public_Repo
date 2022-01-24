import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('28_AIA생명.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    time.sleep(random.uniform(0.3,0.6))
    print('수집완료')
    outfile.close()

def getStoreInfo():
    url = 'https://www.aia.co.kr/ko/help-support/find-us/find-office.html'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    table = bsObj.find('table',{"class":"responsive"})
    tr = table.find_all('tr')
    result =[]
    for info in tr:
        try:
            name = 'AIA생명'
            branch = info.select('td')[0]
            branch = str(branch).replace('<td><b>','').replace('</b></td>','')+'점'
            addr = info.select('td')[1]
            addr = str(addr).replace('<td>', '').replace(' </td>', '').lstrip().rstrip()
            tell = info.select('td')[2]
            tell = str(tell).replace('<td>', '').replace('</td>', '').lstrip().rstrip()
        except: pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()