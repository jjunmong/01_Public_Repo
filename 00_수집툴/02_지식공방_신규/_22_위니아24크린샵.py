import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('22_위니아24크린샵.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list ==[] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s\n' % store['addr'])

        page +=1

    outfile.close()
def getStoreInfo(intPageNo):
    url = "http://winia24cleanshop.com/frt/information/shopFind.do"
    params = {
        # 'page': '1',
        'recordSize': '5',
        'sid': '',
        'searchText1': '',
    }
    params['page'] = intPageNo
    pageString = requests.get(url, params = params).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, intPageNo)
    result = []
    try:
        ul = bsObj.find('ul',{"class":"list-con"})
        li = ul.find_all('li')
    except : pass
    else:
        for info in li:
            try:
                name = '위니아24크린샵'
                branch = info.find('strong').text.replace(' ','')
                addr = info.find('p').text
            except : pass
            else:
                result.append({"name":name,"branch":branch,"addr":addr})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()