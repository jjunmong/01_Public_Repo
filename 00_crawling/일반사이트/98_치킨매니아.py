import sys
import requests
import bs4
import codecs
import time
import random
import json
def main():

    outfile = codecs.open('98_치킨매니아.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True :
        storeList = getStoreInfo(page)
        if getStoreInfo(page) == [] : break
        for store in storeList:
            if store['branch'].startswith('매장안내') == True: pass
            else :
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])
        page +=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.cknia.com/store/list.html?page={}&plist=&find_field=&find_word=&find_state=&find_ordby=&conf=&find_mode='.format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    li = bsObj.find_all('li')
    print(intPageNo, url)
    result = []
    for info in li:
        try:
            name = '치킨매니아'
            branch = info.find('p',{"class":"tit"}).text
            branch = branch.split(' ')[1]
            addr = str(info.select('span')[0]).replace('<span>주소 : ','').replace('</span>','')
            tell = str(info.select('span')[1]).replace('<span>전화번호 : ','').replace('</span>','')
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()