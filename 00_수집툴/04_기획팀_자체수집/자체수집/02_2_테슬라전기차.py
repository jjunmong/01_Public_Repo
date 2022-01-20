import bs4
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\02_2_테슬라전기차\\') == False : os.makedirs('수집결과\\02_2_테슬라전기차\\')
outfilename = '수집결과\\02_2_테슬라전기차\\02_2_테슬라전기차{}.txt'.format(today)
outfilename_true = '수집결과\\02_2_테슬라전기차\\02_2_테슬라전기차{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\02_2_테슬라전기차\\02_2_테슬라전기차{}.log_실패.txt'.format(today)

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
    outfile.write("BRANCH|ADDR|TELL|CHARGER\n")

    idx_list = getSuperchagersIdx()
    for ss in idx_list:
        print(ss)
    for idx in idx_list:
        store_List = getSuperchagersInfo(idx)
        for store in store_List:
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['charger'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

    outfile = codecs.open(outfilename, 'a', 'utf-8')
    idx_list = getSuperchagersIdx2()
    for ss in idx_list:
        print(ss)
    for idx in idx_list:
        store_List = getSuperchagersInfo2(idx)
        for store in store_List:
            if store['branch'] =='서울 – 강서 수퍼 차저' : pass
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['charger'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getSuperchagersIdx():
    url = 'https://www.tesla.com/ko_KR/findus/list/superchargers/South+Korea'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    pageinfo = requests.get(url, headers = headers).text
    time.sleep(1)
    bsObj = bs4.BeautifulSoup(pageinfo,"html.parser")
    section = bsObj.find('div',{"class":"state"})
    urls = section.find_all('a')
    result =[]
    for info in urls:
        aname = info['href']
        aname2 = aname.split('/')
        aname3 = str(aname2[5:6]).replace('[','').replace(']','').replace("'","")
        result.append(aname3)
    return result
def getSuperchagersInfo(name):
    url = 'https://www.tesla.com/ko_KR/findus/location/supercharger/{}'.format(name)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    pageinfo = requests.get(url, headers=headers).text
    print(url)
    result = []
    bsObj = bs4.BeautifulSoup(pageinfo, "html.parser")
    time.sleep(1)
    div = bsObj.find('address', {"class": "vcard"})
    branch = bsObj.find('h1').text
    addr = ''
    try:
        if div.find('span', {"class": "coming-soon"}).text == 'coming soon': addr = 'coming soon'
    except:
        try:
            addr = div.find('span', {"class": "street-address"}).text
        except:
            addr = ''
    try:
        tell = div.find('span', {"class": "value"}).text.replace('\xa0','')
    except:
        tell = ''
    try:
        charger = div.select('p')[1].text
        if charger.startswith('http') or charger.startswith('www'): charger = div.select('p')[2].text
    except:
        charger = ''
    try:
        coord = str(bsObj.select_one('#location-map > a > img')['src']).split('=')[2]
        coord = coord.split(',')
        ycord = coord[0]
        xcord = str(coord[1]).replace('&zoom','')
    except:
        xcord = ''
        ycord = ''
    result.append({"branch": branch, "addr": addr, "tell": tell, "charger": charger,'xcord':xcord,'ycord':ycord})
    print(result)
    return result

def getSuperchagersIdx2():
    url = 'https://www.tesla.com/ko_KR/findus/list/chargers/South+Korea'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    pageinfo = requests.get(url, headers = headers).text
    time.sleep(1)
    bsObj = bs4.BeautifulSoup(pageinfo,"html.parser")
    section = bsObj.find('div',{"class":"state"})
    urls = section.find_all('a')
    result =[]
    for info in urls:
        aname = info['href']
        aname2 = aname.split('/')
        aname3 = str(aname2[5:6]).replace('[','').replace(']','').replace("'","")
        if aname3 == 'seoulgangseosupercharger' : pass
        else:
            result.append(aname3)
    return result

def getSuperchagersInfo2(name):
    url = 'https://www.tesla.com/ko_KR/findus/location/charger/{}'.format(name)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    pageinfo = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageinfo, "html.parser")
    time.sleep(1)
    div = bsObj.find('address', {"class": "vcard"})
    branch = bsObj.find('h1').text
    addr = ''
    result = []
    try:
        if div.find('span', {"class": "coming-soon"}).text == 'coming soon': addr = 'coming soon'
    except:
        try:
            addr = div.find('span', {"class": "street-address"}).text
        except:
            addr = ''
    try:
        tell = div.find('span', {"class": "value"}).text.replace('\xa0','')
    except:
        tell = ''
    try:
        charger = div.select('p')[1].text
        if charger.startswith('http') or charger.startswith('www') : charger = div.select('p')[2].text
    except:
        charger = ''
    try:
        coord = str(bsObj.select_one('#location-map > a > img')['src']).split('=')[2]
        coord = coord.split(',')
        ycord = coord[0]
        xcord = str(coord[1]).replace('&zoom','')
    except:
        xcord = ''
        ycord = ''
    result.append({"branch": branch, "addr": addr, "tell": tell, "charger": charger,'xcord':xcord,'ycord':ycord})
    print(result)
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()