import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('65_아트박스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD|WEEKTIME\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s|' % store['ycord'])
        outfile.write(u'%s\n' % store['weektime'])
    time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo():
    url = 'https://www.artbox.co.kr/goods/storeInfoLayer.action'
    data = {
        '_': '1616546952877',
        'pointYn': 'N',
        'keyword': '',
        'place': '전체',
        'shop_no': '',
    }
    response = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '아트박스'
            branch = info.find('span',{"class":"txt"}).text.replace('\r','').replace('\n','').replace('\t','')
            addr = str(info.select('td')[3]).replace('<td><span class="txt">','').replace('</span></td>','')
            tell = str(info.select('td')[2]).replace('<td><span class="nor">','').replace('</span></td>','')
            xcord = info.find('button')['data-point-y']
            ycord = info.find('button')['data-point-x']
            weektime = str(info.select('td')[1]).replace('<td><span class="nor">','').replace('</span></td>','')
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord,'weektime':weektime})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()