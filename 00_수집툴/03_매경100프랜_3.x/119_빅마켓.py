import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('119_빅마켓.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo():
    url = 'http://company.lottemart.com/vc/info/branch.do?SITELOC=DK013'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '빅마켓'
            branch = info.find('h3').text.replace('빅마켓 ','')
            addr = str(info.select('span')[0]).replace('<span>','').replace('</span>','').replace('<br/>','').replace('\r','').replace('\n','').replace('\t','').lstrip().rstrip()
            tell = str(info.select('span')[1]).replace('<span>','').replace('</span>','').lstrip().rstrip()
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()