import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('06_빕스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|OLDADDR|NEWADDR|TELL|TIME|PARKIMG\n")

    stores = getStoreListAll()
    for list in stores:
        store_list = getStoreInfo(list)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['oldaddr'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['time'])
            outfile.write(u'%s\n' % store['parking'])

    outfile.close()

def getStoreList(pageNo):
    url = 'https://www.ivips.co.kr:7002/store/storeStoreInfoQ.asp?pageseq={}'.format(pageNo)
    pageString = requests.get(url).text
    print(url , pageNo)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try :
            a = info.find('a')['href']
            a= str(a).split("'")[1]
        except :
            pass
        else :
            result.append(a)
    return result

def getStoreListAll():
    result = []
    page = 1
    while True:
        if getStoreList(page) == [] : break
        result = result + getStoreList(page)
        page += 1

    results = list(set(result))

    return results
def getStoreInfo(list_code):
    url = 'https://www.ivips.co.kr:7002/store/storeStoreDetailPrt.asp'
    data = {
        'compCD': 'vips',
        # 'JUMCODE': 'SH0074',
        'pageseq': '3',
        'premier_type': '',
        'store_type': '',
        'taste_type': '',
        'dlight_type': '',
        'onebir_type': '',
        'lactation_type': '',
        'play_type': '',
        'kids_type': '',
        'event_room': '',
        'seminar_room': '',
        'wifi': '',
        'house_wedding': '',
        'jumname': '',
        'city': '',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '207',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ASPSESSIONIDQARCBATD=DBCAAOGBBNEPICKDIAHGDEDE; ACEFCID=UID-5E7C4FE06119D705155D2CAD; _ga=GA1.3.1677209801.1585205217; _gid=GA1.3.1371865254.1585205217',
        'Host': 'www.ivips.co.kr:7002',
        'Origin': 'https://www.ivips.co.kr:7002',
        'Referer': 'https://www.ivips.co.kr:7002/store/storeStoreInfoQ.asp?pageseq=3',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    }
    data['JUMCODE'] = list_code
    pageString = requests.post(url, data = data).text
    print(url,list_code)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = 'VIPS'
    branch = bsObj.select('#content > div > div.stInfo > div.clfix > h5')
    branch = str(branch).replace('[','').replace(']','').replace('<h5>','').replace('</h5>','').replace(' ','')
    addr = bsObj.select('#content > div > div.stInfo > table > tbody > tr:nth-child(3) > td')
    addr = str(addr).replace('[', '').replace(']', '').replace('<td>','').replace('</td>','').replace('<br/>','').replace('도로명주소 : ','').replace(' 지번주소 : ','|')
    addr = addr.split('|')
    try:
        oldaddr = addr[1]
    except:
        oldaddr = ''
    newaddr = addr[0]
    tell = bsObj.select('#content > div > div.stInfo > table > tbody > tr:nth-child(2) > td')
    tell = str(tell).replace('[', '').replace(']', '').replace('<td>','').replace('</td>','').replace('\n','').replace('\t','').replace('\xa0','').replace(',',' /')
    time = bsObj.select('#content > div > div.stInfo > table > tbody > tr:nth-child(5) > td')
    time = str(time).replace('[', '').replace(']', '').replace('<td>','').replace('</td>','')
    parking = bsObj.select('#content > div > div.stInfo > table > tbody > tr:nth-child(7) > td')
    parking = str(parking).replace('[', '').replace(']', '').replace('<td>','').replace('</td>',' ')
    result.append({"name":name, "branch":branch,"oldaddr":oldaddr,'newaddr':newaddr,"tell":tell,"time":time,"parking":parking})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()