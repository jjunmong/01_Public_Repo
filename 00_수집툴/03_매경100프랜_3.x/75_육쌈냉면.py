import sys
import requests
import bs4
import codecs
import time
import random
import os

def main():

    outfile = codecs.open('75_육쌈냉면2.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    storeList = getStoreInfo_all()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

    lines_seen = set()  # holds lines already seen
    outfile = codecs.open('75_육쌈냉면.txt', 'w', 'utf-8')
    for line in codecs.open('75_육쌈냉면2.txt', 'r', 'utf-8'):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

    os.remove(r'C:\00_업무\00_개발업무\03_매경100프랜_3.x\00_수집툴\75_육쌈냉면2.txt')

def getStoreInfo(intPageNo):
    url = 'http://www.yookssam.com/sub/sub04_03.php?boardid=store&sk=&sw=&category=&etc_1=&etc_2=&offset={}'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=eb81e939c1989213beaa53558eff7413; websight_log_count=1',
        'Host': 'www.yookssam.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.yookssam.com/sub/sub04_03.php?boardid=store&sk=&sw=&category=&etc_1=&etc_2=&offset=20',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    print(url, intPageNo)
    ul = bsObj.find('tbody')
    tr = ul.find_all('tr')
    result = []
    for info in tr:
        name = '육쌈냉면'
        branch = info.find('td',{"class":"tt"}).text
        addr = info.find('td',{"class":"addr"}).text
        tell = str(info.select('td')[2]).replace('<td>','').replace('</td>','')
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def getStoreInfo_all():
    result = []
    page = 0
    while True:
        result =result+ getStoreInfo(page)
        page +=10
        if page == 150: break
        time.sleep(random.uniform(0.3, 0.9))
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()