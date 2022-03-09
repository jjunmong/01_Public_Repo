import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('07_맥시칸치킨.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|NEWADDR|OLDADDR|TELL|XCORD|YCORD\n")

    stores = getStoreList_all()
    for list in stores:
        store_list = getStoreInfo(list)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])

    outfile.close()

def getStoreList(pageNo):
    url = 'http://www.mexican.co.kr/2020/skin/store/flashmap.html?&pno={}'.format(pageNo)
    pageString = requests.get(url).text
    print(url , pageNo)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr :
        try :
            a = info.find('a')['href']
            a = str(a).replace('#','')
        except:
            pass
        else:
            result.append(a)
    return result

def getStoreList_all():
    result = []
    page = 1
    while True :
        if getStoreList(page) == []: break
        result = result + getStoreList(page)

        page += 1
    results = list(set(result))
    return results

def getStoreInfo(pageInfo):
    url = 'http://www.mexican.co.kr/2020/skin/store/{}'.format(pageInfo)
    pageString = requests.get(url).text
    print(url,pageInfo)
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    result = []
    name = '맥시칸치킨'
    branch = bsObj.select('body > div.storeview > div.storedetail > div.nametitle > h1')
    branch = str(branch).replace('[','').replace(']','').replace('<h1>','').replace('</h1>','')
    infos = bsObj.select('body > div.storeview > div.storedetail > p')
    infos = str(infos).split('/')
    addr = infos[1].replace('strong>','').replace('<br','')
    tell = infos[3].replace('strong>','').replace(' ','')
    cord = bsObj.select('script')
    cord = str(cord).split(',')
    xcord = cord[4:5]
    xcord = str(xcord).replace("[","").replace(")']","").replace("'","")
    ycord = cord[3:4]
    ycord = str(ycord).replace("[' {\\n\\t\\t\\tcenter: new daum.maps.LatLng(","").replace("]","").replace("'","").replace('}','')
    result.append({"name":name, "branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()