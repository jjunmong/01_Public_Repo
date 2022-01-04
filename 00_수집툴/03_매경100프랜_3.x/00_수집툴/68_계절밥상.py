import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('68_계절밥상.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|OLDADDR|NEWADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['oldaddr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intpageNo):
    url = 'https://www.seasonstable.co.kr:7017/store/list.asp?page={}'.format(intpageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ASPSESSIONIDAQQCADRD=LCGJNGGAGLGIPFDDJIHOCGDC; _ga=GA1.3.894471375.1593418613; _gid=GA1.3.1930060833.1593418613; _gat=1',
        'Host': 'www.seasonstable.co.kr:7017',
        'Pragma': 'no-cache',
        'Referer': 'https://www.seasonstable.co.kr:7017/store/list.asp',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,'html.parser')
    print(url, intpageNo)
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        name = '계절밥상'
        branch = info.find('span',{"class":"db"}).text.replace(' ','')
        oldaddr = info.select('p')[0]
        oldaddr = str(oldaddr).split('>')[2].replace('\xa0','').replace('</p','')
        newaddr = info.select('p')[1]
        newaddr = str(newaddr).split('>')[2].replace('\xa0','').replace('</p','')
        tell = info.find('td',{"class":"num"}).text
        result.append({"name":name,"branch":branch,"oldaddr":oldaddr,"newaddr":newaddr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()