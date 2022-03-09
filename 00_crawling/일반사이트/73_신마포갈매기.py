import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('73_신마포갈매기.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://www.mapo92.com/board/index.php?board=map_01&sca=all&type=list&select=&search=&page={}'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=11b237e78d7104edb10db494454d2516; _pk_ref.190.076c=%5B%22%22%2C%22%22%2C1593591221%2C%22https%3A%2F%2Fwww.google.co.kr%2F%22%5D; _pk_id.190.076c=544dda24b7caf81a.1593591221.1.1593591224.1593591221.',
        'Host': 'www.mapo92.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.mapo92.com/board/index.php?board=map_01&sca=all',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    print(url, intPageNo)
    ul = bsObj.find('ul',{"class":"store_ul"})
    li = ul.find_all('li')
    result = []
    for info in li:
        try:
            name = '신마포갈매기'
            branch = info.find('p').text
            addr = info.find('span',{"class":"ellipsis"}).text
            tell = info.select('span')[1]
            tell = str(tell).replace(' ','').replace('<span>','').replace('</span>','')
            cord = info.find('script')
            cord = str(cord).split(':')
            xcord = str(cord[5]).replace("'","").replace('},\n\t\t\t\t\t\tscrollwheel','').replace(' ','')
            ycord = cord[4].replace("'","").replace(' ','').replace(',lng','')
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()