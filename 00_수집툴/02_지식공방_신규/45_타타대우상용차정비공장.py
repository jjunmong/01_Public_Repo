import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('45_타다대우상용차정비공장.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True :
        store_list = getStoreInfo_svc(page)
        if store_list == []: break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

    outfile = codecs.open('45_타다대우상용차대리점.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True :
        store_list = getStoreInfo_dealer(page)
        if store_list == []: break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStoreInfo_dealer(intPageNo):
    url = 'http://www.tata-daewoo.com/ver7/purchase/sales_guide.php?page={}&code=01&sido=&gugun=&searchkw='.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.206477546.1591341638; _gid=GA1.2.1743987058.1591341638',
        'Host': 'www.tata-daewoo.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.tata-daewoo.com/ver7/purchase/sales_guide.php?page=2&code=02&sido=&gugun=&searchkw=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    print(url, intPageNo)
    tbody = bsObj.find('tbody')
    result = []
    try:
        tr = tbody.find_all('tr')
    except: pass
    else:
        for info in tr:
            name = '타타대우판매대리점'
            branch = info.find('a').text.replace('(주)','').replace('(유)','').replace('(합)','').replace(' ','')
            addr = info.find('td',{"class":"address"}).text
            tell = info.select('td')[2]
            tell = str(tell).replace('<td>','').replace('</td>','').lstrip().rstrip()
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
        return result

def getStoreInfo_svc(intPageNo):
    url = 'http://www.tata-daewoo.com/ver7/purchase/sales_guide.php?page={}&code=02&sido=&gugun=&searchkw='.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.206477546.1591341638; _gid=GA1.2.1743987058.1591341638',
        'Host': 'www.tata-daewoo.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.tata-daewoo.com/ver7/purchase/sales_guide.php?page=2&code=02&sido=&gugun=&searchkw=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    print(url, intPageNo)
    tbody = bsObj.find('tbody')
    result = []
    try:
        tr = tbody.find_all('tr')
    except: pass
    else:
        for info in tr:
            name = '타타대우정비공장'
            branch = info.find('a').text.replace('(주)','').replace('(유)','').replace('(합)','').replace(' ','')
            addr = info.find('td',{"class":"address"}).text
            tell = info.select('td')[2]
            tell = str(tell).replace('<td>','').replace('</td>','').lstrip().rstrip()
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
        return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

