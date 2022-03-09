import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('83_파파존스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo():
    url = 'https://www.pji.co.kr/searchStore?addr1=&addr2=&name2='
    pageString = requests.get(url).text
    jsonstring = json.loads(pageString)
    entityList = jsonstring['list']
    result = []
    for info in entityList:
        try:
            name = '파파존스'
            branch = info['name']
            addr = info['address']
            tell = info['phone1']
            xcord = info['xaxis']
            ycord = info['yaxis']
        except:
            pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()