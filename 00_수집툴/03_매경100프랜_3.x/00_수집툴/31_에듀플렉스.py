import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('31_에듀플렉스.txt', 'w', 'utf-8')
    outfile.write("NAME|ADDR|OPENDATE|HOMEPAGE|FAX|TELL\n")

    page = getStoreIdx_all()
    print(page)
    for num in page:
        store_list = getStoreInfo(num)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['addr'])

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(idx):
    url = 'http://www.eduplex.net/store/store_posi?lat=&lng=&store_idx={}'.format(idx)
    pageData = requests.get(url)
    print(url)
    pageData.encoding = 'utf-8'
    text = pageData.text
    pageString = bs4.BeautifulSoup(text, "html.parser")
    data=[]
    name = "에듀플렉스"
    branch = pageString.find('span',{"class":"name"}).text.rstrip().lstrip()
    tell = pageString.find('span',{"class":"f_right tel"}).text.rstrip().lstrip()
    addr = pageString.find('p',{"class":"mt5"}).text.rstrip().lstrip()
    data.append({"name":name,"branch":branch,"tell":tell,"addr":addr})
    return data

def getStoreIdx(intPageNo):
    url = 'http://www.eduplex.net/store/store_list_get'
    params = {
        # 'page_num': '2',
        'add': '',
        'store_name': '',
        'region_cd': '',
        'city_cd': ''
    }
    params['page_num'] = intPageNo
    pageData = requests.post(url, data = params)
    print(url,params)
    pageData.encoding = 'utf-8'
    text = pageData.text
    pageString = bs4.BeautifulSoup(text, "html.parser")
    data = []
    tr = pageString.find_all('tr')
    for infos in tr:
        url = infos.select('a')
        url = str(url).split("'")
        url1= str(url[31:32])
        url2 = url1.replace('[','').replace(']','').replace("'","")
        if url2 == '' : pass
        else :
            data.append(url2)
    return data

def getStoreIdx_all():
    result = []
    page = 1
    while True:
        result = result + getStoreIdx(page)
        if getStoreIdx(page) == [] : break
        page += 1
        if page == 99: break
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()