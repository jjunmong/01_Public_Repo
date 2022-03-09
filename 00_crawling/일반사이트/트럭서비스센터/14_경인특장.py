import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('14_경인특장.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if len(store_list) < 3: break
        print(page)
        for store in store_list:
            if store['addr'] == None : pass
            else:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.kyeonginvan.com/bbs/board.php?board=chainstore&indexorder=2&no=&command=list&page={}'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=65456b5b8da4227f6f8c62bfb0523bb6',
        'Host': 'www.kyeonginvan.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.kyeonginvan.com/bbs/board.php?board=chainstore',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr :
        try:
            name = '경인특장'
            branch = info.find('a').text.lstrip().rstrip()
            addr = str(info.select('td')[1]).replace('<td class="list_wr_add">','').replace('</td>','').replace('\r','').replace('\n','').replace('\t','').lstrip().rstrip()
            if len(addr) > 50: addr = None
            tell = str(info.select('td')[2]).replace('<td class="list_wr_add" width="130">','').replace('</td>','').replace('\r','').replace('\n','').replace('\t','').replace('TEL. ','').lstrip().rstrip()
            if len(tell) > 50: tell = None
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})

    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

