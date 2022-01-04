import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('70_그램그램.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    url_list = getStoreInfo_url_list()
    for url in url_list:
        storeList = getSotreInfo(url)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreNum():
    url = 'http://www.gram-gram.com/renew/html/store1.html'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ACEUCI=1; ACEUCI=1; _ga=GA1.2.1604106503.1593485394; _gid=GA1.2.1360070216.1593485394; ACEUACS=1579483474047131591; ACEFCID=UID-5EFAA851EA724EF8F147F9C1; _atrk_siteuid=_vp9RuQbhAm3YPYA; appier_utmz=%7B%22csr%22%3A%22google%22%2C%22timestamp%22%3A1593485394%2C%22lcsr%22%3A%22google%22%7D; _atrk_ssid=lJ9Z353GtKmDByl76SKJoe; _atrk_sessidx=1; appier_pv_counter9ucW14niBQtuzin=0; appier_page_isView_9ucW14niBQtuzin=48db0853061c7e8b5b4367466cd7e5287740a2e521c928cbf521e766438dfe80; appier_pv_counterePHkrf0GT5ePiVV=0; appier_page_isView_ePHkrf0GT5ePiVV=48db0853061c7e8b5b4367466cd7e5287740a2e521c928cbf521e766438dfe80',
        'Host': 'www.gram-gram.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.gram-gram.com/renew/html/store1.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,'html.parser')
    a = bsObj.select('#wrap > div.content > div.inner_sub_container > div.sub_content > table > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(5) > a')
    a = str(a).split(';')[3]
    a = str(a).split('=')[1]
    a = str(a).split('&')[0]
    a= int(a)
    return a

def getStoreInfo_url_list():
    result = []
    page = getStoreNum()
    while True:
        result = result + getStoreInfo_url(page)
        if len(getStoreInfo_url(page)) < 8 : break
        page -= 1
    time.sleep(random.uniform(0.3, 0.9))
    return result

def getStoreInfo_url(intPageNo):
    url = 'http://www.gram-gram.com/renew/html/store1.html?page={}&boardcodeb=b2015030908465355&sword=&atype=&ctype='.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ACEUCI=1; ACEUCI=1; _ga=GA1.2.1604106503.1593485394; _gid=GA1.2.1360070216.1593485394; ACEUACS=1579483474047131591; ACEFCID=UID-5EFAA851EA724EF8F147F9C1; _atrk_siteuid=_vp9RuQbhAm3YPYA; appier_utmz=%7B%22csr%22%3A%22google%22%2C%22timestamp%22%3A1593485394%2C%22lcsr%22%3A%22google%22%7D; _atrk_ssid=lJ9Z353GtKmDByl76SKJoe; _atrk_sessidx=1; appier_pv_counter9ucW14niBQtuzin=0; appier_page_isView_9ucW14niBQtuzin=48db0853061c7e8b5b4367466cd7e5287740a2e521c928cbf521e766438dfe80; appier_pv_counterePHkrf0GT5ePiVV=0; appier_page_isView_ePHkrf0GT5ePiVV=48db0853061c7e8b5b4367466cd7e5287740a2e521c928cbf521e766438dfe80',
        'Host': 'www.gram-gram.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.gram-gram.com/renew/html/store1.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,'html.parser')
    print(url, intPageNo)
    li = bsObj.find_all('tr')
    result = []
    for info in li:
        try:
            a = info.find('a')['href']
        except : pass
        else:
            result.append(a)
    return result

def getSotreInfo(url_list):
    url = 'http://www.gram-gram.com/renew/html/store1.html'+url_list
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ACEUCI=1; ACEUCI=1; _ga=GA1.2.1604106503.1593485394; _gid=GA1.2.1360070216.1593485394; ACEUACS=1579483474047131591; ACEFCID=UID-5EFAA851EA724EF8F147F9C1; _atrk_siteuid=_vp9RuQbhAm3YPYA; appier_utmz=%7B%22csr%22%3A%22google%22%2C%22timestamp%22%3A1593485394%2C%22lcsr%22%3A%22google%22%7D; _atrk_ssid=lJ9Z353GtKmDByl76SKJoe; _atrk_sessidx=1; appier_pv_counter9ucW14niBQtuzin=0; appier_page_isView_9ucW14niBQtuzin=48db0853061c7e8b5b4367466cd7e5287740a2e521c928cbf521e766438dfe80; appier_pv_counterePHkrf0GT5ePiVV=0; appier_page_isView_ePHkrf0GT5ePiVV=48db0853061c7e8b5b4367466cd7e5287740a2e521c928cbf521e766438dfe80',
        'Host': 'www.gram-gram.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.gram-gram.com/renew/html/store1.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    print(url)
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,'html.parser')
    result = []
    name = '그램그램'
    td = bsObj.select('td')
    branch = str(td[0]).replace('<td>','').replace('</td>','')
    addr = str(td[1]).replace('<td>','').replace('</td>','')
    tell = str(td[2]).replace('<td>','').replace('</td>','')
    cord = str(bsObj.select('script')).split(':')[28]
    cord = str(cord).split(',')
    xcord = str(cord[1]).replace(')','').replace(' ','')
    ycord = str(cord[0]).replace(' new daum.maps.LatLng(','').replace(' ','')
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()