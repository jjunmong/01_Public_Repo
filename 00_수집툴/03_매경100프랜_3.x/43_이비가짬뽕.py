import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('43_이비가짬뽕.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")


    for store in range(0, 300, 15):
        store_list = getInfo(store)
        print(store, store_list)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getInfo(pageNo):
    url = 'https://www.ebiga.co.kr/main/inc/_ajax_more_content.php?key=store&start={}&keyword=&opt=&total_count='.format(pageNo)
    print(url, pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        name = '이비가짬뽕'
        branch = info.find('p',{"class":"fs22"}).text
        addr = info.select('p')[1]
        addr = str(addr).replace('<p class="fs16">','').replace('</p>','')
        tell = info.select('p')[2]
        tell = str(tell).replace('<p class="fs16">', '').replace('</p>', '')
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()


