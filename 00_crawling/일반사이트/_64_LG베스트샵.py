import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('64_LG전자베스트샵.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|OLDADDR|NEWADDR|TELL|XOCRD|YCORD|WEEKTIME|SATTIME|SUNTIME\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['oldaddr'])
        outfile.write(u'%s|' % store['newaddr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s|' % store['ycord'])
        outfile.write(u'%s|' % store['weektime'])
        outfile.write(u'%s|' % store['sattime'])
        outfile.write(u'%s\n' % store['suntime'])
    time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo():
    url = 'https://www.lge.co.kr/lgekor/bestshop/shop/retrieveBestshop.do?currentLatitude=37.4964224&currentLongitude=127.0382592&selAgNums=&selAgNum='
    response = requests.post(url).text
    jsonString = json.loads(response)
    list_all = jsonString[0]['storeData']
    result = []
    for info in list_all:
        name = 'LG전자베스트샵'
        branch = str(info['agName']).replace(' ','')
        oldaddr = info['agAddr1']
        newaddr = info['agNAddr1']
        tell = info['agTel']
        xcord = info['agGpsY']
        ycord = info['agGpsX']
        weekTime = info['agWeekday']
        satTime = info['agSaturday']
        sunTime = info['agSunday']
        result.append({'name':name,'branch':branch,'oldaddr':oldaddr,'newaddr':newaddr,'tell':tell,'xcord':xcord,'ycord':ycord,'weektime':weekTime,'sattime':satTime,'suntime':sunTime})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()