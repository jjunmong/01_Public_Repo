import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('60_주커피.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if len(store_list) < 10 :
            for store in store_list:
                if store['branch'] == '' : pass
                else:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['branch'])
                    outfile.write(u'%s|' % store['addr'])
                    outfile.write(u'%s\n' % store['tell'])
            break
        print(page)
        for store in store_list:
            if store['branch'] == '' : pass
            else:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])
        page+=1
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://www.zoo-coffee.com:6503/store/store.asp?page={}&sCate=&sKeyword=&pidx=&tags=&cate=&ProductSort='.format(intPageNo)
    response = requests.get(url).text
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '주커피'
            branch = info.find('td',{"width":"125"}).text
            addr = info.find('td',{"width":"351"}).text
            tell = info.find('td',{"width":"140"}).text
        except:
            pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()