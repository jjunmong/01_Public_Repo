import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('61_포차어게인.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s\n' % store['time'])

    time.sleep(random.uniform(0.3, 0.9))

def getStoreInfo():
    url = 'http://www.pochaa.net/store/store02.php'
    pageString = requests.get(url)
    print(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    mapList = bsObj.find('div',{"class":"mapList"})
    tr = mapList.find_all('ul',{"class":"gaList"})
    result = []
    for info in tr:
        try:
            name = info.find('h1',{"class":"gaTxt_1"}).text.rstrip().lstrip().replace('포차어게인 ','포차어게인|').replace('포차고고 ','포차고고|')
            infos = info.find('p',{"class":"gaTxt_2"}).text.rstrip().lstrip().replace('\t','').replace('주소 : ','').replace('전화번호 : ','|').replace('영업시간 : ','|')
            infos = str(infos).split('|')
            addr = infos[0].rstrip().lstrip()
            tell = infos[1].rstrip().lstrip()
            time = infos[2].rstrip().lstrip()
        except:
            pass
        else:
            result.append({"name":name,"addr":addr,"tell":tell,"time":time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()