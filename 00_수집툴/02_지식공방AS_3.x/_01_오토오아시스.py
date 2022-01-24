import sys
import time
import codecs
import requests
import random
import json
import codecs
import bs4

def main():

    outfile = codecs.open('01_오토오아시스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if len(store_list) < 5  :
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|\n' % store['tell'])
            break
        else:
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|\n' % store['tell'])
            page += 1
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo(number):
    url = 'https://www.autooasis.com/brand'
    data  ={
        'brandName': '',
        'regionL': '',
        'regionM': '',
        'position': '',
        'service': '',
        # 'numPage': '16',
        'listCnt': '5',
    }
    data['numPage'] = number
    res = requests.post(url , data = data).text
    print(url, data)
    bsObj = bs4.BeautifulSoup(res,"html.parser")
    list_all = bsObj.find_all("ul",{"class":"search_branch"})
    dataAll = []
    for ss in list_all :
        try :
            name = "오토오아시스"
            branch = ss.find("li",{"class":"branch_title"}).text.replace(" ","").rstrip().lstrip().upper()
            addr = ss.find("li",{"class":"branch_address"}).text.rstrip().lstrip().upper()
            tell = ss.find("li",{"class":"branch_phone"}).text.rstrip().lstrip().upper()
        except : pass
        else:
            dataAll.append({"name": name, "branch": branch, "addr": addr, "tell": tell})
    return dataAll

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
