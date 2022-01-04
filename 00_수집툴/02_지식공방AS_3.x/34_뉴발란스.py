import sys
import time
import codecs
import requests
import random
import json
import bs4

sido_list = ['117', '118', '122', '116', '125', '127', '124', '129', '121', '131', '126', '120', '128', '132', '123', '130', '119']


def main():

    outfile = codecs.open('34_뉴발란스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCODR|YCORD\n")
    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page += 1
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo(intpageNo):
    url = 'https://www.nbkorea.com/support/shopListViewMore.action'
    data ={
        # 'pageNo': '3',
        'searchArea': '',
        'searchWord': '',
    }
    data['pageNo'] = intpageNo
    pageString = requests.post(url,data =data).text
    print(url, data)
    jsonString = json.loads(pageString)
    list  = jsonString['shopList']
    result = []
    for info in list:
        name = '뉴발란스'
        branch = info['ShopName']
        branch = str(branch).replace('직영상설_','').replace('사입상설_','')+'점'
        addr = info['ShopAddress']
        tell = info['TelNo']
        xcord = info['Hardness']
        ycord = info['Latitude']
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()