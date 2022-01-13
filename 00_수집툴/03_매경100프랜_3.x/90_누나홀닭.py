import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('90_누나홀닭.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    url_list = getStoreInfo_url_list()
    for url in url_list:
        storeList = getStoreInfo(url)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
def getStoreInfo_url(intPageNo):
    url = 'http://www.noonaholdak.co.kr/intro/shop?page={}&location=&search_page='.format(intPageNo)
    pageString = requests.get(url)
    print(intPageNo, url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    ul = bsObj.find('ul',{"class":"shop_list"})
    li = ul.find_all('li')
    result = []
    for info in li:
        a = info.find('a')['href']
        result.append(a)
    return result

def getStoreInfo_url_list():
    result = []
    page = 1
    while True:
        result = result + getStoreInfo_url(page)
        if getStoreInfo_url(page) == [] : break
        page +=1
        time.sleep(random.uniform(0.3, 0.9))
    return result

def getStoreInfo(url_list):
    url = 'http://www.noonaholdak.co.kr/'+url_list
    pageString = requests.get(url)
    print(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    result = []
    name = '누나홀닭'
    branch = bsObj.select('#shop_detail > h3 > span:nth-child(2)')
    branch = str(branch).replace('[<span>','').replace('</span>]','')
    addr = bsObj.select('#shop_address > div:nth-child(1) > span')
    addr = str(addr).replace('\n','').replace('\t','').replace('\xa0','').replace('[<span>주 소  : ','').replace('</span>]','')
    tell = bsObj.select('#shop_address > div:nth-child(2) > span')
    tell = str(tell).replace('\n','').replace('\t','').replace('\xa0','').replace('[<span>전화번호 : ','').replace('</span>]','')
    cord = str(bsObj.select('script')).split('daum.maps.LatLng( ')[1]
    cord = str(cord).split(',')
    xcord = str(cord[1]).replace(')','').lstrip().rstrip()
    ycord = str(cord[0]).lstrip().rstrip()
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()