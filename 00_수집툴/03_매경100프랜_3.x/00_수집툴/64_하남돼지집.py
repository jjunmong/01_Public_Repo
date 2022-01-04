import sys
import time
import codecs
import requests
import random
import json
import bs4


def main():

    outfile = codecs.open('64_하남돼지집.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1

        time.sleep(random.uniform(0.3, 0.9))

def getStoreInfo(intpageNo):
    url = 'https://hanampig.co.kr/board/index.php'
    params = {
        'board': 'map_01',
        'sca': 'all',
        'type': 'list',
        'select': '',
        'search': '',
        # 'page': '1',
    }
    params['page']=intpageNo
    pageString = requests.get(url, params = params).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url , intpageNo)
    ul = bsObj.find('ul',{"class":"store_list"})
    li = ul.find_all('li')
    result = []
    for info in li:
        name = '하남돼지집'
        branch = info.find('p',{"class":"store_name ellipsis"}).text
        addr = info.find('p', {"class": "store_add ellipsis"}).text
        tell = info.find('p', {"class": "store_tel"}).text.replace(')','-')
        result.append({"name":name, "branch":branch,"addr":addr,"tell":tell})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
