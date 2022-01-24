import sys
import time
import codecs
import requests
import random
import json
import bs4
import urllib.parse

def main():

    outfile = codecs.open('41_신한카드.txt', 'w', 'utf-8')
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
    url = 'https://www.shinhancard.com/mob/MOBFM12121N/MOBFM12121R02.ajax'
    data={}
    data['mbw_json'] = '{"areanum":"'+'","gubun":"1","flag":"card"}'
    pageString = requests.post(url,data= data).text
    jsonString = json.loads(pageString)
    entityList = jsonString['mbw_json']['allBranchInfoList']
    result = []
    for info in entityList:
        name = '신한카드'
        branch = info['deptname']
        addr = str(info['deptaddr1'])
        tell = info['phonenum1']
        xcord = info['x']
        ycord = info['y']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})

    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()