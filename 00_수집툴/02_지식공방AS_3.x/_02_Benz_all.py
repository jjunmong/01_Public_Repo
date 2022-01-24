import sys
import time
import codecs
import requests
import random
import json
import codecs
import bs4
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():

    outfile = codecs.open('02_Benz_svc.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|WEEKTIME|SATTIME|SUNTIME\n")

    store_list = getStoreInfo_svc()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['week_time'])
        outfile.write(u'%s|' % store['sat_time'])
        outfile.write(u'%s\n' % store['sun_time'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

    outfile = codecs.open('02_Benz_showroom.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|\n")

    url_list = getStoreInfo_showroom_list()
    for urls in url_list:
        store_list = getStoreInfo_showroom(urls)
        print(urls)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo_svc():
    url = 'https://www.theclasshyosung.com/ko/desktop/passenger-cars/service/service-and-accessories/service-center.html'
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    p = bsObj.find_all('p',{"class":"wb-e-pgph-text"})
    result = []
    for info in p:
        name = '벤츠'
        info = str(info)
        info_split = info.split('<')
        branch = str(info_split[1]).replace('br>','').replace('\xa0','').replace('br/>','').replace('\n','').replace('p class="wb-e-pgph-text">','').replace(' ','')
        addr = str(info_split[2]).replace('br>','').replace('\xa0','').replace('br/>','').replace('\n','').replace('주소 :','').replace('주소: ','').lstrip().rstrip()
        tell = str(info_split[3]).replace('br>','').replace('\xa0','').replace('br/>','').replace('\n','').replace('전화 :','').replace('전화:','').lstrip().rstrip()
        week_time = str(info_split[6]).replace('br>','').replace('\xa0','').replace('br/>','').replace('\n','').replace('월~금: ','').lstrip().rstrip()
        sat_time = str(info_split[7]).replace('br>','').replace('\xa0','').replace('br/>','').replace('\n','').replace('토요일: ','').lstrip().rstrip()
        sun_time = str(info_split[8]).replace('br>','').replace('\xa0','').replace('br/>','').replace('\n','').replace('일요일 및 공휴일 :','').lstrip().rstrip()
        if branch == '구리센터' :
            week_time = str(info_split[5]).replace('br>', '').replace('\xa0', '').replace('br/>', '').replace('\n',
                                                                                                              '').replace(
                '월~금: ', '').lstrip().rstrip()
            sat_time = str(info_split[6]).replace('br>', '').replace('\xa0', '').replace('br/>', '').replace('\n',
                                                                                                             '').replace(
                '토요일: ', '').lstrip().rstrip()
            sun_time = str(info_split[7]).replace('br>', '').replace('\xa0', '').replace('br/>', '').replace('\n',
                                                                                                             '').replace(
                '일요일 및 공휴일 :', '').lstrip().rstrip()
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"week_time":week_time,"sat_time":sat_time,"sun_time":sun_time})
    return result

def getStoreInfo_showroom_list():
    url = 'https://www.theclasshyosung.com/ko/desktop/passenger-cars/showroom-2/Sales-Showroom.html'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            urls = info.find('a')['href']
        except:
            pass
        else:
            if urls.startswith('/ko/desktop/passenger-cars/showroom-2/Sales-Showroom/') == True : result.append(urls)
            else: pass
    results = list(set(result))
    return results

def getStoreInfo_showroom(url_list):
    url = 'https://www.theclasshyosung.com'+url_list
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    name = '벤츠'
    branch = bsObj.select('#standard-wrapper > section > section.col-sm-9.standard-content.nc-main.nc-car1 > div:nth-child(1) > div > h2')
    branch = str(branch).replace('[<h2 class="wb-e-hdl-3">','').replace('</h2>]','').replace(' ','')
    addr = bsObj.select('#standard-wrapper > section > section.col-sm-9.standard-content.nc-main.nc-car1 > div.par > div.bulletpointlist.abstractcomponent > div > div > div > ul > li:nth-child(1)')
    addr = str(addr).replace('[<li class="wb-e-bulletlist-2__item col-md-12">주소 : ', '').replace('</li>]', '')
    tell = bsObj.select('#standard-wrapper > section > section.col-sm-9.standard-content.nc-main.nc-car1 > div.par > div.bulletpointlist.abstractcomponent > div > div > div > ul > li:nth-child(2)')
    tell = str(tell).replace('[<li class="wb-e-bulletlist-2__item col-md-12">', '').replace('</li>]', '').replace('전화 : ','').replace(')','-').replace(' ','')
    time = bsObj.select('#standard-wrapper > section > section.col-sm-9.standard-content.nc-main.nc-car1 > div.par > div.bulletpointlist.abstractcomponent > div > div > div > ul > li:nth-child(4)')
    time = str(time).replace('[<li class="wb-e-bulletlist-2__item col-md-12">', '').replace('</li>]', '').replace('영업시간 : ','')
    result=[]
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
