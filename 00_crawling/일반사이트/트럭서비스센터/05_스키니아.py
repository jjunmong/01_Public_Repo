import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('05_스키니아.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    store_list = getStoreList()
    for list in store_list:
        store_list = getStoreInfo(list)
        print(list)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['time'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])

        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreList():
    url = 'https://www.scania.com/kr/ko/home/misc/dealer-locator/dealer-listing.html'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find_all('div',{"class":"col-sm-12 col-md-4 department-tile-container"})
    result = []
    for info in div :
        a= str(info.find('a')['href'])
        result.append(a)
    return result

def getStoreInfo(url):
    urls = 'https://www.scania.com'+url
    pageString = requests.get(urls).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = '스키니아'
    branch = bsObj.find('h1',{"data-analytics-lead":"dd_dealername"}).text
    addr = str(bsObj.find('p',{"class":"how-to-find"}).text).split('\n')[4].lstrip().rstrip()
    tell = str(bsObj.select('div > div.grey-area > div.how-to-find.maxWidth > div > div:nth-child(2) > div > p:nth-child(1)')).split('>')[4].replace('+82 (','').replace('</p','').replace(')','').lstrip().rstrip().replace(' ','-').replace('+82-','')
    time1 = str(bsObj.select('div > div.grey-area > div.how-to-find.maxWidth > div > div:nth-child(1) > div > div:nth-child(1) > div > p > strong')).replace('[<strong>','').replace('</strong>]','').replace('\n','').replace(' ','')
    time2 = str(bsObj.select('div > div.grey-area > div.how-to-find.maxWidth > div > div:nth-child(1) > div > div:nth-child(1) > div > div > p')).replace('[<p class="time-stamp"> ','').replace('</p>]','')
    time3 = str(bsObj.select('div > div.grey-area > div.how-to-find.maxWidth > div > div:nth-child(1) > div > div:nth-child(2) > div > p > strong')).replace('[<strong>','').replace('</strong>]','').replace('\n','').replace(' ','')
    time4 = str(bsObj.select('div > div.grey-area > div.how-to-find.maxWidth > div > div:nth-child(1) > div > div:nth-child(2) > div > div > p')).replace('[<p class="time-stamp"> ','').replace('</p>]','')
    cord = str(bsObj.find('a',{"data-analytics-lead":"dd_direction"})['href']).split(',')
    xcord = cord[1]
    ycord = str(cord[0]).replace('https://maps.google.com/maps?q=','')
    time = time1 + ':' + time2 + '/' + time3 + ':' + time4
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

