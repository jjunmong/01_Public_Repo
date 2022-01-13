import sys
import requests
import bs4
import codecs
import time
import random
import os

def main():

    outfile = codecs.open('76_자연별곡2.txt', 'w', 'utf-8')
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
    outfile = codecs.open('76_자연별곡.txt', 'w', 'utf-8')
    for line in codecs.open('76_자연별곡2.txt', 'r', 'utf-8'):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

    os.remove(r'C:\00_업무\00_개발업무\03_매경100프랜_3.x\00_수집툴\76_자연별곡2.txt')

def getStoreInfo(intPageNo):
    url = 'http://www.naturekitchen.co.kr/Store/StoreFind.aspx?CurrentPage={}&Area=&Search='.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=vczqnu55aaybiq453dv1bz55; __utma=191304757.1416617667.1593677178.1593677178.1593677178.1; __utmc=191304757; __utmz=191304757.1593677178.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=191304757.3.10.1593677178',
        'Host': 'www.naturekitchen.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://www.naturekitchen.co.kr/Store/StoreFind.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    print(url, intPageNo)
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '자연별곡'
            branch = info.find('td',{"class":"StoreName"}).text.replace(' ','')
            addr = str(info.select('td')[2]).split('\r')[1]
            addr = addr.replace('\n                                ','')
            tell = str(info.select('td')[3]).replace('<td>','').replace('</td>','')
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def getStoreInfo_all():
    result = []
    page = 1
    while True:
        result =result+ getStoreInfo(page)
        page +=1
        if page == 15: break
        time.sleep(random.uniform(0.3, 0.9))
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()