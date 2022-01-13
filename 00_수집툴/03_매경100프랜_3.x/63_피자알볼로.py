import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('63_피자알볼로.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['time'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    time.sleep(random.uniform(0.3, 0.9))

def getStoreInfo():
    url = 'https://www.pizzaalvolo.co.kr/api/stores'
    parmas = {
        'name':'점'
    }
    pageString = requests.get(url, params = parmas).text
    jsonString = json.loads(pageString)
    entityList = jsonString['result']
    result = []
    for info in entityList:
        try:
            name = '피자알볼로'
            branch = info['name']
            addr = info['address1'] + ' ' + info['address2'] + ' ' + info['address3'] + ' ' + info['address4']
            tell = info['mainPhone']
            time = info['openTime'] + '~' + info['closeTime']
            xcord = info['lng']
            ycord = info['lat']
        except:
            pass
        else:
            result.append({"name":name, "branch":branch,"addr":addr,"tell":tell,"time":time,"xcord":xcord,"ycord":ycord})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
