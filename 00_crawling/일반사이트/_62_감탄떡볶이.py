import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('62_감탄떡볶이.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 0
    while True:
        store_list = getStoreInfo(page)
        if len(store_list) < 15 :
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
        page+=15
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.gamtan.co.kr/main/store_list.php?page_idx=166&startPage={}&gubun=&add_code=&keyword='.format(intPageNo)
    response = requests.get(url).text
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '감탄떡볶이'
            branch = info.find('td',{"class":"store-name"}).text.replace('-','')
            addr = info.find('td',{"class":"left store-address"}).text
            tell = info.find('td',{"class":"store-tel"}).text
            if tell == [] : tell = ''
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