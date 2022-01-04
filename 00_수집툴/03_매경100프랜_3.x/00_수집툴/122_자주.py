import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('122_JAJU.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page +=1
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')
def getStoreInfo(inPageNo):
    url = 'http://www.sivillage.com/cst/cstStoreTbl.siv?page_idx={}&&erp_brnd_cd=J1&_=1598412988787'.format(inPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    dl = bsObj.find_all('dl')
    result = []
    for info in dl:
        try:
            name = 'JAJU'
            branch = info.find('dt').text.replace('JAJU ','').replace('E-MART','이마트').replace(' ','')
            addr = info.find('p',{"class":"addr"}).text
            tell = info.find('p',{"class":"tel"}).text
            if tell == '-' : tell = ''
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()