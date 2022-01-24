import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('73_닛산.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD\n")

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
    url = 'https://www.nissan.co.kr/content/nissan_prod/ko_KR/index/dealer-finder/jcr:content/freeEditorial/contentzone_e70c/columns/columns12_df4d/col1-par/find_a_dealer_1b87.extended_dealers_by_location.json/_charset_/utf-8/page/1/size/30/data.json'
    res = requests.get(url).text
    jsonString = json.loads(res)
    entityList = jsonString['dealers']
    result = []
    for info in entityList:
        name = '닛산'
        branch = str(info['tradingName']).replace(' ','')
        addr = info['address']['addressLine1']
        tell = str(info['contact']['phone']).replace('(','').replace(')','-')
        xcord = info['geolocation']['longitude']
        ycord = info['geolocation']['latitude']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()