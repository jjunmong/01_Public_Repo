import sys
import time
import codecs
import requests
import random
import json
import bs4

# sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시', '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주특별자치도']
sido_code = ['0','1','2','3','4','5','6','7']
def main():

    outfile = codecs.open('12_TG삼보서비스센터.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|XCORD|YCORD\n")

    for sido in sido_code:
        store_list = getStoreInfo(sido)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])

    outfile.close()

def getStoreInfo(sidoCode):
    url = 'https://www.trigem.co.kr/customer/ascenter/ascenter.jsp'
    data ={}
    data['province'] = sidoCode
    print(url, sidoCode)
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr',{"class":"board_list2"})
    result = []
    for info in tr:
        try:
            name = 'TG삼보서비스센터'
            branch = info.find('td',{"align":"center"}).text
            addr = info.find('td',{"align":"left"}).text
            cord = info.find('a')['href']
            cord = str(cord).split('&')
            xcord = cord[3]
            xcord = str(xcord).replace('x=','')
            if xcord.startswith('q') == True : xcord = str(cord[2]).replace('lng=','')
            elif branch == 'TGS동래센터' : xcord =''
            ycord = cord[4]
            ycord = str(ycord).replace('y=', '')
            if ycord.startswith('t') == True: ycord = str(cord[1]).replace('lat=', '')
            elif branch == 'TGS동래센터': ycord = ''
        except:
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
