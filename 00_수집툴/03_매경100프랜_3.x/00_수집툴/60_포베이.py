import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('60_포베이.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if len(storeList) < 10 : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))


def getStoreInfo(page):
    url = 'http://www.phobay.com/Store/SearchStore.php'
    params = {
        'ptype': '',
        # 'page': '2',
        'code': 'Store',
    }
    params['page'] = page
    pageString = requests.get(url , params = params, )
    print(page , url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '포베이'
            branch = info.find('a').text.rstrip().lstrip()
            addr = info.find('td',{"align":"left"}).text.rstrip().lstrip()
            tell = info.find('td',{"width":"120"}).text.replace(') ','-').rstrip().lstrip()
        except :
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()