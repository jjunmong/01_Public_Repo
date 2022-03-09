import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('87_60계치킨.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    url_list = getStoreInfo_all()
    for url in url_list:
        storeList = getStoreInfo(url)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
def getStoreInfo_url(intPageNo):
    url = 'http://www.60chicken.com/bbs/board.php?bo_table=store&page={}&si=&gu=&dong='.format(intPageNo)
    pageString = requests.get(url)
    print(intPageNo)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            link = info.find('a')['href']
        except : pass
        else:
            result.append(link)
    return result

def getStoreInfo_all():
    result = []
    page = 1
    while True:
        result = result + getStoreInfo_url(page)
        if getStoreInfo_url(page) == [] : break
        page += 1
    return result

def getStoreInfo(url_list):
    url = url_list
    pageString = requests.get(url)
    print(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    result = []
    name = '60계치킨'
    infos = bsObj.find('dd').text
    branch = infos.split('\n')[1]
    addr = infos.split('\n')[4]
    addr = addr.replace('주소 : ','')
    tell = infos.split('\n')[5]
    tell = tell.replace('전화번호 : ','')
    cord = bsObj.select('script')
    cord = str(cord).split('var')
    xcord = str(cord[12]).replace(' wr_lng = ','').replace(';\n','')
    ycord = str(cord[11]).replace(' wr_lat = ','').replace(';\n','')
    result.append({'name':name, 'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()