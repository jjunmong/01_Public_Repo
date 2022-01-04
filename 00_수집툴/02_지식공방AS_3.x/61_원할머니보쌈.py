import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('61_원할머니보쌈.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo():
    url = 'https://wonandone.co.kr/bossam/store.asp'
    data = {
        'KeyBrand': 'b',
        'KeyOrder': 'S',
        'KeyAddr1': '',
        'KeyAddr2': '',
        'KeyWord': '점',
    }
    response = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '원할머니보쌈'
            branch = info.find('strong',{"class":"tit"}).text.replace(' ','')
            addr = info.find('p',{"class":"addr"}).text
            tell = info.find('p',{"class":"tel"}).text
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