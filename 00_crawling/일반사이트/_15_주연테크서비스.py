import sys
import time
import codecs
import requests
import random
import json
import bs4

# sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시', '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주특별자치도']

def main():

    outfile = codecs.open('15_주연테크.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    outfile.close()

def getStoreInfo():
    url = 'https://www.jooyon.co.kr/center.php'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.select('tbody')[2]
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        name = '주연테크'
        branch = info.select('td')[2]
        branch = str(branch).replace('<td>','').replace('</td>','').lstrip().rstrip()
        addr = info.select('td')[4]
        addr = str(addr).replace('<td class="jy_hide">','').replace('</td>','')
        tell = info.select('td')[3]
        tell = str(tell).replace('<td>','').replace('</td>','')
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
