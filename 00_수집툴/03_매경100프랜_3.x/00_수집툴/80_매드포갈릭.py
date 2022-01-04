import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('80_매드포갈릭.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")
    store_num_list = getStoreInfo_list()
    for num in store_num_list:
        storeList = getStoreInfo(num)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo_list():
    url = 'https://www.madforgarlic.com/store/search'
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'SCOUTER=x253uoocibgitq; btnFooterTop=; JSESSIONID=D2A522922F50F496E6D9D5CA8112283F',
        'Host': 'www.madforgarlic.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.madforgarlic.com/store/search',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    tr = bsObj.find_all('div',{"class":"list-inner"})
    result = []
    for info in tr:
        a = info.find('a')['onclick']
        a = str(a).replace("viewStore('","").replace("');","")
        if a.startswith('search') == True :pass
        else:
            result.append(a)
    return result

def getStoreInfo(listnum):
    url = 'https://www.madforgarlic.com/store/viewStoreAjax?storeSeq={}'.format(listnum)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'SCOUTER=x253uoocibgitq; btnFooterTop=; JSESSIONID=D2A522922F50F496E6D9D5CA8112283F',
        'Host': 'www.madforgarlic.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.madforgarlic.com/store',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    print(listnum, url)
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    result = []
    name = '매드포갈릭'
    branch = bsObj.find('div',{"class":"tit"}).text.replace('\n','').replace('\r','').replace('\t','').replace('배달의민족','').replace('요기요','').replace('쿠팡','').replace('이츠','')
    addr = bsObj.find('li',{"class":"add"}).text.replace('\n','').replace('주소','')
    tell =  bsObj.find('li',{"class":"tel"}).text.replace('\n','').replace('전화','')
    time = bsObj.find('li',{"class":"time"}).text.replace('\n','').replace('영업시간','')
    xcord = bsObj.find('input',{"name":"store_lng"})['value']
    ycord = bsObj.find('input',{"name":"store_lat"})['value']
    result.append({'name':name, 'branch':branch, 'addr':addr,'tell':tell,'time':time,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
