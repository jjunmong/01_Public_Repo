import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('79_라라코스트.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    url_list = getStoreList_all()
    for url in url_list:
        storeList = getStoreInfo(url)
        if storeList == [] : break
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
    url = 'https://raracost.com/pg/bbs/board.php?bo_table=Nstore&page={}'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=akhbhkusptvvrnhfhg70ppj992; f33d2ed86bd82d4c22123c9da444d8ab=MTU5NDcwOTIxMQ%3D%3D; 96b28b766b7e0699aa91c9ff3d890663=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvLmtyLw%3D%3D; 2a0d2363701f23f8a75028924a3af643=MTEyLjE2OS4zMy42Nw%3D%3D; wcs_bt=411bb230b5830:1594709210; _ga=GA1.2.1209313978.1594709211; _gid=GA1.2.142839040.1594709211; _gat_gtag_UA_108055291_1=1',
        'Host': 'raracost.com',
        'Pragma': 'no-cache',
        'Referer': 'http://raracost.com/pg/bbs/board.php?bo_table=Nstore&page=2',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    tr = bsObj.find_all('td')
    result = []
    for info in tr:
        try:
            a = info.find('a')['href']
        except : pass
        else:
            if a.startswith('https://raracost.com/pg/bbs/board.php?bo_table=') == False : pass
            else:
                result.append(a)
    return result

def getStoreList_all():
    page = 1
    result = []
    while True :
        result = result+ getStoreInfo_url(page)
        if getStoreInfo_url(page) == [] : break
        print(page)
        page+=1
    return result

def getStoreInfo(urls):
    url = urls
    print(urls)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    result = []
    name = '라라코스트'
    branch = bsObj.find('h4').text
    addr = str(bsObj.select('#bo_v > header > div.tour-info > ul > li:nth-child(2) > dd')).replace('[<dd>','').replace('</dd>]','')
    tell = str(bsObj.select('#bo_v > header > div.tour-info > ul > li:nth-child(1) > dd')).replace('[<dd>','').replace('</dd>]','')
    cord = str(bsObj.select('script')).split('new daum.maps.LatLng(')[1]
    cord = str(cord).split(',')
    xcord = str(cord[1]).replace(')','').lstrip().rstrip()
    ycord =  str(cord[0]).lstrip().rstrip()
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()