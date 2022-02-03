import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('09_이스즈.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    store_list = getStoreInfo()
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
def getStoreInfo():
    url = 'http://isuzukorea.com/helpdesk/services.asp'
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr :
        try:
            name = '이스즈'
            branch = str(info.find('td',{"class":"area"})).split('>')[4].replace('</td','').lstrip().rstrip()
            addr = str(info.find('td',{"class":"add"})).split('주소')[1].replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t </div>\n</div>\n</div>\n</div>\n</td>','').replace(' : ','').lstrip().rstrip()
            infos = str(info.find('td',{"class":"call"}).text).split('\n')
            tell = str(infos[0]).lstrip().rstrip()
            time = str(infos[1]).lstrip().rstrip()
            cord = str(info.find('script')).split(',')
            xcord = str(cord[2]).replace(')','').lstrip().rstrip()
            ycord = str(cord[1]).replace(' {\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcenter: new naver.maps.LatLng(','').lstrip().rstrip()
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time,'xcord':xcord,'ycord':ycord})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

