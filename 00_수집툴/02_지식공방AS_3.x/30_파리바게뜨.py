import sys
import time
import codecs
import requests
import random
import json
import bs4

sido_list = ['117', '118', '122', '116', '125', '127', '124', '129', '121', '131', '126', '120', '128', '132', '123', '130', '119']


def main():

    outfile = codecs.open('30_빠리바게트.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCODR|YCORD\n")

    for sido in sido_list:
        store_list = getStoreInfo(sido)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])

    outfile.close()

def getStoreInfo(sidoCode):
    url = 'https://www.paris.co.kr/wp-admin/admin-ajax.php'
    data = {
        'action': 'pb_store_get_list',
        'type': '#search',
        'keyword': '',
        # 'area1': '118',
        'area2': '',
        'latitude': '37.4964224',
        'longitude': '127.03498239999998',
    }
    data['area1'] = sidoCode
    pageString = requests.get(url , params = data).text
    print(url, sidoCode)
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    div = bsObj.find_all('div')
    result = []
    for info in div:
        try:
            name = '파리바게뜨'
            branch = info.find('span',{"class":"label"}).text
            addr = info.find('p',{"class":"store-addr"}).text
            tell = info.find('a',{"class":"tel"}).text
            xcord = info['data-longitude']
            ycord = info['data-latitude']
        except :
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()