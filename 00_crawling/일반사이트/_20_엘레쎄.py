import codecs
import time
import requests
import sys
import random
import json
import bs4

def main():

    outfile = codecs.open('20_엘레쎄.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|INFO\n")

    store_list = getStoreNum2()
    result = []
    for ss in store_list:
        result = result+ getStores(ss)

    for store in result:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s' % store['branch'])
        outfile.write(u'%s\n' % store['addr'])

    time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreNum(intpageNo):
    url = "http://ellesse.co.kr/board/store-info/12/?board_no=12&page={}".format(intpageNo)
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        openurl = requests.get(url, headers = headers)
    except :
        print('Error calling the API')
        return  None
    response = openurl.content
    print(url)
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    tbody = bsObj.find('tbody')
    td = tbody.find_all('td')
    store_list = []
    for list in td:
        try:
            a = list.find('a')['href']
            b = a[23:27]
        except :
            pass
        else:
            store_list.append(b)
    return store_list

def getStoreNum2():
    result = []
    for ss in range(1,5):
        result = result + getStoreNum(ss)
    return  result

def getStores(storeList):
    url = "http://ellesse.co.kr/article/store-info/12/{}/".format(storeList)
    headers = {'User-Agent': 'Mozilla/5.0'}
    try :
        urlopen = requests.get(url,headers = headers)
    except :
        print('Error calling the API')
        return  None
    response = urlopen.content
    print(url)
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    div = bsObj.find_all('div',{"style":"padding: 13px; border: 1px solid rgb(204, 204, 204); border-image: none; color: rgb(85, 85, 85); line-height: 20px; font-size: 14px; margin-bottom: 20px; display: block;"})
    data_all = []
    for list in div:
        try:
            name = "엘레쎄"
            branch = list.find('strong').text.rstrip().lstrip().replace(' ','')
            addr2 = list.find('span').text.replace('\n','|').rstrip('').lstrip().replace('						','')
            addr2 = addr2.splitlines()
            addr = "".join(addr2)
        except:
            pass
        else:
            data_all.append({"name":name,"branch":branch,"addr":addr})
    return data_all

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()