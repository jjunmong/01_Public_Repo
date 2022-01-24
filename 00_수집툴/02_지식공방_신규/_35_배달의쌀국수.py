import sys
import codecs
import requests
import bs4
import json
import time
import random

def main():

    outfile = codecs.open('35_배달의쌀국수.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    url_list = getStoreList_dup()
    for urls in url_list:
        store_list = getStoreInfo(urls)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.6, 0.9))
    outfile.close()

def getStoreInfo_list(intPageNo):
    url = 'http://www.baessal.com/%eb%a7%a4%ec%9e%a5%ec%95%88%eb%82%b4/?board_name=sss11&mode=list&search_field=fn_title&order_by=fn_pid&order_type=desc&board_page={}&list_type=list'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url ,intPageNo)
    tbody = bsObj.find('tbody',{"id":"sss11_board_body"})
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        a = info.find('a')['href']
        result.append(a)
    return result

def getStoreList_all():
    result = []
    page = 1
    while True:
        result = result + getStoreInfo_list(page)
        if getStoreInfo_list(page) == []: break
        page += 1
        if page == 7 : break
    return result

def getStoreList_dup():
    results = list(set(getStoreList_all()))
    return results
    # result = getStoreList_all()
    # results = set()
    # new_results = []
    # for list in result:
    #     lists = tuple(list.items())
    #     if lists not in results:
    #         results.add(lists)
    #         new_results.append(list)
    # return new_results

def getStoreInfo(urls):
    url = urls
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(urls)
    result = []
    try:
        name = '배달의쌀국수'
        branch = bsObj.select('#mb_sss11_tr_title > td > span:nth-child(1)')
        branch = str(branch).split('>')
        branch = str(branch[1]).replace('</span','').lstrip().rstrip()
        addr = bsObj.select('#mb_sss11_tr_content > td > p:nth-child(1) > span')
        addr = str(addr).split(':')
        addr = str(addr[2]).replace('</span>]','').lstrip().rstrip()
        tell = bsObj.select('#mb_sss11_tr_content > td > p:nth-child(2) > span')
        tell = str(tell).split(':')
        tell = str(tell[2]).replace('</span>]','').replace('<span style="font-size','').replace('<br/>','').lstrip().rstrip()
        if branch == '광진점' : tell = '02-455-0856'
    except : pass
    else:
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
