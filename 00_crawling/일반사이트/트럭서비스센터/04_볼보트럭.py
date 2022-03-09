import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('04_볼보트럭.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    store_list = getStoreList()
    for list in store_list:
        store_list = getStoreInfo(list)

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreList():
    url = 'https://www.volvotrucks.kr/ko-kr/dealer-locator.html'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find_all('li', {"style": "width: 115.0px;float: left;list-style: none;margin: 0 0 12.0px 0;"})
    result = []
    for info in div:
        try:
            a = info.find('a')['href']
        except : pass
        else:
            result.append(a)
    return result

def getStoreInfo(url):
    print(url)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = '볼보트럭'
    try:
        try:
            branch = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > h2 > p')).split('>')[1].replace('</p','').replace('볼보트럭 ','')
        except:
            branch = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > h2 > span')).split('>')[1].replace('</span', '').replace('볼보트럭 ', '')
        addr = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(2)')).split('>')[1].replace('</p','')
        if addr == '' :
            addr = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(3)')).split('>')[1].replace('</p','')
        tell = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(3)')).split('>')[1].replace('</p','')
        tell = str(tell.split(',')[0]).replace('대표전화','').replace(')','-').replace(' ','').replace(':','').replace('전화번호','').replace('전화','').lstrip().rstrip()
        if tell.startswith('1') or tell.startswith('0') == False :
            tell = str(bsObj.select(
                'body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(4)')).split(
                '>')[1].replace('</p', '')
            tell = str(tell.split(',')[0]).replace('대표전화', '').replace('전화','').replace(')', '-').replace(' ', '').replace(':', '').replace(
                '전화번호', '').lstrip().rstrip()
        if tell == '' :
            tell = str(bsObj.select(
                'body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(3)')).split(
                '>')[1].replace('</p', '')
            tell = str(tell.split(',')[0]).replace('대표전화', '').replace(')', '-').replace(' ', '').replace(':', '').replace(
                '전화번호', '').lstrip().rstrip()
        if branch == '서산사업소' :
            tell = str(bsObj.select(
                'body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(5)')).split(
                '>')[1].replace('</p', '')
            tell = str(tell.split(',')[0]).replace('대표전화', '').replace(')', '-').replace(' ', '').replace(':', '').replace(
                '전화번호', '').replace('전화', '').lstrip().rstrip()
        time1 = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(6)')).split('>')[1].replace('</p','').replace('- ','').replace('<b/','')
        time2 = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(7)')).split('>')[1].replace('</p','').replace('- ','').replace('<b/','')
        time3 = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(8)')).split('>')[1].replace('</p','').replace('- ','').replace('<b/','')
        time4 = str(bsObj.select('body > div.main-content.container > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div.wrapper > div > div > p:nth-child(9)')).split('>')[1].replace('</p', '').replace('- ', '').replace('<b/', '').replace('<b', '')
        if time4.startswith('<') == True: time4 = ''
        time = str(time1 + '/' + time2 + '/' + time3 + '/' + time4).replace('<b/- ', '').replace('<b/', '').replace('-','').lstrip().rstrip()
    except:
        result.append({'name':name,'branch':url,'addr':'','tell':'','time':''})
    else:
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

