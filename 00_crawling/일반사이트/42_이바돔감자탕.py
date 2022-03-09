import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('42_이바돔감자탕.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getInfo(page)
        if storeList == []: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

        page += 1

        if page == 30: break
        # elif len(storeList) < 15: break

        time.sleep(random.uniform(0.3, 0.9))

def getInfo(pageNo):
    url = 'https://www.ebadom.com/board/index.php?board=map_01&sca=all&type=list&page={}'.format(pageNo)
    print(url , pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li',{"class":"store_li"})
    result =[]
    for info in li:
        name = "이바돔감자탕"
        branch = info.find('p',{"class":"store_tit"}).text
        addr = info.find('span',{"class":"ellipsis"}).text
        tell = info.find('p',{"class":"store_txt m_t20"}).text.replace('전화 ','').replace(') ','-')
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
