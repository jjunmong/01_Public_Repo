import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('88_깐부치킨.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://kkanbu.co.kr/home/sub02.php?mid=10&where=&keyword=&p={}'.format(intPageNo)
    pageString = requests.get(url)
    print(intPageNo, url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '깐부치킨'
            branch = info.find('p',{"class":"t1"}).text
            addr = info.find('p',{"class":"t2"}).text
            tell = info.find('span',{"class":"tel"}).text
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()