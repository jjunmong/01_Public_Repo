import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('115_청담이상.txt', 'w', 'utf-8')
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
    url = 'http://www.leesang.co.kr/store/find_store_proc.php'
    data = {
        'RetrieveFlag': 'MARK',
        'str_xpoint1': '31.47314607546956',
        'str_xpoint2': '38.85869229872511',
        'str_ypoint1': '118.64996763649268',
        'str_ypoint2': '135.72111158231516',
        'str_level': '13',
        'pg': '1',
        'page': '1',
        'str_mxpoint': '',
        'str_mypoint': '',
        'str_sido': '',
        'str_sigun': '',
        'Txt_word': '',
    }
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        name = '청담이상'
        branch = info['title']
        addr = info['addr']
        tell = info['tel']
        cordx = info['latlng2']
        cordy = info['latlng1']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'cordx':cordx,'cordy':cordy})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()