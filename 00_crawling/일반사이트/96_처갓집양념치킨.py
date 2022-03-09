import sys
import requests
import bs4
import codecs
import time
import random
import json
def main():

    outfile = codecs.open('96_처갓집양념치킨.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True :
        storeList = getStoreInfo(page)
        if getStoreInfo(page) == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page +=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.cheogajip.co.kr/bbs/board.php?bo_table=store&page={}'.format(intPageNo)
    pageString = requests.get(url).text
    print(intPageNo, url)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '처갓집양념치킨'
            branch = str(info.select('td')[1]).replace('<td class="td_date">','').replace('</td>','')
            addr = info.find('td',{"class":"td_subject"}).text
            tell = str(info.select('td')[3]).replace('<td class="td_date">','').replace('</td>','')
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()