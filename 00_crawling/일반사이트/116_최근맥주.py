import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('116_최군맥주.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")


    for page in range(1, getPageCount()):
        storeList = getStoreInfo(page)
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'http://www.choigoonbeer.com/04_introduce/intro01.php?page={}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '최군맥주'
            branch = str(info.select('td')[1]).split('>')[2].replace('</a','').replace(' ','')
            addr = info.find('td',{"class":"left"}).text
            tell = str(info.select('td')[3]).replace('<td>','').replace('</td>','')
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def getPageCount():
    url = 'http://www.choigoonbeer.com/04_introduce/intro01.php'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    count = bsObj.select('body > div.wrap > div.com_wrap > div.com_container > div.com_contents > div > div.intro01_08 > table > tbody > tr:nth-child(1) > td:nth-child(1)')
    count = str(count).replace('[<td>','').replace('</td>]','')
    count = int(count) / 10
    if type(count) is float : count = int(count +2)
    else: count = int(count + 1)
    return count

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()