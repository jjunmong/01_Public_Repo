import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('81_미스사이공.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True :
        storeList = getStoreInfo(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.miss420.net/bbs/board.php?bo_table=store&page={}'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,k-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=m6b7od3mdk7srcoo3t0k89usd2; 2a0d2363701f23f8a75028924a3af643=MTEyLjE2OS4zMy42Nw%3D%3D; ck_font_resize_rmv_class=; ck_font_resize_add_class=; _ga=GA1.2.731760360.1594797183; _gid=GA1.2.1676557038.1594797183; _gat=1; _gat_gtag_UA_121838701_1=1; e1192aefb64683cc97abb83c71057733=c3RvcmU%3D',
        'Host': 'www.miss420.net',
        'Pragma': 'no-cache',
        'Referer': 'http://www.miss420.net/bbs/board.php?bo_table=store&page=2',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    print(url, intPageNo)
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    result = []
    a = bsObj.find_all('a')
    for info in a:
        detail = info['href']
        if detail.startswith('javascript:setAddrMap(') == True :
            detail = str(detail).split("'")
            print(detail)
            name = '미스사이공'
            branch = str(detail[19]).replace(' ','')
            addr = detail[1]
            tell = detail[23]
            result.append({'name':name, 'branch':branch, 'addr':addr, 'tell':tell})
        else : pass
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()