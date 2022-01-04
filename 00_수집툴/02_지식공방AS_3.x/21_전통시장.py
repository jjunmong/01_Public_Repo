import bs4
import codecs
import time
import requests
import sys
import random

def main():

    outfile = codecs.open('21_전통시장.txt', 'w', 'utf-8')
    outfile.write("NAME|MKT_CD|SIDO|SIGUNGU|ADDR\n")

    store_list = getStores()

    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['mkt_cd'])
        outfile.write(u'%s|' % store['siDo'])
        outfile.write(u'%s|' % store['siGunGu'])
        outfile.write(u'%s\n' % store['addr'])

    outfile.close()

def getStores():
    url = "http://www.sbiz.or.kr/sijangtong/nation/sijang/readSijangListAjax.do"
    data = {
        'special_mkt_yn': '',
        'siDo': '',
        'siGunGu': '',
        'city_cd': '',
        'county_cd': '',
        'marketName': '',
        'item': ''
    }
    try :
        urlopen = requests.post(url , data = data)
        print(urlopen,url)
    except :
        print('Error calling the API')
    urlopen.encoding = 'utf-8'
    html = urlopen.text
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    tr = bsObj.find_all('tr')
    print(tr)
    data=[]
    for ss in tr:
        try:
            name = ss.find('a')['marketname'].lstrip().rstrip().upper()
            mkt_cd = ss.find('a')['mkt_cd'].lstrip().rstrip().upper()
            siDo = ss.find('a')['sido'].lstrip().rstrip().upper()
            siGunGu = ss.find('a')['sigungu'].lstrip().rstrip().upper()
            addr = ss.select('td')[1].text.replace('\n','').replace('\t','').lstrip().rstrip().upper()
        except :
            pass
        if len(addr) < 15:
            pass
        # if  addr.replace(' ','').replace('(','').replace(')','').isalpha() == True :
        #     pass
        else:
            data.append({"name":name,"mkt_cd":mkt_cd,"siDo":siDo,"siGunGu":siGunGu,"addr":addr})

    results = set()
    new_results = []
    for list in data:
        lists = tuple(list.items())
        if lists not in results:
            results.add(lists)
            new_results.append(list)

    return  new_results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()