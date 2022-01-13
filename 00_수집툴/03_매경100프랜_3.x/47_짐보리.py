import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('47_짐보리등.txt', 'w', 'utf-8')
    outfile.write("BRANCH|ADDR|TELL|XCORD|YCORD|TIME\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == []: break;

        for store in storeList:
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['time'])

        page += 1

        if page == 10: break

        time.sleep(random.uniform(0.3, 0.9))

def getStoreInfo(pageNo):
    url = 'http://www.magformersworld.com/GHome/Common/store_list_div.asp'
    data= {
        'ONOFF': 'F',
        'SM':'',
        # 'PAGE':'1',
        'CNT': '1000',
    }
    data['PAGE'] = pageNo
    pageString = requests.post(url, data=data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li',{"class":"store_li"})
    print(url, pageNo)
    result = []
    for info in li:
        branch = info.find('dt',{"class":"offline_tit"}).text.replace('[','').replace('] ',' ').replace(' \u3000\u3000','')
        addr = info.find('dl',{"class":"add"}).text.replace('\n','').replace('주소 : ','')
        tell = info.find('dl',{"class":"tel"}).text.replace('\n','').replace('연락처 : ','')
        time = info.find('dl',{"class":"open"}).text.replace('\n','').replace('영업시간 : ','')
        cord = info.find('a')['href']
        cord = str(cord).replace("javascript:OpenMap('","").replace("');","").replace("'","")
        cord = cord.split(',')
        xcord = cord[1]
        ycord = cord[0]
        result.append({"branch":branch,"addr":addr,"tell":tell,"time":time,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
