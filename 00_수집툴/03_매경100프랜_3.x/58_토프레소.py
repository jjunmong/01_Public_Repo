import sys
import time
import codecs
import requests
import time
import random
import json
import bs4


def main():

    outfile = codecs.open('58_토프레소.txt', 'w', 'utf-8')
    outfile.write("IDX|NAME|BRANCH|TELL|ADDR|TIME|YCORD|XCORD\n")

    for line in getStoreInfo():
        outfile.write(line)

    outfile.close()


def getStoreInfo():
    url = 'http://www.topresso.com/skin/store/storedata.asp'
    data = {
        'method': 'keyword',
        'lat': '37.5350146',
        'lng': '127.00879880000002',
        'keyword': '점'
    }
    pageString = requests.post(url, data =data).text.replace('[','').replace(']','')
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    bsObj = str(bsObj).replace("{seq: '","").replace("', title: '","|토프레소|").replace("', phone: '","|").replace("', newAddress: '","|").replace("', address: '","|").replace("', latitude: '","|").replace("', longitude: '","|").replace("'}","").replace(",","")
    return bsObj

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
