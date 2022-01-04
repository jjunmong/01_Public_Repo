import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('49_청년다방.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == []: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

        page += 1

        if page == 70: break

        time.sleep(random.uniform(0.6, 0.9))

def getStoreInfo(pageNo):
    url = 'http://www.youngdabang.com/board/index.php'
    data= {
        'board': 'map_01',
        'sca': 'all',
        'type': 'list',
        'select': '',
        'search': '',
        # 'page': '2',
    }
    data['page'] = pageNo
    pageString = requests.get(url, params=data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, pageNo)
    li = bsObj.find_all('li',{"class":"store_li"})
    result = []
    for info in li:
        name = "청년다방"
        branch = info.find("p",{"class":"store_name new"}).text.replace('NEW','')
        addr = info.find("p",{"class":"store_addr ellipsis"}).text
        try:
            tell = info.find("p",{"class":"store_tel"}).text.replace(')','-')
        except :
            tell = ''
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
