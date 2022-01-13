import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('129_에넥스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'http://www.enex.co.kr/store/store.php?&nowPage={}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '에넥스'
            branch = str(info.select('td')[0]).replace('<td>','').replace('</td>','').replace('에넥스','').replace(' ','').lstrip().rstrip()
            addr = str(info.select('td')[1]).replace('<td>','').replace('</td>','').lstrip().rstrip()
            tell = str(info.select('td')[2]).replace('<td>','').replace('</td>','').lstrip().rstrip()
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()