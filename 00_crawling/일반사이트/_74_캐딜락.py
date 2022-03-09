import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('74_캐딜락.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo():
    url = 'https://www.cadillac.co.kr/shopping/showroom.php'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '캐딜락'
            branch = info.find('div',{"class":"font-16 font-bold"}).text.replace(' ','')
            addr = info.find('div',{"class":"font-12 mt-5 align-left"}).text
            tell = str(info.select('div')[4]).split(',')[0]
            tell = tell.replace('\t','').replace('</div>','').replace('<div class="font-12 mt-5 align-left">\r\n\r\n전화: (','').replace(')','-').replace(' ','')
        except:
            pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()