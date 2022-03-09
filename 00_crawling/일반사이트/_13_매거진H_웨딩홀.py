import requests
import codecs
import time
import bs4
import json
import sys
import random
import re
def main():
    outfile = codecs.open('13_Magazine_wedding.txt', 'w', 'utf-8')
    outfile.write("NAME|old_addr|new_addr\n")

    idx_list = []
    for idx in range(0, 60):
        idx_list = idx_list + getStore_list(idx)
    print(idx_list)

    result = []
    for idx in idx_list:
        result = result + getSotre_info(idx)

    results2 = set()
    new_results = []
    for list in result:
        lists = tuple(list.items())
        if lists not in results2:
            results2.add(lists)
            new_results.append(list)

    for ss in new_results:
        print(ss)

    for result_list in new_results:
        outfile.write(u'%s|' % result_list['name'])
        outfile.write(u'%s|' % result_list['old_addr'])
        outfile.write(u'%s|\n' % result_list['new_addr'])
    outfile.close()


### 웨딩홀 ID LIST 가져오기
def getStore_list(intPageNo):
    url = 'http://www.magazine-h.com/hall/lists?page={}&search_kind=WNAME&SIDO=&GUGUN=&SUB_LINE=&SUB_STATION=&WTYPE=&WFOOD=&WFOODMENU=&WHUMAN=&keyword='.format(intPageNo)
    req = requests.get(url)
    req.encoding = 'utf-8'
    html = req.text
    bsObj = bs4.BeautifulSoup(html,"html.parser")
    data_all = bsObj.find_all('ul',{"class":"cutbox"})
    idx_all = []
    for list_all in data_all :
        idx = list_all.find('a')['href'].replace('/hall/view/?idx=','')
        idx_all.append(idx)
    return idx_all



##웨딩홀 IDX 리스트를 가지고 정보 가져오기

def getSotre_info(Nom):
    url = 'http://www.magazine-h.com/hall/view/?idx={}'.format(Nom)
    print(url)
    req = requests.get(url)
    response = req.content
    print(response)
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    info_all = []
    name = bsObj.find('div',{"class":"hv_name"}).text.replace('\n','').replace('웨딩홀 문의하기','').rstrip().lstrip().upper()
    old_addr = bsObj.select('ul')[5].text.replace('\n','').replace('주소','').replace('|','').rstrip().lstrip().upper()
    new_addr = bsObj.select('ul')[6].text.replace('\n','').replace('|','').replace('도로명주소','').rstrip().lstrip().upper()
    if new_addr.startswith("위치") : new_addr = "없음"
    info_all.append({"name":name, "old_addr":old_addr,"new_addr":new_addr})
    return info_all

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()