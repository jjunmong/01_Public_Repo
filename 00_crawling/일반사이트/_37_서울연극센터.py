import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('37_서울연극센터.txt', 'w', 'utf-8')
    outfile.write("BRANCH|ADDR|TELL|XCORD|YCORD\n")

    url_list = getStore_url()

    for url in url_list:
        store_list = getStoreInfo(url)
        print(url)
        for store in store_list:
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStore_url():
    url = 'https://www.sfac.or.kr/site/SFAC_KOR/02/10227000000002018102507.jsp'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find('div',{"class":"map_cont"})
    a = div.find_all('a')
    result = []
    for info in a:
        href = info['href']
        href = str(href).replace('main','map').replace('streetArts','ssacc').replace('sam_map.do','sgcitizenhall_map.do')
        result.append(href)
    return result

def getStoreInfo(url):
    url = 'https://www.sfac.or.kr/'+url
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    result = []
    branch = str(bsObj.select('#dBody > h1 > span > a:nth-child(1) > strong')).replace('[<strong>','').replace('</strong>]','')
    addr = str(bsObj.select('#dBody > div.space_pg > div.map_ui > ul > li:nth-child(1) > strong')).replace('[<strong>','').replace('</strong>]','').replace('오시는길','')
    if addr == '서울특별시 중구 소파로 138 (예장동 8-19)' : branch = '남산예술센터'
    tell = str(bsObj.select('#dBody > div.space_pg > div.map_ui > ul > li:nth-child(2) > strong')).replace('[<strong>','').replace('</strong>]','')
    try:
        script = str(bsObj.select('script')).split('new naver.maps.LatLng(')[1]
        script = str(script).split(')')[0]
        script = str(script).split(',')
        xcord = str(script[1]).replace(' ','')
        ycord = str(script[0]).replace(' ','')
    except :
        xcord = ''
        ycord = ''
    result.append({'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()