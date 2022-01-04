import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('71_동대문엽기떡볶이.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    url_list = getStoreInfo_url_list()
    for url in url_list:
        storeList = getStoreInfo(url)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo_url(intPageNo):
    url = 'http://www.yupdduk.com/store/list?cpage={}&sido=&gugun=&stname='.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'logday=20200701; logdata=9010000000000%2C9050000000000%2C9020000000000%2C9040000000000%2C9050000000000%2C',
        'Host': 'www.yupdduk.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.yupdduk.com/store/list?cpage=41&sido=&gugun=&stname=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,'html.parser')
    print(url, intPageNo)
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            a = info['onclick']
            a = str(a).split(',')
            a1 = a[0].replace("'","").replace('bodview(','')
            a2 = a[1] .replace("'","")
            a3 = a[2].replace("'","")
            a = 'http://www.yupdduk.com/store/view?co_code='+a2+'&co_gubun='+a1+'&cpage='+a3+'&sido=&gugun=&stname='
        except : pass
        else:
            result.append(a)
    return result

def getStoreInfo(url_list):
    url = url_list
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'logday=20200701; logdata=9010000000000%2C9050000000000%2C9020000000000%2C9040000000000%2C9050000000000%2C',
        'Host': 'www.yupdduk.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.yupdduk.com/store/list?cpage=41&sido=&gugun=&stname=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    print(url)
    pageString = requests.get(url, headers=headers)
    bsObj = bs4.BeautifulSoup(pageString.content, 'html.parser')
    result = []
    name = '동대문엽기떡볶이'
    branch = bsObj.select('body > div.container.subbody > div.row.justify-content-center.mt-4 > div > p')
    branch = str(branch).split('-')[3].replace(' ','').replace('</p>]','')
    td = bsObj.find_all('td',{"style":"width:67%;padding-right:10px;"})
    addr = str(td[0]).replace('<td style="width:67%;padding-right:10px;">','').replace('</td>','')
    if len(addr) < 10 : addr = str(td[2]).replace('<td style="width:67%;padding-right:10px;">','').replace('</td>','')
    tell = str(td[1]).replace('<td style="width:67%;padding-right:10px;">','').replace('</td>','')
    if tell.startswith('0') == False : tell = str(td[3]).replace('<td style="width:67%;padding-right:10px;">','').replace('</td>','')
    cord = str(bsObj.select('script')).split(':')[2]
    cord = str(cord).split(',')
    xcord = str(cord[1]).replace(' ','').replace(')','')
    ycord = str(cord[0]).replace(' new daum.maps.LatLng(','')
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def getStoreInfo_url_list():
    result = []
    page = 1
    while True:
        result = result + getStoreInfo_url(page)
        if len(getStoreInfo_url(page)) < 10 : break
        page += 1
    time.sleep(random.uniform(0.3, 0.9))
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()