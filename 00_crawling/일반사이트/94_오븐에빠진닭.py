import sys
import requests
import bs4
import codecs
import time
import random
import json
def main():

    outfile = codecs.open('94_오븐에빠진닭.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    area_code = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    for code in area_code:
        storeList = getStoreInfo(code)
        for store in storeList:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(area_code):
    url = 'http://www.oppadak.co.kr/ajax/store.php'
    data = {
        'pg': '200',
        'search_name': '',
        'area_code': '1'
    }
    data['area_code'] = area_code
    pageString = requests.post(url,data = data).text
    jsonString = json.loads(pageString)
    result = []
    try:
        entityList = jsonString['data']
    except: result == []
    else:
        print(entityList)

        for info in entityList:
            name = '오븐에빠진닭'
            branch = info['branch_name']
            addr = info['branch_addr']
            addr = str(addr).replace('\xa0','').replace('   ',' ').replace('  ','')
            tell = info['branch_tel']
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()