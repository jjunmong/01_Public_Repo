import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('78_신영증권.txt', 'w', 'utf-8')
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
    url = 'https://www.shinyoung.com/Assets/ini/location.ini?_=1632448347339'
    pageString = requests.get(url).text
    jsonstring = json.loads(pageString)
    result = []
    for info in jsonstring:
        try:
            name = '신영증권'
            branch = info['NAME']
            addr = info['ADDRESS']
            tell = info['TEL']
            cord = str(info['LOCATION']).split(',')
            xcord = str(cord[1]).strip()
            ycord = str(cord[0]).strip()
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