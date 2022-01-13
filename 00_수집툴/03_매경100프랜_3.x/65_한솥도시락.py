import sys
import time
import codecs
import requests
import random
import json
import bs4


def main():

    outfile = codecs.open('65_한솥도시락.txt', 'w', 'utf-8')
    outfile.write("ID|NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    sidoList = ['001','002','003','004','005','006','007','008','009','010','011','012','013','014','015','016','017']
    for sido in sidoList:
        storeList = getStoreInfo(sido)
        for store in storeList:
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['time'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])

        time.sleep(random.uniform(0.3, 0.9))

def getStoreInfo(sidoCode):
    url = 'https://www.hsd.co.kr/api/store_search'
    params = {
        'idx': '',
        # 'sido': '001',
        'gungoo': '',
        'searchKeyword': '',
    }
    params['sido']=sidoCode
    pageString = requests.get(url, params = params).text
    jsonString = json.loads(pageString)
    print(url , sidoCode)
    result =[]
    for info in jsonString:
        id = info['storeId']
        name = '한솥도시락'
        branch = info['name']
        addr = info['address']
        tell = info['phoneNumber']
        time = info['businessHour'].replace('\n','')
        xcord = info['lng']
        ycord = info['lat']
        if id == '' : pass
        else :
            result.append({"id":id,"name": name, "branch": branch, "addr": addr, "tell": tell, "time": time, "xcord": xcord, "ycord": ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
