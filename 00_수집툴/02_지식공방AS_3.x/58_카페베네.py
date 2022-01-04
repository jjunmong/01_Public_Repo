import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('58_카페베네.txt', 'w', 'utf-8')
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
    url = 'http://caffebene.com/store/local.html?ss=%EC%A0%90'
    response = requests.get(url).text
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    ul_id = bsObj.find('ul',{"id":"datalist"})
    li = ul_id.find_all('li')
    result = []
    for info in li:
        name = '카페베네'
        branch = info.find('h4').text
        addr = info.find('p',{"class":"addr"}).text
        tell = info.find('p',{"class":"tel"}).text
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()