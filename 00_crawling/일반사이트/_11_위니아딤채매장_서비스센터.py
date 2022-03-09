import sys
import time
import codecs
import requests
import random
import json
import bs4

# sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시', '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주특별자치도']

def main():

    outfile = codecs.open('14_위니아에이드서비스센터.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|NEWADDR|OLDADDR|TELL|TIME\n")

    page = 1
    while True:
        store_list = getStoreInfo_svc(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['oldaddr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page += 1
    outfile.close()

    outfile = codecs.open('14_위니아에이드매장.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|NEWADDR|OLDADDR|TELL|TIME\n")

    page = 1
    while True:
        store_list = getStoreInfo_shop(page)
        if store_list == []: break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['oldaddr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page += 1
    outfile.close()


def getStoreInfo_svc(pageNo):
    url = 'https://www.winiadimchae.com/support/system_ajax.jsp'
    data = {
        'ORDER': 'SEARCH',
        '_SIDO': '',
        'SEARCH_VALUE': '',
        # 'nowPage': '1',
        'type': '2',
    }
    data['nowPage'] = pageNo
    pageString = requests.post(url, data=data).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '위니아에이드'
            branch = info.find('a').text
            addr = info.find('p').text
            addr = addr.split('(지번)')
            newaddr = addr[0]
            oldaddr = addr[1]
            tell = info.find('p', {"class": "phone"}).text
            time = info.find('p', {"class": "store_info"}).text
        except:pass
        else:
            result.append({"name": name, "branch": branch, "newaddr": newaddr, "oldaddr": oldaddr, "tell": tell, "time": time})
    return result

def getStoreInfo_shop(pageNo):
    url = 'https://www.winiadimchae.com/support/system_ajax.jsp'
    data = {
        'ORDER': 'SEARCH',
        '_SIDO': '',
        'SEARCH_VALUE': '',
        # 'nowPage': '1',
        'type': '1',
    }
    data['nowPage'] = pageNo
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '위니아에이드'
            branch = info.find('a').text
            addr = info.find('p').text
            addr = addr.split('(지번)')
            newaddr = addr[0]
            oldaddr = addr[1]
            tell = info.find('p', {"class": "phone"}).text
            time = info.find('p', {"class": "store_info"}).text
        except:pass
        else:
            result.append({"name": name, "branch": branch, "newaddr": newaddr, "oldaddr": oldaddr, "tell": tell, "time": time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
