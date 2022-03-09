import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('69_롯데슈퍼.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종', '제주']

    for sido in sido_list:
        store_list = getStoreInfo(sido)
        print(sido)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(sidoname):
    url = 'https://www.lotteon.com/p/lotteplus/offlinestore/selectStoreSearchList'
    data = {
        'mallNo': '5',
        # 'area1': '서울',
        'area2': '',
        'strNm': '',
        'scrollIndex': '0',
        'strKndCd': '',
        'osDvsCd': 'W',
        'fromMallNo': '',
    }
    data['area1']=sidoname
    response = requests.get(url, params = data).text
    jsonString = json.loads(response)
    entityList = jsonString['storeInfo']
    result = []
    for info in entityList:
        name = info['strKndCdText']
        branch = info['strNm']
        addr = info['strAddr']
        tell = info['rprtTelNo']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()