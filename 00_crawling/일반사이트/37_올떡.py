import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('37_올떡.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_List = getinfo()
    for store in store_List:
        outfile.write(u'%s|' % store['ID'])
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getinfo():
    url = 'https://www.alltokk.co.kr/shop/shopListJs.asp'
    data = {
        'lat': '',
        'lng': '',
        'search_text': ''
    }
    jsonData = requests.post(url, data=data).text
    print(url, data)
    jsonString = json.loads(jsonData)
    print(jsonString)
    result = []
    for infos in jsonString:
        ID = infos['branch_id']
        name = "올떡"
        branch = infos['branch_name']
        addr = infos['branch_address']
        tell = infos['branch_tel']
        result.append({"ID" : ID,"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()