import bs4
import codecs
import time
import requests
import sys
import random


sido_list2 = ['대전']  # 테스트용
# 경상도, 전라도가 없음...사이트 내부 자체 옵션에서도 제외되어 있음.
sido_list = ['경기','광주','대구','대전','부산','서울','세종','울산','인천','충남','충북','강원']

def main():

    outfile = codecs.open('16_불교방송_사찰암자.txt', 'w', 'utf-8')
    outfile.write("NAME|ADDR|TELL|xcord|ycord\n")

    for sido_name in sido_list:
        page = 1
        while True :
            store_list = getStores(page, sido_name)
            if store_list == None : break;

            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['xcord'])
                outfile.write(u'%s\n' % store['ycord'])

            page += 1
            if page == 99 : break

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStores(intPageNo, sido_name):
    url = "http://www.bbsi.co.kr/HOME/search/temple.html?Page={}&TITLE=&SIDO={}&GUGUN=".format(intPageNo, sido_name)
    try :
        urlopen = requests.get(url)
        print(urlopen,url)
    except :
        print('Error calling the API')
        return  None

    urlopen.encoding = 'utf-8'
    html = urlopen.text
    try :
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        infoAll = bsObj.find('ul', {"class": "list float"})
        liAll = infoAll.find_all('li')
    except AttributeError:
        pass
    else:
        data = []
        for list in liAll:
            name = list.find("div", {"class": "subject"}).text.rstrip().lstrip().replace(' ', '')
            addr1 = sido_name
            if addr1 == '경기': addr1 = '경기도'
            if addr1 == '광주': addr1 = '광주광역시'
            if addr1 == '대구': addr1 = '대구광역시'
            if addr1 == '대전': addr1 = '대전광역시'
            if addr1 == '부산': addr1 = '부산광역시'
            if addr1 == '서울': addr1 = '서울특별시'
            if addr1 == '세종': addr1 = '세종특별자치시'
            if addr1 == '울산': addr1 = '울산광역시'
            if addr1 == '인천': addr1 = '인천광역시'
            if addr1 == '충남': addr1 = '충청남도'
            if addr1 == '충북': addr1 = '충청북도'
            addr2 = list.find("div", {"class": "info"}).text.rstrip().lstrip().replace('(', '').replace(')', '-') \
                .replace('\xa0\r\n\t\t\t\t\t\t\t\t\t\t\t', '|')
            addr = addr1 + " " + addr2
            cord = list.find('a')['onclick'].replace('goMapCenter(','').replace(",11,'N')",'').replace(',','')
            xcord = cord[13:]
            ycord = cord[:13]
            data.append({"name": name, "addr": addr,"xcord":xcord,"ycord":ycord})
        return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()







