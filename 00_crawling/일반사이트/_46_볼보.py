import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('46_볼보서비스센터.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME1|TIME2|XCORD|YCORD\n")

    store_list = getStoreInfo_svc()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['time1'])
        outfile.write(u'%s|' % store['time2'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

    outfile = codecs.open('46_볼보.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME1|TIME2|XCORD|YCORD\n")

    store_list = getStoreInfo_showroom()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['time1'])
        outfile.write(u'%s|' % store['time2'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo_svc():
    url = 'https://vckiframe.com/oxp/center/json/service.json'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.155548789.1591342790; _gid=GA1.2.1846973381.1591342790; _gat_gtag_UA_163181869_1=1',
        'Host': 'vckiframe.com',
        'Pragma': 'no-cache',
        'Referer': 'https://vckiframe.com/oxp/center/index.html?type=service',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    pageString = requests.get(url, headers = headers, verify = False).text
    jsonData = json.loads(pageString)
    result = []
    for info in jsonData:
        name = '볼보서비스센터'
        branch = info['name']
        branch = branch.replace('볼보','').replace(' ','')
        addr = info['addr'].replace('<span>','').replace('</span>','')
        tell = info['phone']
        time1 = info['time_1']
        time2 = info['time_2']
        xcord = info['lng']
        ycord = info['lat']
        result.append({"name":name, "branch":branch,"addr":addr,"tell":tell,"time1":time1,"time2":time2,"xcord":xcord,"ycord":ycord})
    return result

def getStoreInfo_showroom():
    url = 'https://vckiframe.com/oxp/center/json/showroom.json'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.155548789.1591342790; _gid=GA1.2.1846973381.1591342790; _gat_gtag_UA_163181869_1=1',
        'Host': 'vckiframe.com',
        'Pragma': 'no-cache',
        'Referer': 'https://vckiframe.com/oxp/center/index.html?type=service',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    pageString = requests.get(url, headers = headers, verify = False).text
    jsonData = json.loads(pageString)
    result = []
    for info in jsonData:
        name = '볼보'
        branch = info['name']
        branch = branch.replace('볼보','').replace(' ','')
        addr = info['addr'].replace('<span>','').replace('</span>','')
        tell = info['phone']
        time1 = info['time_1']
        time2 = info['time_2']
        xcord = info['lng']
        ycord = info['lat']
        result.append({"name":name, "branch":branch,"addr":addr,"tell":tell,"time1":time1,"time2":time2,"xcord":xcord,"ycord":ycord})
    return result


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

