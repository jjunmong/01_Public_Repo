import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('120_씨스페이스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList ==[] : break
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s\n' % store['addr'])
        page+=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'http://cspace.co.kr/bbs/board.php?bo_table=location&page={}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('tr')
    result = []
    for info in li:
        try:
            name = '씨스페이스'
            branch = str(info.select('a')[0]).replace('<a class="select_spot">','').replace('</a>','').lstrip().rstrip()
            addr = str(info.select('a')[1]).replace('<a class="select_spot">','').replace('</a>','').lstrip().rstrip()
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()