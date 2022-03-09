import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('24_chevrolet_svc.txt', 'w', 'utf-8')
    outfile.write("##NAME|BRANCH|FEAT|XCOORD|YCOORD|ADDR|TELL|TIME|ID|CODE\n")
    list_count =int(getStore_num()) // 5 + 1
    result =[]
    for num in range(1 , list_count):
        result =result + getStore_info(num)
        time.sleep(random.uniform(0.3, 0.7))

    results = set()
    new_results = []
    for list in result:
        lists = tuple(list.items())
        if lists not in results:
            results.add(lists)
            new_results.append(list)

    for store in new_results:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['feat'])
        outfile.write(u'%s|' % store['xcoord'])
        outfile.write(u'%s|' % store['ycoord'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['time'])
        outfile.write(u'%s|' % store['id'])
        outfile.write(u'%s\n' % store['code'])

    outfile.close()

def getStore_num():
    url = 'https://www.chevrolet.co.kr/chevy/as.gm?accessType=search&addrSi=&addrGu=&workArea=&searchType=1&searchCity=0&searchGu=&firmName=%BC%AD%BA%F1%BD%BA%BC%BE%C5%CD%B8%ED%C0%BB+%C0%D4%B7%C2%C7%CF%BC%BC%BF%E4&pgIdx=1'
    try:
        urlOpen = requests.get(url)
        print(urlOpen, url)
    except:
        print('Error calling the API')
    html = urlOpen.text
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    entityList_Num = bsObj.find('h5',{"class":"result"}).text.replace('검색 결과','').replace('(','').replace(')','')
    return  entityList_Num

def getStore_info(intPageNum):
    url = 'https://www.chevrolet.co.kr/chevy/as.gm?accessType=search&addrSi=&addrGu=&workArea=&searchType=1&searchCity=0&searchGu=&firmName=%BC%AD%BA%F1%BD%BA%BC%BE%C5%CD%B8%ED%C0%BB+%C0%D4%B7%C2%C7%CF%BC%BC%BF%E4&pgIdx={}'.format(intPageNum)
    try:
        urlOpen = requests.get(url)
        print(urlOpen, url)
    except:
        print('Error calling the API')
    html = urlOpen.text
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    entityList = bsObj.find_all('li',{"class":"list"})
    # print(entityList)
    storeList = []
    for i in range(len(entityList)):
        subname_list = entityList[i].find('a')
        # print(subname_list)
        info_list = entityList[i].find('a')['onclick'].replace('asMap(','').replace(');','').replace("'",'')
        info_list_split = info_list.split(',')
        print(info_list_split)
        subname_list = subname_list.text
        storeInfo = {}
        storeInfo['name'] = '쉐보레';         storeInfo['branch'] = '';      storeInfo['feat'] = ''
        strtemp = "".join(subname_list).lstrip().rstrip()
        if strtemp.startswith('[직영]'):
            strtemp = strtemp[4:].lstrip()
            storeInfo['feat'] = '직영'
        elif strtemp.find("바로")!= -1 :
            strtemp = strtemp
            storeInfo['feat']='바로'
        elif strtemp.find("지정")!= -1 :
            strtemp = strtemp
            storeInfo['feat']='지정'
        else:
            strtemp = strtemp
            storeInfo['feat'] = ''
        storeInfo['branch'] = strtemp.lstrip().rstrip().upper()
        storeInfo['xcoord']= info_list_split[2].lstrip().rstrip().upper()
        storeInfo['ycoord']= info_list_split[1].lstrip().rstrip().upper()
        storeInfo['addr']= info_list_split[3].lstrip().rstrip().upper()
        storeInfo['time']= info_list_split[9].lstrip().rstrip().upper()
        storeInfo['tell'] = info_list_split[4].lstrip().rstrip().upper()
        storeInfo['id'] = info_list_split[5].lstrip().rstrip().upper()
        storeInfo['code'] = info_list_split[6].lstrip().rstrip().upper()

        storeList += [storeInfo]
    return storeList

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
