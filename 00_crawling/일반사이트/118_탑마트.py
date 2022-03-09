import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('118_탑마트.txt', 'w', 'utf-8')
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
        page+=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'http://www.seowon.com/store/search_store.do?pageNo={}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    infos = bsObj.find_all('div',{"class":"store_list margB20PX"})
    result = []
    for info in infos:
        try:
            name = '탑마트'
            branch = info.find('dt',{"class":"margB15PX"}).text.replace(' 인터넷전단 보기오시는 길\n','')
            addr = str(info.select('dd')[1]).replace('<dd>','').replace('</dd>','').lstrip().rstrip()
            tell = str(info.select('dd')[2]).replace('<dd>','').replace('</dd>','').lstrip().rstrip().replace(')','-')
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()