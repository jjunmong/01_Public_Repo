import requests
import codecs
import sys
import time
import codecs
import random
import json
import bs4

def main():
    outfile = codecs.open('03_Gukteacher.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|\n' % store['time'])
        page += 1

def getStoreInfo(pageNo):
    url = "http://www.homesfood.co.kr/bbs/board.php?bo_table=store&page={}".format(pageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    td = bsObj.findAll("tr")
    data =[]
    for info_list in td:
        try :
            name = '국선생'
            branch = info_list.find("td", {"class": "td_subject"}).text.replace('\n','')
            infos = info_list.find('td',{"class":"td_branch_addr"}).text
            addr = str(infos).split('(')[0]
            tell = str(str(infos).split('전화번호')[1]).split('\\')[0].rstrip().lstrip().replace('\n','').replace('닫기','')
            time = str(str(infos).split('영업시간')[1]).split('/')[0].rstrip().lstrip()
        except : pass
        else :
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()