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
        store_list = getStoreInfo_store(page)
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
    url = 'https://www.winiasls.com/support/store/item'
    data = {
        'divideType': '2',
        'sido': '',
        'storeName': '',
        'storeDiv': '',
        'storeSeq': '',
        # 'pageIndex': '1',
    }
    data['pageIndex'] = pageNo
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '61',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_BS_GUUID=ybjIEz4HRAH9vZIksj0mHX5iVmeEFWrd7KWMk1tc; _TRK_CR=https%3A%2F%2Fwww.winiasls.com%2Fsupport%2Fshop; JSESSIONID=0000lfymepupQNsgUyNC5wCqv33:-1; _TRK_UID=18eb688d4fd10949e78550fb5b00e033:3:0.3074625733024691:1586843463120; _TRK_SID=660edb1140cac7a01ec2dc631ae10403; _TRK_EX=2',
        'Host': 'www.winiasls.com',
        'Origin': 'https://www.winiasls.com',
        'Referer': 'https://www.winiasls.com/support/service',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    pageString = requests.post(url, data = data, headers = headers).text
    print(url, pageNo, "svc")
    jsonString = json.loads(pageString)
    entitydata = jsonString['list']
    result = []
    for info in entitydata:
        name = '위니아에이드'
        branch = info['storeName']
        branch = str(branch).replace('위니아에이드 ','')
        sido = info['sido']
        gugun = info['gugun']
        new_addr_info = info['newAddr']
        old_addr_info = info['detailAddr']
        newaddr = sido + " " + gugun + " " + new_addr_info
        oldaddr = sido + " " + gugun + " " + old_addr_info
        tell = info['tel']
        time = info['workTime']
        result.append({"name":name,"branch":branch,"newaddr":newaddr,"oldaddr":oldaddr,"tell":tell,"time":time})
    return result

def getStoreInfo_store(pageNo):
    url = 'https://www.winiasls.com/support/store/item'
    data = {
        'divideType': '1',
        'sido': '',
        'storeName': '',
        'storeDiv': '',
        'storeSeq': '',
        # 'pageIndex': '1',
    }
    data['pageIndex'] = pageNo
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '61',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_BS_GUUID=ybjIEz4HRAH9vZIksj0mHX5iVmeEFWrd7KWMk1tc; _TRK_CR=https%3A%2F%2Fwww.winiasls.com%2Fsupport%2Fshop; JSESSIONID=0000lfymepupQNsgUyNC5wCqv33:-1; _TRK_UID=18eb688d4fd10949e78550fb5b00e033:3:0.3074625733024691:1586843463120; _TRK_SID=660edb1140cac7a01ec2dc631ae10403; _TRK_EX=2',
        'Host': 'www.winiasls.com',
        'Origin': 'https://www.winiasls.com',
        'Referer': 'https://www.winiasls.com/support/service',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    pageString = requests.post(url, data = data, headers = headers).text
    print(url, pageNo, "store")
    jsonString = json.loads(pageString)
    entitydata = jsonString['list']
    result = []
    for info in entitydata:
        name = '위니아에이드'
        branch = info['storeName']
        branch = str(branch).replace('위니아에이드 ','')
        sido = info['sido']
        gugun = info['gugun']
        if gugun == None : gugun = ''
        new_addr_info = info['newAddr']
        old_addr_info = info['detailAddr']
        newaddr = sido + " " + gugun + " " + new_addr_info
        oldaddr = sido + " " + gugun + " " + old_addr_info
        tell = info['tel']
        time = info['workTime']
        result.append({"name":name,"branch":branch,"newaddr":newaddr,"oldaddr":oldaddr,"tell":tell,"time":time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
