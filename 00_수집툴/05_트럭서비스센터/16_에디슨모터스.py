import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('16_에디슨모터스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()

    for store in store_list:
        if store['branch'] == '상호' : pass
        else:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
# 다 수집하고 나서 부품대리점은 수동으로 지워줘야합니다.(성일공업사) 위로는 다 삭제
def getStoreInfo():
    url = 'http://www.edisonmotorsev.com/customer/center'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.daewoobus.co.kr',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr :
        try:
            name = '에디슨모터스'
            branch = info.find('td').text.replace('(주)','')
            addr = str(info.select('td')[1]).replace('<td>','').replace('</td>','').lstrip().rstrip()
            tell = str(info.select('td')[3]).replace('<td class="ls0">','').replace('</td>','').split('  ')[0].lstrip().rstrip()
            xcord = info['data-y']
            ycord = info['data-x']
            if branch == '지정정비공장':
                branch = str(info.select('td')[1]).replace('(주)','').replace('<td>', '').replace('</td>','').lstrip().rstrip()
                addr = str(info.select('td')[2]).replace('<td>', '').replace('</td>', '').lstrip().rstrip()
                tell = str(info.select('td')[4]).replace('<td class="ls0">', '').replace('</td>','').split('  ')[0].lstrip().rstrip()
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

