import requests
import codecs
import time
import sys
import random
import bs4


def main():

    outfile = codecs.open('33_오레시피.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    urls = getStoreUrlList()
    print(urls)
    for url in urls :
        for store in getStoreInfo(url):
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s\n' % store['branch'])

    outfile.close()

def getStoreUrl(intPageNo):
    url = 'http://orecipe.co.kr/board/index.php?board=map_01&sca=all&type=list&select=&search=&page={}&now_date=M1ij3'.format(intPageNo)
    pageData = requests.get(url)
    pageData.encoding = 'utf-8'
    text = pageData.text
    pageString = bs4.BeautifulSoup(text, "html.parser")
    storeList = pageString.find_all("div",{"class":"storeImg f_left"})
    data = []
    for urls in storeList:
        url = 'http://orecipe.co.kr/' + urls.find('a')['href']
        data.append(url)

    return data

def getStoreUrlList():
    result = []
    page = 1
    while True:
        result = result + getStoreUrl(page)
        if getStoreUrl(page) == [] : break
        page += 1
        if page == 99: break
    return result

def getStoreInfo(url):
    url = url
    pageData = requests.get(url)
    print(url)
    pageData.encoding = 'utf-8'
    text = pageData.text
    pageString = bs4.BeautifulSoup(text, "html.parser")
    data = []
    name = "오레시피"
    branch = pageString.find('table',{"class":"store_view_top"}).text.replace('\n','').replace("매장명","").replace("오레시피","")\
        .replace("도로명 주소","|").replace("전화번호","|").rstrip().lstrip().replace('   ','').replace('  ','')
    data.append({"name":name,"branch":branch})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()