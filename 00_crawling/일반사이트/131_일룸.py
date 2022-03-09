import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('131_일룸.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD")

    sido_list = ['A02001',	'A02002',	'A02003',	'A02004',	'A02005',	'A02006',	'A02007',	'A02008',	'A02009',	'A02010',	'A02011',	'A02012',	'A02013',	'A02014']

    for sido in sido_list:
        store_list = getStoreInfo(sido)
        print(sido)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(sidoCode):
    url = 'https://www.iloom.com/store/changeStoreList.do'
    data = {
        # 'area1': 'A02001',
        'area2': '',
        'type': 'A',
    }
    data['area1'] = sidoCode
    pageString = requests.post(url, data = data).text
    pageString = pageString.replace(' 				','')
    jsonString = json.loads(pageString)
    entityList = jsonString['list']
    result = []
    for info in entityList:
        try:
            name = '일룸'
            branch = info['storeNm']
            addr = str(info['address']).lstrip().rstrip()
            tell = info['phone']
            xcord = info['storeLng']
            ycord = info['storeLat']
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()