import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('89_노랑통닭.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        for store in storeList:
            if store['name'] == '매장찾기서비스' : pass
            else:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.norangtongdak.co.kr/store/store.html?p={}&'.format(intPageNo)
    pageString = requests.get(url)
    print(intPageNo, url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    div = bsObj.find_all('div')
    result = []
    for info in div:
        try:
            name = '노랑통닭'
            branch = info.find('p',{"class":"txt1"}).text.replace(' ','')
            if branch == '매장찾기서비스' : pass
            addr = info.find('li',{"class":"txt3"}).text
            tell = info.find('li',{"class":"txt2"}).text
            time = info.find('li',{"class":"txt4"}).text
            xcord = info.find('a')['data-longitude']
            ycord = info.find('a')['data-latitude']
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time,'xcord':xcord,'ycord':ycord})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()