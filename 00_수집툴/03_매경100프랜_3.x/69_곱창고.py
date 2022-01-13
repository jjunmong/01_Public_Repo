import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('69_곱창고.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    url_list = getStoreInfo_url_list()
    for url in url_list:
        storeList = getSotreInfo(url)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['time'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo_url_list():
    result = []
    page = 1
    while True:
        result = result + getStoreInfo_url(page)
        if getStoreInfo_url(page) == [] : break
        page += 1
    time.sleep(random.uniform(0.3, 0.9))
    return result

def getStoreInfo_url(intPageNo):
    url = 'http://www.gobchanggo.co.kr/board/index.php?board=map_01&sca=all&type=list&select=&search=&page={}&now_date=h7hQv'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=57prfe1vsp4cpgq81d0ovdsm37',
        'Host': 'www.gobchanggo.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://www.gobchanggo.co.kr/board/index.php?board=map_01&sca=all',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,'html.parser')
    li = bsObj.find_all('li',{"class":"store_li"})
    result = []
    for info in li:
        a = info.find('a')['href']
        result.append(a)
    return result

def getSotreInfo(url_list):
    url = 'http://www.gobchanggo.co.kr/'+url_list
    print(url)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,'html.parser')
    result = []
    name = '곱창고'
    branch = bsObj.select('#boardWrap > div.store_info_wrap > div.store_info_right.f_right > p')
    branch = str(branch).replace('[<p class="store_info_tit">','').replace('</p>]','')
    addr = bsObj.select('#boardWrap > div.store_info_wrap > div.store_info_right.f_right > ul > li.store_info1 > p.store_info_txt02')
    addr = str(addr).replace('[<p class="store_info_txt02">','').replace('</p>]','')
    tell = bsObj.select('#boardWrap > div.store_info_wrap > div.store_info_right.f_right > ul > li.store_info2 > p.store_info_txt02')
    tell = str(tell).replace('[<p class="store_info_txt02">','').replace('</p>]','')
    time = bsObj.select('#boardWrap > div.store_info_wrap > div.store_info_right.f_right > ul > li.store_info3 > p.store_info_txt02')
    time = str(time).replace('[<p class="store_info_txt02">','').replace('</p>]','')
    cord = str(bsObj.select('script')).split(':')
    ycord = str(cord[14]).replace(', lng','').replace("'","").replace(' ','')
    xcord = str(cord[15]).replace('},','').replace("'","").replace(' ','').replace('\n\tscrollwheel','')
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()