import requests
import codecs
import sys
import time
import codecs
import random
import json
import bs4

def main():
    outfile = codecs.open('06_김영희강남동태찜.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
    outfile.close()

def getStoreInfo(pageNo):
    url = "http://www.e-happyfood.com/store.php?page={}&region_id=&name=#store-search".format(pageNo)
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.1771324665.1604566507; _gid=GA1.2.1731080075.1604566507',
        'Host': 'www.e-happyfood.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.e-happyfood.com/store.php?page=2&region_id=&name=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    }
    pageString = requests.get(url, headers = header).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    div = bsObj.find_all('tr')
    data = []
    for info in div :
        try:
            name = "김영희강남동태찜"
            branch = str(info.select('td')[0]).replace('<td>','').replace('</td>','')
            addr = str(info.select('td')[1]).replace('<td>','').replace('</td>','')
            tell = str(info.select('td')[2]).replace('<td>','').replace('</td>','')
        except:
            pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()