import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('52_가르텐비어.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if getStoreInfo(page) == []: break
        print(page)
        for store in store_list:
            if store['name'].startswith('가르텐') == False : pass
            else:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])
        page+=1
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://beafriend.co.kr/sub05_1?page={}'.format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result =[]
    for info in tr:
        try:
            name = info.find('b').text
            branch = info.find('a').text
            addr = info.find('td',{"class":"td_location"}).text
            tell = info.find('td',{"class":"td_name sv_use"}).text
        except: pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()