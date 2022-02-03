import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('11_한국특장차.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo():
    url = 'http://www.kortrailer.com/page.php?Main=1&sub=7'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=qe4s3gpsiulcpsh4h9qe8q58o4; 2a0d2363701f23f8a75028924a3af643=MTEyLjE2OS4zMy42Nw%3D%3D',
        'Host': 'www.kortrailer.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.kortrailer.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find_all('div')
    result = []
    for info in div :
        try:
            name = '한국특장차'
            branch = info.find('h3').text
            addr = str(info.select('p')[0]).split('</span>')[1].replace('</p>','').lstrip().rstrip()
            tell = str(info.select('p')[1]).split('</span>')[1].replace('</p>','').replace(' TEL : ','')
            cord = str(info.find('iframe')['src']).split('!2d')
            cord2 = str(cord[1]).split('!')
            xcord = cord2[0]
            ycord = str(cord2[1]).replace('3d','')
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})

    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

