import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('31_신라명과.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s\n' % store['time'])

    outfile.close()

def getStoreInfo():
    url = 'http://www.shillabakery.com/hi-story/today-shilla/store/'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    div = bsObj.find_all('div',{"class":"inner-wrap"})
    result = []
    for info in div:
        try:
            name = '신라명과'
            branch = info.find('p',{"class":"title"}).text
            branch = branch.replace('신라명과 ','')
            infos = info.select('p')[2]
            infos = str(infos).split('\n')
            addr = infos[0]
            addr = str(addr).replace('<p>','').replace('<br/>','').lstrip().rstrip()
            tell = infos[1]
            tell = str(tell).replace('<br/>','').lstrip().rstrip().replace('T.','')
            time = infos[2]
            time = str(time).replace('<br/>','').lstrip().rstrip().replace('</p>','')
        except:
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
