import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('44_쌍용자동차부품대리점.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 2
    while True :
        store_list = getStoreInfo(page)
        if store_list == None : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1

        time.sleep(random.uniform(0.3, 0.9))

    store_list = getStoreInfo_ori()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://www.smotor.com/kr/service/network/comp/index,1,list,{}.html'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'WMONID=QJ7MzJROPs4; JSESSIONID=PaTR16hCSUEhswK0MkROr8bTJfLSi3UU9R9NzkZPOdeRAX1D42OwKDyDkDGjPFLy.was02_servlet_engine3',
        'Host': 'www.smotor.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.smotor.com/kr/service/network/comp/index.html',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
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
            name = '쌍용자동차부품대리점'
            branch = info.select('td')[1]
            branch = str(branch).replace('<td class="leftTxt">','').replace('</td>','').lstrip().rstrip()
            addr = info.select('td')[2]
            addr = str(addr).replace('<td class="leftTxt">','').replace('</td>','').replace('\xa0','').lstrip().rstrip()
            tell = info.select('td')[3]
            tell = str(tell).replace('<td>','').replace('</td>','').lstrip().rstrip()
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
        return result

def getStoreInfo_ori():
    url2 = 'https://www.smotor.com/kr/service/network/comp/index.html'
    headers2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'WMONID=QJ7MzJROPs4; JSESSIONID=PaTR16hCSUEhswK0MkROr8bTJfLSi3UU9R9NzkZPOdeRAX1D42OwKDyDkDGjPFLy.was02_servlet_engine3',
        'Host': 'www.smotor.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.smotor.com/kr/service/network/comp/index.html',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
    pageString2 = requests.get(url2, headers=headers2)
    bsObj2 = bs4.BeautifulSoup(pageString2.content, "html.parser")
    tbody2 = bsObj2.find('tbody')
    tr2 = tbody2.find_all('tr')
    result = []
    for info in tr2:
        name = '쌍용자동차부품대리점'
        branch = info.select('td')[1]
        branch = str(branch).replace('<td class="leftTxt">', '').replace('</td>', '').lstrip().rstrip()
        addr = info.select('td')[2]
        addr = str(addr).replace('<td class="leftTxt">', '').replace('</td>', '').replace('\xa0', '').lstrip().rstrip()
        tell = info.select('td')[3]
        tell = str(tell).replace('<td>', '').replace('</td>', '').lstrip().rstrip()
        result.append({"name": name, "branch": branch, "addr": addr, "tell": tell})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

