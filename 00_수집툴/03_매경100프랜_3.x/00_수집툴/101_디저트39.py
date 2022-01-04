import sys
import requests
import bs4
import codecs
import time
import random
import json
def main():

    outfile = codecs.open('101_디저트39.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    url_list = getStoreInfo_url_list()
    for url in url_list:
        storeList = getStoreInfo(url)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo_url(intPageNo):
    url = 'http://www.dessert39.com/store/store.php'
    data = {
        'RetrieveFlag': '',
        # 'page': '2',
        'Txt_sido': '',
        'str_no': '',
        'Txt_key': 'all',
        'Txt_word': '',
        'txtRows': '10',
    }
    data['page']=intPageNo
    pageString = requests.post(url, data = data)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    ul = bsObj.find('ul',{"class":"findStore_list"})
    li = ul.find_all('li')
    result = []
    for info in li:
        try:
            a = info.find('a')['href']
        except: pass
        else:
            result.append(a)
    return result

def getStoreInfo_url_list():
    result = []
    page = 1
    while True :
        result = result + getStoreInfo_url(page)
        if getStoreInfo_url(page) == [] : break
        print(page)
        page +=1
        time.sleep(random.uniform(0.3, 0.9))
    return result

def getStoreInfo(url):
    full_url = 'http://www.dessert39.com/store/'+url
    pageString = requests.get(full_url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    print(full_url)
    result=[]
    name = '디저트39'
    branch = bsObj.find('div',{"class":"tit"}).text
    addr = bsObj.select('#store > div.store_view.clear > div.info > ul > li:nth-child(1)')
    addr = str(addr).replace('[<li>주소 : ','').replace('</li>]','')
    tell = bsObj.select('#store > div.store_view.clear > div.info > ul > li:nth-child(2)')
    tell = str(tell).replace('[<li>전화번호 : ','').replace('</li>]','')
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()