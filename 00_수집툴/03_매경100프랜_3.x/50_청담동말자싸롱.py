import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('50_청담동말자싸롱.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == []: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['time'])

        page += 1

        if page == 30: break

        time.sleep(random.uniform(0.6, 0.9))

def getStoreInfo(pageNo):
    url = 'http://www.malja.co.kr/bbs/board.php'
    data= {
        'bo_table': 'store'
    }
    data['page'] = pageNo
    pageString = requests.get(url, params=data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, pageNo)
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr',{"class":""})
    result = []
    for info in tr:
        try:
            name = "청담동말자싸롱"
            branch = info.find("td",{"class":"store_name"}).text.rstrip().lstrip()
            addr = info.find("td",{"class":"t_left t_new store_address"}).text.rstrip().lstrip()
            tell = info.find("td",{"date-th":"전화번호"}).text.replace(')','-').rstrip().lstrip()
            time = info.find("td",{"date-th":"영업시간"}).text.rstrip().lstrip()
            cord = info.find("a")['onclick']
            cord = cord.split(',')
            xcord = cord[0].replace("viewMap(","")
            ycord = cord[1].replace(")","")
        except:
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
