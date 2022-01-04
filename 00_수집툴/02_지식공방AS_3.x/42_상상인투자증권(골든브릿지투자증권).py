import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('42_상상인투자증권.txt', 'w', 'utf-8')
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
    url = 'http://www.sangsanginib.com/html/foot_pop/foot_pop04.html'
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '상상인투자증권'
            branch = info.find('a').text
            addr = str(info.select('td')[2]).replace('<td class="con">','').replace('</td>','')
            tell = str(info.select('td')[1]).replace('<td class="con">','').replace('</td>','').replace('(','').replace(')','-')
        except:
            pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()