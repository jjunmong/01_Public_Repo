import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('43_신영증권.txt', 'w', 'utf-8')
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
    url = 'https://www.shinyoung.com/Assets/ini/location.ini?_=1612858145604'
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=roYXSHWutejK8w59Pqsr2wh3n9ScNnfy6dMDwDq2.was01',
        'Host': 'www.shinyoung.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.shinyoung.com/?page=10019',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    pageString = requests.get(url, headers = headers).text
    jsonString = json.loads(pageString)

    result = []
    for info in jsonString:
        try:
            name = '신영증권'
            branch = info['NAME']
            addr = info['ADDRESS']
            tell = info['TEL']
            cord = str(info['LOCATION']).split(',')
            xcord = str(cord[1]).lstrip().rstrip()
            ycord = str(cord[0]).lstrip().rstrip()
        except:
            pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()