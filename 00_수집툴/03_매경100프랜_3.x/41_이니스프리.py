import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('41_이니스프리.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")
    sido_list = ['서울','경기','강원','충북','충남','경북','경남','전북','전남','인천','대전','울산','광주','대구','부산','세종','제주']

    for sido in sido_list:
        store_list = getInfo(sido)
        print(sido)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getInfo(sido):
    url = 'https://m.innisfree.com/kr/ko/mFindStoreListAjax.do'
    data = {
        'pageType': 'area',
        # 'gubun1': '강원',
        'gubun2': '',
        'custNm': '',
    }
    data['gubun1'] = sido
    pageString = requests.post(url, data= data).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        name = "이니스프리"
        branch = info.find('div',{"class":"tit"}).text
        addr = info.find('div',{"class":"adrs"}).text
        try:
            tell = info.find('div',{"class":"tel"}).text
        except AttributeError:
            tell = ''
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

