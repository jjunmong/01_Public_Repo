import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('93_멕시카나.txt', 'w', 'utf-8')
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

def getStoreInfo():
    url = 'https://www.mexicana.co.kr:50010/company/find_store.asp'
    pageString = requests.get(url)
    print(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '멕시카나'
            branch = info.find('p',{"class":"loc_tit"}).text
            addr = info.find('p', {"class": "loc_lo"}).text
            tell = info.find('p', {"class": "loc_call"}).text
            xcord = info.find('p', {"class": "loc_lo"})['data-coordy']
            ycord = info.find('p', {"class": "loc_lo"})['data-coordx']
        except: pass
        else:
            result.append({'name':name, 'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()