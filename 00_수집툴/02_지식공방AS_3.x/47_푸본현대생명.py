import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('47_푸본현대생명.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")


    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.3,0.6))

    store_list = getStoreInfo2()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo():
    url ="https://www.fubonhyundai.com/menu/viewPage/cmmn/CUSI160100000000"
    pageString = requests.post(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    entityList = bsObj.find('tbody',{"id":"PAYMENT"})
    entityList = str(entityList).replace('<!--','').replace('-->','')
    entityList = bs4.BeautifulSoup(entityList,"html.parser")
    tr = entityList.find_all('tr')
    result = []
    for info in tr:
            name = '푸본현대생명'
            branch = info.find('td').text
            addr = str(info.select('td')[1]).replace('<td class="ta-left">','').replace('<td>','').replace('</td>','')
            tell = str(info.select('td')[3]).replace('<td class="ta-left">','').replace('<td>','').replace('</td>','')
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result


def getStoreInfo2():
    url ="https://www.fubonhyundai.com/menu/viewPage/cmmn/CUSI160100000000"
    pageString = requests.post(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    entityList = bsObj.find('tbody',{"id":"LOAN"})
    entityList = str(entityList).replace('<!--','').replace('-->','')
    entityList = bs4.BeautifulSoup(entityList,"html.parser")
    tr = entityList.find_all('tr')
    result = []
    for info in tr:
            name = '푸본현대생명'
            branch = info.find('td').text.replace('㈜','').replace(' ','')
            addr = str(info.select('td')[1]).replace('<td class="ta-left">','').replace('<td>','').replace('</td>','')
            tell = str(info.select('td')[3]).replace('<td class="ta-left">','').replace('<td>','').replace('</td>','')
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()