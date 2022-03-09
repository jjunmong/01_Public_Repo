import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('45_삼성생명.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|CAT|ADDR|TELL|TIME|XCORD|YCORD\n")

    store_list = getStoreInfo()

    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['cat'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['time'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3,0.6))

    outfile.close()
def getStoreInfo():
    url ="https://www.samsunglife.com/gw/api/cs/location/search/location"
    data = {
        'g': 'srH0OdXoU53DAFRpbu2fQvkwwIHbdHCwJQdy3F2P6dqPDudkSREBQThT0A9yPQ==',
        'b': 'NThhZDcwMzkwYzMyNDA2Njk5MjYzMjI5YjM0ODZlZDLCutQ83M56t4ZbKmNiv8tMlRfDx8ItEs8pE3KuRt+Qj+5831YlO1xmHmTxDiREm78bxhJT558EOgc5yE8=',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '203',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'WMONID=Z0ZuiwDZldT; m1JSESSIONID=0PWJsNz9dvMV9k_y-o9kXL8HGhSR9fPqrKHoCeVJWTHf-JO-8g64!1961240335!-912231132; AMCVS_F93A97AE5992D29C0A495DC2%40AdobeOrg=1; AMCV_F93A97AE5992D29C0A495DC2%40AdobeOrg=1075005958%7CMCIDTS%7C18669%7CMCMID%7C73126879467606632730252250585786401541%7CMCAAMLH-1613527603%7C11%7CMCAAMB-1613527603%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1612930004s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.1; s_ptc=%5B%5BB%5D%5D; s_cc=true; s_ppn=%EA%B3%A0%EA%B0%9D%EC%84%BC%ED%84%B0%3E%EC%A7%80%EC%A0%90%EC%B0%BE%EA%B8%B0; s_ppvl=%25uBA54%25uC778%2C68%2C22%2C791%2C1503%2C791%2C1920%2C1080%2C1%2CP; s_ppv=%25uACE0%25uAC1D%25uC13C%25uD130%253E%25uC9C0%25uC810%25uCC3E%25uAE30%2C62%2C62%2C791%2C1503%2C791%2C1920%2C1080%2C1%2CP; s_sq=%5B%5BB%5D%5D; s_sn=%5B%5B%27PC%27%2C%271612923704621%27%5D%5D',
        'dcpChnlTyp': 'PC',
        'Host': 'www.samsunglife.com',
        'Origin': 'https://www.samsunglife.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.samsunglife.com/individual/cs/location/MDP-CUBRF040100M',
        'timeout': '900000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    }
    pageString = requests.post(url, data = data, headers = headers).text
    jsonString = json.loads(pageString)
    entityList = jsonString['response']
    result = []
    for info in entityList:
        name= '삼성생명'
        branch = info['subList'][0]['gname']
        cat = info['subList'][0]['bScCd']
        addr = info['subList'][0]['address']
        tell = info['subList'][0]['tel']
        time = info['subList'][0]['bTime']
        xcord = info['lng']
        ycord = info['lat']
        result.append({'name':name,'branch':branch,'cat':cat,'addr':addr,'tell':tell,'time':time,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()