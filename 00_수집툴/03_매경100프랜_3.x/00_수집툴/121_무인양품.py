import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('121_무인양품.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|CORDX|CORDY\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['cordx'])
        outfile.write(u'%s\n' % store['cordy'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo():
    url = 'https://www.muji.com/storelocator/?_ACTION=_SEARCH&c=kr&lang=LC&swLat=34.644543398180495&swLng=123.82644583203123&neLat=38.31799097705596&neLng=131.90689016796873'
    pageString = requests.get(url).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        try:
            name = '무인양품'
            branch = info['shopname']
            branch = branch.replace('MUJI ','').replace(' ','')
            addr = info['shopaddress']
            tell = info['tel']
            tell = tell.replace('\u3000','')
            cordx = info['longitude']
            cordy = info['latitude']
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'cordx':cordx,'cordy':cordy})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()