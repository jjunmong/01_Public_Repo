import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('74_유가네닭갈비.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.yoogane.co.kr/store/find_a_store.html?page={}&lcode=&mcode=&keyword=&code=&service_chk1=&service_chk2=&service_chk3=&service_chk4=&service_chk5=&service_chk6=&service_chk7=&service_chk8='.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.3.550578305.1593663904; PHPSESSID=1hj5cm55ou96sbdu9a126a8bq7; _gid=GA1.3.1551316337.1606896230; _gat_gtag_UA_104069541_1=1',
        'Host': 'www.yoogane.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://www.yoogane.co.kr/store/find_a_store.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,'html.parser')
    tr = bsObj.find_all('div',{"class":"store-list-inner"})
    result = []
    for info in tr:
        try:
            name = '유가네닭갈비'
            branch = info.find('p').text.replace('\n','').lstrip().rstrip()
            addr = info.find('li').text.replace('주소 :  ','')
            tell = info.find('a').text.replace('TEL :  ','')
            time = info.select('li')[2]
            time = str(time).replace('<li><span class="l-tt">영업시간 : </span> ','').replace('</li>','')
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()