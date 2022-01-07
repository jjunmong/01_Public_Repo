import time
import codecs
import requests
import random
import bs4
from datetime import datetime

def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\어린이집_신규_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("stcode|crname|crtel|crfax|craddr|crhome|crcapat|arcode|frstcnfmdt\n")
    url_list = getUrl()

    for url in url_list:
        store_list = getStoreInfo(url)
        print(store_list)
        for store in store_list:
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtel'])
            outfile.write(u'%s|' % store['crfax'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crhome'])
            outfile.write(u'%s|' % store['crcapat'])
            outfile.write(u'%s|' % store['arcode'])
            outfile.write(u'%s\n' % store['frstcnfmdt'])

        time.sleep(random.uniform(0.9, 0.8))

    outfile.close()
def getUrl():
    with open('월별_신규_URL.txt') as data:
        lines = data.read().splitlines()
    url_list = lines
    return  url_list

def getStoreInfo(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    pageString = requests.get(url, headers = headers).text
    time.sleep(0.2)
    print(url)
    soup = bs4.BeautifulSoup(pageString, 'lxml')
    list = soup.find_all('item')
    data = []
    for info in list:
        stcode = info.find('stcode').text
        crname = info.find('crname').text
        crtel = info.find('crtel').text
        crfax = info.find('crfax').text
        craddr = info.find('craddr').text
        crhome = info.find('crhome').text
        crcapat = info.find('crcapat').text
        arcode = info.find('arcode').text
        frstcnfmdt = info.find('frstcnfmdt').text
        data.append({"stcode":stcode,"crname":crname,"crtel":crtel,"crfax":crfax,"craddr":craddr
                     ,"crhome":crhome,"crcapat":crcapat,"arcode":arcode,"frstcnfmdt":frstcnfmdt})
    return data

main()