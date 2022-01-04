import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('59_요거프레소.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if len(store_list) < 10 :
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['tell'])
                outfile.write(u'%s\n' % store['time'])
            break
        print(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page+=1
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://www.yogerpresso.co.kr/founded/store/store_sub01.html?page={}&s_sido=&s_sigungu=&s_key=&s_parking=&s_wifi=&s_new=&s_delivery=&s_allday='.format(intPageNo)
    response = requests.get(url, verify = False).text
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    div = bsObj.find_all('div',{"class":"m_con"})
    result = []
    for info in div:
        try:
            name = '요거프레소'
            branch = info.find('div',{"class":"name_con"}).text.replace('\n','').replace('\r','').replace('\t','')
            addr = info.find('div',{"class":"address_con"}).text.replace('\n','').replace('\r','').replace('\t','')
            tell = str(info.find('a')['href']).replace('tel:','')
            time = info.find('div',{"class":"info_con"}).text.replace('\n','').replace('\r','').replace('\t','')
        except :
             pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()