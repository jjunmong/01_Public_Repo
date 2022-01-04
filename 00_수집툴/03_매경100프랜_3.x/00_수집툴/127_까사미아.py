import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('127_까사미아.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo():
    url = 'http://casamia.ssg.com/service/store.ssg'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li',{"class":"mncasamia_storelst_item"})
    result = []
    for info in li:
        try:
            name = '까사미아'
            branch = info.find('dt',{"class":"mncasamia_storelst_tit"}).text.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            addr = info.find('dd',{"class":"mncasamia_storelst_addr"}).text.replace('주소','').replace('\n','')
            tell = info.find('p',{"class":"mncasamia_storelst_intotx1"}).text
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()