import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('66_한촌설렁탕.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|ID\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s\n' % store['id'])

    outfile.close()

def getStoreInfo():
    url = 'http://hanchon.kr/new/board/view3_map_00/resource/place_find.php'
    data = {
        'board': 'map_01',
        'sca': 'all',
        'search': '',
        'select': 'title_01||addr_road||addr_number',
        'placeName': '',
    }
    pageString = requests.post(url, data = data)
    jsonString = json.loads(pageString.content)
    entityList = jsonString['data']
    result = []
    for info in entityList:
        name = '한촌설렁탕'
        branch = info ['subject']
        addr = info['address']
        tell = info ['phone']
        id = info ['id']
        result.append({"name":name, "branch":branch,"addr":addr,"tell":tell, "id":id})
    return  result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()