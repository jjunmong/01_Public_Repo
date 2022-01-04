import sys
import time
import codecs
import requests
import random
import json
import codecs
import bs4
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():

    outfile = codecs.open('03_벤츠트럭.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['time'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo():
    url = 'https://roadefficiency.co.kr/service/'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        name = '벤츠'
        gubun = str(info.select('td')[2]).replace('<td>','').replace('</td>','')
        if gubun.endswith('본부') == True : pass
        else:
            branch = info.select('td')[4]
            branch = str(branch).replace(' ','').replace('<td>','').replace('</td>','')
            if branch.startswith('개소') == True: pass
            else:
                addr = info.select('td')[5]
                addr = str(addr).replace('<td>','').replace('</td>','')
                tell = info.select('td')[7]
                tell = str(tell).replace('<td>', '').replace('</td>', '')
                time = info.select('td')[6]
                time = str(time).replace('<td>', '').replace('</td>', '').replace('</br>','')
                xcord = info.select('td')[11]
                xcord = str(xcord).replace('<td>', '').replace('</td>', '')
                ycord = info.select('td')[10]
                ycord = str(ycord).replace('<td>', '').replace('</td>', '')
                result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
