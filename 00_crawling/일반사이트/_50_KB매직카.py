import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('50_KB매직카.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    urls = getStoreInfo_list()

    for url in urls:
        store_list = getStoreInfo(url)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo_list():
    url = 'https://www.mandoplaza.com/service/shop_location?is_official=Y'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'mobileapp=N; mandoplazacom_firstmall=448c0d0f680bb15e36c2b87f95758d0a6af955e3; shopReferer=https%3A%2F%2Fwww.google.co.kr%2F; refererDomain=google.co.kr; marketplace=google; mandoplazacomvisitorInfo=a%3A2%3A%7Bs%3A4%3A%22date%22%3Bs%3A10%3A%222020-06-16%22%3Bs%3A7%3A%22referer%22%3Bs%3A25%3A%22https%3A%2F%2Fwww.google.co.kr%2F%22%3B%7D; mobileapp=N',
        'Host': 'www.mandoplaza.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.mandoplaza.com/service/shop_location?is_as=Y',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find_all('ul',{"class":"tbody"})
    result = []
    for info in div:
        link = info.find('a')['href']
        result.append(link)
    return result


def getStoreInfo(urls):
    url = 'https://www.mandoplaza.com/service/'+urls
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'mobileapp=N; shopReferer=https%3A%2F%2Fwww.google.co.kr%2F; refererDomain=google.co.kr; marketplace=google; mobileapp=N; mandoplazacom_firstmall=1035463601ae33060e7ba7d1f2037d40e8ba9cda; mandoplazacomvisitorInfo=a%3A2%3A%7Bs%3A4%3A%22date%22%3Bs%3A10%3A%222020-06-17%22%3Bs%3A7%3A%22referer%22%3Bs%3A62%3A%22https%3A%2F%2Fwww.mandoplaza.com%2Fservice%2Fshop_location%3Fis_official%3DY%22%3B%7D',
        'Host': 'www.mandoplaza.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.mandoplaza.com/service/shop_location?is_official=Y',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url)
    result = []
    name = '만도플라자'
    branch = bsObj.select('#layout_body > div > form > div.shp_info_bx > div.shp_info_tit')
    branch = str(branch).replace('[<div class="shp_info_tit">','').replace('</div>]','').replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    addr = bsObj.select('#layout_body > div > form > div.shp_info_bx > div.shp_info_in > div.shp_info_in_right > ul > li:nth-child(5) > div.con')
    addr = str(addr).replace('[<div class="con">','').replace('</div>]','').lstrip().rstrip()
    tell = bsObj.select('#layout_body > div > form > div.shp_info_bx > div.shp_info_in > div.shp_info_in_right > ul > li:nth-child(3) > div.con')
    tell = str(tell).replace('[<div class="con">','').replace('</div>]','').lstrip().rstrip()
    time = bsObj.select('#layout_body > div > form > div.shp_info_bx > div.shp_info_in > div.shp_info_in_right > ul > li:nth-child(4) > div.con')
    time = str(time).replace('[<div class="con">','').replace('</div>]','').lstrip().rstrip()
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

