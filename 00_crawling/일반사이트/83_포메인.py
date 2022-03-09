import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('83_포메인.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|OLDADDR|NEWADDR|TELL|XCORD|YCORD\n")

    storeList = getStoreInfo()
    for store in storeList:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['oldaddr'])
        outfile.write(u'%s|' % store['newaddr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo():
    url = 'https://phomein.com/brand/store/selectStoreList.do'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=28A11CC66F3D6512D0E982CDA19FB64E; _ga=GA1.2.1895320196.1594874011; _gid=GA1.2.1951555397.1594874011; _gat_gtag_UA_135650389_1=1',
        'Host': 'phomein.com',
        'Pragma': 'no-cache',
        'Referer': 'https://phomein.com/brand/main/main.do',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    data = {
        'name':'',
        'useyn':'1'
    }
    pageString = requests.post(url,data=data ,headers = headers).text
    jsonString = json.loads(pageString)
    print(jsonString)
    entityList = jsonString['resultList']
    result = []
    for info in entityList:
        name = '포메인'
        branch = info['name']
        oldaddr = info['oaddr']
        newaddr = info['naddr']
        tell = info['hp1']+'-'+info['hp2']+'-'+info['hp3']
        xcord = info['longi']
        ycord = info['lat']
        result.append({'name':name,'branch':branch,'oldaddr':oldaddr,'newaddr':newaddr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()