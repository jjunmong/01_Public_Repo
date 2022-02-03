import time
import requests
import random
import bs4
import codecs
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\11_4_어린이집집_폐지\\') == False : os.makedirs('수집결과\\11_4_어린이집집_폐지\\')
outfilename = '수집결과\\11_4_어린이집집_폐지\\어린이집_폐지_{}.txt'.format(today)
outfilename_true = '수집결과\\11_4_어린이집집_폐지\\어린이집_폐지_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\11_4_어린이집집_폐지\\어린이집_폐지_{}.log_실패.txt'.format(today)

def main():
    try:
        Crawl_run()
        outfile = codecs.open(outfilename_true, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '정상 수집 완료'
        outfile.write(write_text)
        outfile.close()
    except:
        if os.path.isfile(outfilename_true):
            os.remove(outfilename_true)
        outfile = codecs.open(outfilename_false, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '수집 실패' + '|' + str(traceback.format_exc())
        outfile.write(write_text)
        outfile.close()

def Crawl_run():
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("stcode|crname|crtel|crfax|craddr|crhome|crcapat|arcode|crstdate\n")
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
            outfile.write(u'%s\n' % store['crstdate'])
        time.sleep(random.uniform(0.9, 0.8))
    outfile.close()

def getUrl():
    with open('월별_폐지_URL.txt') as data:
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
        crstdate = info.find('crstdate').text
        data.append({"stcode":stcode,"crname":crname,"crtel":crtel,"crfax":crfax,"craddr":craddr
                     ,"crhome":crhome,"crcapat":crcapat,"arcode":arcode,"crstdate":crstdate})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()