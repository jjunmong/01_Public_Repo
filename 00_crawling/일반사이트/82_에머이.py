import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('82_에머이.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    urls = getStoreInfo_list_all()
    for url in urls:
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

def getStoreInfo_list(intPageNo):
    url = 'http://www.emoikorea.com/board/board_list?per_page={}&code=map&search_type=&search=&sido=&gugun='.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'designart_site=sfo08d3bnaaoh295djg5fu8tu0r8q27m',
        'Host': 'www.emoikorea.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.emoikorea.com/board/board_list?per_page=2&code=map&search_type=&search=&sido=&gugun=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    print(url, intPageNo)
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    result = []
    table = bsObj.find('table',{"class":"board_list"})
    tr = table.find_all('tr')
    for info in tr:
        try:
            a = info.find('a')['href']
        except: pass
        else:
            result.append(a)
    return result

def getStoreInfo_list_all():
    result= []
    page = 1
    while True:
        result = result+getStoreInfo_list(page)
        if getStoreInfo_list(page) == [] : break
        page += 1
        time.sleep(random.uniform(0.3, 0.9))
    return result

def getStoreInfo(url_list):
    url = 'http://www.emoikorea.com'+url_list
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'designart_site=svjuje81uvapplcpn5g6i9ecd1da2out',
        'Host': 'www.emoikorea.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.emoikorea.com/board/board_list?per_page=3&code=map&search_type=&search=&sido=&gugun=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers=headers).text
    print(url_list)
    bsObj = bs4.BeautifulSoup(pageString, 'html.parser')
    result = []
    name = '에머이'
    branch = bsObj.select('#content_sub > div > div.board_view > div.view_tit > h3')
    branch =  str(branch).replace('[<h3>','').replace('</h3>]','')
    addr = bsObj.select('#content_sub > div > div.board_view > div.view_tit > div:nth-child(3)')
    addr = str(addr).replace('[<div style="clear:left;">주소 : ','').replace('</div>]','')
    tell = bsObj.select('#content_sub > div > div.board_view > div.view_tit > div:nth-child(2)')
    tell = str(tell).replace('[<div style="clear:left;">','').replace('</div>]','')
    xcord = bsObj.find('div',{"id":"map"})['data-lng']
    ycord = bsObj.find('div',{"id":"map"})['data-lat']
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()