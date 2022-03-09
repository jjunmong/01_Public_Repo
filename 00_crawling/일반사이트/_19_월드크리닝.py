import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('19_월드크리닝.txt', 'w', 'utf-8')
    outfile.write("ID|Ycord|Xcord|BRANCH|ADDR|TELL|TIME|ETC\n")
    sido_list = ['서울','경기','강원','충북','충남','경북','경남','전북','전남','인천','대전','울산','광주','대구','부산','세종','제주']

    for store in sido_list:
        store_list = getinfo(store)
        for store in store_list:
            outfile.write(u'%s\n' % store['infos'])

    outfile.close()

def getinfo(sido):
    url = 'http://www.worldcleaning.co.kr/use/ajax.shop.php'
    data = {
        'bound': '((33.68593973732815, 123.76868568071649), (40.521681472936486, 132.404425293687))',
        'shop_area': '서울',
        'shop_keyword': '',
    }
    print(url , sido)
    data['shop_area'] = sido
    jsonData = requests.post(url, data=data).text
    pageString = json.loads(jsonData)
    stringConvert4 = pageString['script']
    stringConvert3 = str(stringConvert4)
    stringConvert2 = stringConvert3.replace('"','').replace('</div>','').replace('</li>','').replace('</span>','')\
        .replace('\t','').replace('setMapPoint','').replace(";var locPosition = new daum.maps.LatLng(37.51625134859292, 127.10300624653243);map.setCenter(locPosition);","")\
    .replace("map.setCenter(locPosition);","").replace('\n','').replace(',','|').replace('(','').replace(')','')
    stringConvert = stringConvert2.split(';')
    result = []
    for ss in stringConvert:
        infos = ss
        result.append({"infos":infos})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()