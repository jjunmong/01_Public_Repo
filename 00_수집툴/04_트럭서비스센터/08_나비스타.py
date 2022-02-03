import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('08_나비스타.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|CODE\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo():
    url = 'http://www.chjitrucks.com/bbs/board.php?bo_table=board_as'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr :
        try:
            name = '나비스타'
            branch = info.find('a').text.replace('\r','').replace('\n','').lstrip().rstrip()
            addr = info.find('td',{"class":"td_location"}).text
            tell = info.find('td',{"class":"td_name sv_use"}).text
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

