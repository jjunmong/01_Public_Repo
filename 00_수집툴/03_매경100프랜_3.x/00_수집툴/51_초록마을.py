import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('51_초록마을.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")
    sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종', '제주']

    for sido in sido_list:
        page = 1
        while True:
            storeList = getStoreInfo(sido,page)
            if storeList == []: break;

            for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])

            page += 1

            if page == 30: break

            time.sleep(random.uniform(0.6, 0.9))

def getStoreInfo(sidoname,pageNo):
    url = 'https://www.choroc.com/green/webpage/estore/shopguide/nStore_directsearch.jsp'
    data ={}
    data['cpage'] = pageNo
    data['search'] = sidoname
    pageString = requests.post(url, data=data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, sidoname, pageNo)
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = "초록마을"
            branch = info.find("td").text
            branch = branch.split("\r")
            branch= branch[0]
            addr = info.find("td",{"class":"subject"}).text.rstrip().lstrip().replace('(',' ')
            addr = addr.split('  ')
            addr = addr[0]
            tell = info.find("p",{"class":"tel_no"}).text.replace(')','-').rstrip().lstrip()
        except :
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
