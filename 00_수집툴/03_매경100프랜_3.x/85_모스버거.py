import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('85_모스버거.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
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
    url = 'http://www.moskorea.kr/store/standard?area=&area2=&area2&text=&page={}'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=00a12879fd9130e64da1e22ca545e9bd; mos=mosip',
        'Host': 'www.moskorea.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://www.moskorea.kr/store/standard?area=&area2=&area2&text=&page=2',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    print(intPageNo)
    pageString = requests.get(url,headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find('table',{"class":"fran-tbl"})
    tr = div.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '모스버거'
            branch = info.select('td')[1]
            branch = str(branch).replace('<td>','').replace('</td>','').replace(' [스탠다드]','')
            addr = info.select('td')[2]
            addr = str(addr).replace('<td class="tal">','').replace('</td>','')
            tell = info.select('td')[3]
            tell = str(tell).replace('<td>','').replace('</td>','')
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()