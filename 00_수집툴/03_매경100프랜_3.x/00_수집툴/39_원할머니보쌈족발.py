import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('39_원할머니보쌈족발.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|NEW_ADDR|OLD_ADDR|TELL|TIME\n")

    allList = getStoreidx()
    numList = []
    for info in allList:
        a = info['idx']
        numList.append(a)

    xList = []
    for info in allList:
        a = info['xcord']
        xList.append(a)

    yList = []
    for info in allList:
        a = info['ycord']
        yList.append(a)

    for num, x, y in zip(numList, xList, yList):
        store_List = getStoreInfo(num, x, y)
        print(num, x, y)
        for store in store_List:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['new_addr'])
            outfile.write(u'%s|' % store['old_addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['time'])

    outfile.close()

def getStoreidx():
    url = 'https://wonandone.co.kr/inc/storeMapData.asp'
    data = {
        'KeyBrand': 'w',
        'KeyOrder': 'S',
        'KeyAddr1': '서울',
        'KeyAddr2': '중구',
        'KeyWord': '점',
    }
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    entityList = jsonString['items']
    result = []
    for info in entityList:
        idx = info['store_idx']
        xcord = info['longi']
        ycord = info['lati']
        result.append({'idx':idx,'xcord':xcord,'ycord':ycord})
    return result

def getStoreInfo(intPageNo, xcord, ycord):
    url = 'https://wonandone.co.kr/inc/storeView.asp?store_idx={}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result =[]
    name = '원할머니보쌈족발'
    branch = bsObj.find('h4').text
    new_addr = str(bsObj.select('td')[0]).replace('<td>','').replace('</td>','')
    old_addr = str(bsObj.select('td')[1]).replace('<td>','').replace('</td>','')
    tell = str(bsObj.select('td')[2]).replace('<td>','').replace('</td>','').replace('<img alt="" class="icon_call" src="/images/common/icon_call.png"/>','')
    time = str(bsObj.select('td')[3]).replace('<td>','').replace('</td>','')
    cord1 = xcord
    cord2 = ycord
    result.append({'name':name,'branch':branch,'new_addr':new_addr,'old_addr':old_addr,'tell':tell,'time':time,'xcord':cord1,'ycord':cord2})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()