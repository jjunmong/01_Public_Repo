import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('66_올리브영.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page+= 1

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://www.oliveyoung.co.kr/store/store/getStoreListJsonAjax.do'
    data = {
        # 'pageIdx': '1',
        'searchType': 'new',
        'openYn': 'N',
        'tcCd': '',
        'psCd': '',
        'usrLat': '37.4964224',
        'usrLng': '127.0382592',
    }
    data['pageIdx'] = intPageNo
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    response = requests.post(url, data = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '올리브영'
            branch = info.find('a').text
            addr = info.find('p',{"class":"addr"}).text
            tell = info.find('div',{"class":"call"}).text
            xcord = info.find('input',{"class":"lng"})['value']
            ycord = info.find('input',{"class":"lat"})['value']
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()